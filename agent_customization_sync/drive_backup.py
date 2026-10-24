"""
drive_backup.py
---------------
Automated Google Drive Cloud Backup for Global Customizations, SSOT Skills,
and CLI Runner Scripts.
Seamlessly backs up latest snapshot bundles, Merkle manifests, and local_bin shims
to Google Drive folder preserving permanent fileIds and enabling cloud disaster recovery.
"""

from __future__ import annotations

import hashlib
import json
import os
import random
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

from agent_customization_sync.local_bin_provisioner import LocalBinProvisioner
from agent_customization_sync.snapshot_engine import SnapshotEngine

TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
DRIVE_UPLOAD_ENDPOINT = "https://www.googleapis.com/upload/drive/v3/files"
DRIVE_FILES_ENDPOINT = "https://www.googleapis.com/drive/v3/files"
DEFAULT_FOLDER_ID = "1wGq53okV7ZaFGSw2fWilEfxL4FEIVeIF"


def sha256_file(path: Path) -> str:
    """Computes SHA-256 checksum of a local file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def request_with_retry(
    req: urllib.request.Request,
    max_retries: int = 5,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
) -> tuple[int, bytes]:
    """Executes urllib request with exponential backoff for transient HTTP errors."""
    last_err: Exception | None = None
    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return resp.status, resp.read()
        except urllib.error.HTTPError as e:
            body = e.read()
            last_err = e
            if e.code in (429, 500, 502, 503, 504) and attempt < max_retries - 1:
                sleep_time = initial_delay * (backoff_factor ** attempt) + random.uniform(0.1, 0.5)
                time.sleep(sleep_time)
                continue
            raise urllib.error.HTTPError(e.url, e.code, body.decode("utf-8", errors="replace"), e.hdrs, None) from e
        except urllib.error.URLError as e:
            last_err = e
            if attempt < max_retries - 1:
                sleep_time = initial_delay * (backoff_factor ** attempt) + random.uniform(0.1, 0.5)
                time.sleep(sleep_time)
                continue
            raise
    if last_err:
        raise last_err
    raise RuntimeError("Unexpected request failure without error.")


def get_oauth_credentials() -> tuple[str | None, str | None, str | None]:
    """Resolves OAuth credentials from environment variables or local credential files."""
    client_id = os.environ.get("GDRIVE_CLIENT_ID")
    client_secret = os.environ.get("GDRIVE_CLIENT_SECRET")
    refresh_token = os.environ.get("GDRIVE_REFRESH_TOKEN")

    if not (client_id and client_secret) and os.environ.get("GDRIVE_CLIENT_SECRET_JSON"):
        try:
            raw = json.loads(os.environ["GDRIVE_CLIENT_SECRET_JSON"])
            inst = raw.get("installed") or raw.get("web") or raw
            client_id = inst.get("client_id")
            client_secret = inst.get("client_secret")
        except Exception:
            pass

    if not (client_id and client_secret):
        oauth_path = os.environ.get("GDRIVE_OAUTH_PATH") or os.path.expanduser("~/.gdrive-credentials.json")
        if os.path.exists(oauth_path):
            try:
                with open(oauth_path, encoding="utf-8") as f:
                    oauth = json.load(f)
                    keys = oauth.get("installed") or oauth.get("web") or oauth
                    client_id = keys.get("client_id")
                    client_secret = keys.get("client_secret")
            except Exception:
                pass

    if not refresh_token:
        creds_path = os.environ.get("GDRIVE_CREDENTIALS_PATH") or os.path.expanduser("~/.gdrive-server-credentials.json")
        if os.path.exists(creds_path):
            try:
                with open(creds_path, encoding="utf-8") as f:
                    creds = json.load(f)
                    refresh_token = creds.get("refresh_token")
            except Exception:
                pass

    return client_id, client_secret, refresh_token


def obtain_access_token(client_id: str, client_secret: str, refresh_token: str) -> str:
    """Exchanges refresh token for a fresh Google OAuth2 access token with retry."""
    payload = urllib.parse.urlencode({
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
    }).encode("utf-8")

    req = urllib.request.Request(TOKEN_ENDPOINT, data=payload, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")

    status, body = request_with_retry(req)
    data = json.loads(body.decode("utf-8"))
    if "access_token" not in data:
        raise RuntimeError(f"OAuth token response missing access_token: {data}")
    return data["access_token"]


def find_drive_file_by_name(access_token: str, folder_id: str, file_name: str) -> str | None:
    """Checks if a file with the given name already exists in the target folder."""
    safe_name = file_name.replace("'", "\\'")
    query = f"'{folder_id}' in parents and name = '{safe_name}' and trashed = false"
    url = f"{DRIVE_FILES_ENDPOINT}?q={urllib.parse.quote(query)}&fields=files(id,name,mimeType)"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {access_token}"})
    try:
        status, body_bytes = request_with_retry(req)
        data = json.loads(body_bytes.decode("utf-8"))
        files = data.get("files", [])
        if files:
            return files[0]["id"]
    except Exception:
        pass
    return None


def update_drive_file(access_token: str, file_id: str, content_bytes: bytes, mime_type: str = "application/octet-stream") -> bool:
    """Updates an existing Google Drive file in-place preserving its permanent fileId."""
    if len(content_bytes) > 5 * 1024 * 1024:
        # Resumable upload for large files
        init_req = urllib.request.Request(
            f"https://www.googleapis.com/upload/drive/v3/files/{file_id}?uploadType=resumable",
            method="PATCH"
        )
        init_req.add_header("Authorization", f"Bearer {access_token}")
        init_req.add_header("X-Upload-Content-Type", mime_type)
        init_req.add_header("X-Upload-Content-Length", str(len(content_bytes)))
        with urllib.request.urlopen(init_req, timeout=30) as resp:
            loc = resp.headers.get("Location")
        if not loc:
            return False

        chunk_size = 4 * 1024 * 1024
        total_size = len(content_bytes)
        offset = 0
        while offset < total_size:
            chunk = content_bytes[offset:offset + chunk_size]
            chunk_len = len(chunk)
            end = offset + chunk_len - 1
            chunk_req = urllib.request.Request(loc, data=chunk, method="PUT")
            chunk_req.add_header("Content-Length", str(chunk_len))
            chunk_req.add_header("Content-Range", f"bytes {offset}-{end}/{total_size}")
            chunk_req.add_header("Content-Type", mime_type)
            with urllib.request.urlopen(chunk_req, timeout=120) as cr:
                if cr.status in (200, 201):
                    return True
            offset += chunk_len
        return True

    # Simple media upload for files <= 5MB
    url = f"{DRIVE_UPLOAD_ENDPOINT}/{file_id}?uploadType=media"
    req = urllib.request.Request(url, data=content_bytes, method="PATCH")
    req.add_header("Authorization", f"Bearer {access_token}")
    req.add_header("Content-Type", mime_type)
    status, _ = request_with_retry(req)
    return status in (200, 201)


def create_drive_file(
    access_token: str,
    folder_id: str,
    file_name: str,
    content_bytes: bytes,
    mime_type: str = "application/octet-stream",
    description: str = "",
) -> str:
    """Creates a new file inside the specified Drive folder and returns its permanent fileId."""
    metadata = {
        "name": file_name,
        "parents": [folder_id],
        "mimeType": mime_type,
        "description": description,
    }

    if len(content_bytes) > 5 * 1024 * 1024:
        meta_bytes = json.dumps(metadata).encode("utf-8")
        init_req = urllib.request.Request(
            "https://www.googleapis.com/upload/drive/v3/files?uploadType=resumable",
            data=meta_bytes,
            method="POST"
        )
        init_req.add_header("Authorization", f"Bearer {access_token}")
        init_req.add_header("Content-Type", "application/json; charset=UTF-8")
        init_req.add_header("X-Upload-Content-Type", mime_type)
        init_req.add_header("X-Upload-Content-Length", str(len(content_bytes)))
        with urllib.request.urlopen(init_req, timeout=30) as resp:
            loc = resp.headers.get("Location")
        if not loc:
            raise RuntimeError("Failed to initiate resumable upload session.")

        chunk_size = 4 * 1024 * 1024
        total_size = len(content_bytes)
        offset = 0
        while offset < total_size:
            chunk = content_bytes[offset:offset + chunk_size]
            chunk_len = len(chunk)
            end = offset + chunk_len - 1
            chunk_req = urllib.request.Request(loc, data=chunk, method="PUT")
            chunk_req.add_header("Content-Length", str(chunk_len))
            chunk_req.add_header("Content-Range", f"bytes {offset}-{end}/{total_size}")
            chunk_req.add_header("Content-Type", mime_type)
            with urllib.request.urlopen(chunk_req, timeout=120) as cr:
                if cr.status in (200, 201):
                    res = json.loads(cr.read().decode("utf-8"))
                    return res["id"]
            offset += chunk_len
        raise RuntimeError("Resumable creation did not finish.")

    # Multipart create for files <= 5MB
    boundary = "===============" + str(random.randint(10**10, 10**11)) + "=="
    meta_json = json.dumps(metadata)
    body = (
        f"--{boundary}\r\n"
        f"Content-Type: application/json; charset=UTF-8\r\n\r\n"
        f"{meta_json}\r\n"
        f"--{boundary}\r\n"
        f"Content-Type: {mime_type}\r\n\r\n"
    ).encode() + content_bytes + f"\r\n--{boundary}--\r\n".encode()

    url = f"{DRIVE_UPLOAD_ENDPOINT}?uploadType=multipart"
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Authorization", f"Bearer {access_token}")
    req.add_header("Content-Type", f"multipart/related; boundary={boundary}")

    status, res_bytes = request_with_retry(req)
    data = json.loads(res_bytes.decode("utf-8"))
    return data["id"]


class CustomizationDriveBackup:
    """Manages Drive cloud backups for snapshot archives, manifests, and runner shims."""

    def __init__(
        self,
        folder_id: str = DEFAULT_FOLDER_ID,
        source_dir: Path | None = None,
        snapshot_dir: Path | None = None,
        manifest_file: Path | None = None,
    ):
        self.folder_id = folder_id
        self.source_dir = source_dir or (Path.home() / ".gemini" / "config")
        self.snapshot_dir = snapshot_dir or (Path.home() / ".gemini" / "snapshots" / "customizations")
        self.manifest_file = manifest_file or (self.snapshot_dir / "drive_backup_manifest.json")
        self.engine = SnapshotEngine(source_dir=self.source_dir, snapshot_dir=self.snapshot_dir)
        self.local_bin = LocalBinProvisioner()

    def load_manifest(self) -> dict[str, Any]:
        """Loads or initializes the drive backup manifest."""
        if self.manifest_file.is_file():
            try:
                return json.loads(self.manifest_file.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {
            "schema_version": "1.0.0",
            "folder_id": self.folder_id,
            "folder_url": f"https://drive.google.com/drive/folders/{self.folder_id}",
            "last_synced_at": None,
            "files": {}
        }

    def save_manifest(self, data: dict[str, Any]) -> None:
        """Persists the drive backup manifest."""
        self.manifest_file.parent.mkdir(parents=True, exist_ok=True)
        self.manifest_file.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def run_backup(self, dry_run: bool = False, force: bool = False) -> dict[str, Any]:
        """Uploads or synchronizes latest snapshot bundle, manifest, and local_bin manifest to Drive."""
        snapshots = self.engine.list_snapshots()
        if not snapshots:
            raise RuntimeError("No customization snapshots found. Run 'custom_sync.bat snapshot' first.")

        latest_snap = snapshots[0]
        snap_path = Path(latest_snap.filepath)
        if not snap_path.is_file():
            raise FileNotFoundError(f"Snapshot archive not found at {snap_path}")

        manifest_path = self.source_dir / "customization_manifest.json"
        local_bin_audit = self.local_bin.audit()
        local_bin_manifest_data = json.dumps(local_bin_audit, indent=2).encode("utf-8")

        # Collect targets
        targets = [
            {
                "key": "customization_state_latest.zip",
                "name": "customization_state_latest.zip",
                "content": snap_path.read_bytes(),
                "mime": "application/zip",
                "desc": f"Agent Customization Sync — State Archive ({latest_snap.snapshot_id})",
                "local_sha": latest_snap.sha256_root or sha256_file(snap_path),
            },
            {
                "key": "local_bin_manifest.json",
                "name": "local_bin_manifest.json",
                "content": local_bin_manifest_data,
                "mime": "application/json",
                "desc": "Agent Customization Sync — Global ~/.local/bin CLI Shims Audit Manifest",
                "local_sha": hashlib.sha256(local_bin_manifest_data).hexdigest(),
            }
        ]

        if manifest_path.is_file():
            man_bytes = manifest_path.read_bytes()
            targets.insert(1, {
                "key": "customization_manifest.json",
                "name": "customization_manifest.json",
                "content": man_bytes,
                "mime": "application/json",
                "desc": "Agent Customization Sync — SHA-256 Merkle Manifest (58 Skills, Rules, MCP)",
                "local_sha": hashlib.sha256(man_bytes).hexdigest(),
            })

        print("=== Customization Google Drive Cloud Backup ===")
        print(f"Target Drive Folder : {self.folder_id}")
        print(f"Latest Snapshot ID  : {latest_snap.snapshot_id}")
        print(f"Mode                : {'DRY-RUN (Preview)' if dry_run else 'LIVE UPLOAD'}")
        print("-" * 55)

        manifest_data = self.load_manifest()
        manifest_files = manifest_data.setdefault("files", {})

        if dry_run:
            results = []
            for t in targets:
                f_meta = manifest_files.get(t["key"], {})
                prev_sha = f_meta.get("sha256")
                status = "IN_SYNC" if (prev_sha == t["local_sha"] and not force) else "NEEDS_SYNC"
                print(f"[{status}] {t['name']} ({len(t['content']):,} bytes, SHA: {t['local_sha'][:8]})")
                results.append({"name": t["name"], "status": status, "size": len(t["content"])})
            return {"status": "dry_run", "targets": results}

        # Resolve credentials & token
        cid, sec, rtok = get_oauth_credentials()
        if not (cid and sec and rtok):
            raise RuntimeError("Missing Google Drive OAuth credentials (~/.gdrive-server-credentials.json).")

        access_token = obtain_access_token(cid, sec, rtok)
        synced_count = 0

        for t in targets:
            f_meta = manifest_files.get(t["key"], {})
            file_id = f_meta.get("drive_file_id")
            prev_sha = f_meta.get("sha256")

            if file_id and prev_sha == t["local_sha"] and not force:
                print(f"[UP_TO_DATE] {t['name']} -> ID: {file_id}")
                continue

            if not file_id:
                # Search if file already exists in folder
                existing_id = find_drive_file_by_name(access_token, self.folder_id, t["name"])
                if existing_id:
                    file_id = existing_id
                    print(f"[FOUND_EXISTING] {t['name']} -> ID: {file_id}")

            if file_id:
                print(f"[UPDATING] {t['name']} ({len(t['content']):,} bytes)...", end=" ", flush=True)
                ok = update_drive_file(access_token, file_id, t["content"], t["mime"])
                if ok:
                    print("DONE")
                else:
                    raise RuntimeError(f"Failed to update {t['name']} (ID: {file_id})")
            else:
                print(f"[CREATING] {t['name']} ({len(t['content']):,} bytes)...", end=" ", flush=True)
                file_id = create_drive_file(
                    access_token=access_token,
                    folder_id=self.folder_id,
                    file_name=t["name"],
                    content_bytes=t["content"],
                    mime_type=t["mime"],
                    description=t["desc"]
                )
                print(f"CREATED (ID: {file_id})")

            manifest_files[t["key"]] = {
                "drive_file_id": file_id,
                "drive_file_name": t["name"],
                "description": t["desc"],
                "sha256": t["local_sha"],
                "size_bytes": len(t["content"]),
                "last_uploaded_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "source_snapshot": latest_snap.snapshot_id,
            }
            synced_count += 1

        manifest_data["last_synced_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        self.save_manifest(manifest_data)
        print("-" * 55)
        print(f"[OK] Google Drive Cloud Backup complete. {synced_count} file(s) updated/created.")
        return manifest_data
