Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

strScriptDir = fso.GetParentFolderName(WScript.ScriptFullName)
strDaemonScript = strScriptDir & "\agent_customization_sync\memory_watcher_daemon.py"

' Run watcher daemon completely hidden in the background (WindowStyle 0 = hidden, WaitOnReturn = false)
strCmd = "python """ & strDaemonScript & """"
WshShell.Run strCmd, 0, False
