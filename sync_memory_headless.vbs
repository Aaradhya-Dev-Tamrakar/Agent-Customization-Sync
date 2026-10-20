Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

strScriptDir = fso.GetParentFolderName(WScript.ScriptFullName)
strPythonScript = strScriptDir & "\agent_customization_sync\sync_ecosystem_memory.py"

' Run python silently in the background (WindowStyle 0 = hidden, WaitOnReturn = false)
strCmd = "python """ & strPythonScript & """"
WshShell.Run strCmd, 0, False
