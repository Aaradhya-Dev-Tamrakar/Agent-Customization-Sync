"""
test_manifest.py
----------------
Unit tests for manifest generation, Merkle root hashing, and token estimation.
"""

from pathlib import Path
from agent_customization_sync.manifest import (
    CustomizationManifest,
    estimate_tokens,
    sha256_file,
    sha256_dir,
)


def test_estimate_tokens():
    assert estimate_tokens("") == 0
    short_text = "This is a brief directive for the agent."
    assert estimate_tokens(short_text) > 0

    long_text = "word " * 1000
    tokens = estimate_tokens(long_text)
    # 1000 words should estimate to around 1300 tokens
    assert 1000 <= tokens <= 1500


def test_sha256_file_and_dir(tmp_path: Path):
    import hashlib
    test_file = tmp_path / "sample.txt"
    content = b"Hello World\n"
    test_file.write_bytes(content)
    file_hash = sha256_file(test_file)
    assert len(file_hash) == 64
    assert file_hash == hashlib.sha256(content).hexdigest()

    # Directory hash
    d_hash, count, tokens = sha256_dir(tmp_path)
    assert len(d_hash) == 64
    assert count == 1
    assert tokens > 0


def test_manifest_from_dir(mock_config_dir: Path):
    manifest = CustomizationManifest.from_dir(mock_config_dir)
    assert manifest.schema_version == "1.0.0"
    assert "AGENTS.md" in manifest.rules
    assert "GEMINI.md" in manifest.rules
    assert "skill-alpha" in manifest.skills
    assert "skill-beta" in manifest.skills
    assert "classroom" in manifest.mcp_servers
    assert "disabled-server" in manifest.mcp_servers
    assert manifest.mcp_servers["disabled-server"].disabled is True
    assert manifest.total_token_overhead > 0
    assert manifest.headroom_percent > 90.0
    assert len(manifest.sha256_root) == 64

    # JSON roundtrip
    json_str = manifest.to_json()
    loaded = CustomizationManifest.from_json(json_str)
    assert loaded.sha256_root == manifest.sha256_root
    assert len(loaded.skills) == len(manifest.skills)
    assert len(loaded.rules) == len(manifest.rules)


def test_manifest_root_hash_changes_on_modification(mock_config_dir: Path):
    m1 = CustomizationManifest.from_dir(mock_config_dir)
    # Mutate a rule file
    agents_path = mock_config_dir / "AGENTS.md"
    agents_path.write_text(agents_path.read_text(encoding="utf-8") + "\n# Extra Rule\n", encoding="utf-8")

    m2 = CustomizationManifest.from_dir(mock_config_dir)
    assert m1.sha256_root != m2.sha256_root
