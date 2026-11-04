Set WshShell = CreateObject("WScript.Shell")
Set FSO = CreateObject("Scripting.FileSystemObject")
WshShell.CurrentDirectory = FSO.GetParentFolderName(WScript.ScriptFullName)
WshShell.Run "python -u servir_feria.py", 0, False
WScript.Sleep 1000
WshShell.Run "http://127.0.0.1:8766/visita_virtual.html"
