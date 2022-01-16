Function FileExists(FilePath)
  Set fso = CreateObject("Scripting.FileSystemObject")
  If fso.FileExists(FilePath) Then
    FileExists=CBool(1)
  Else
    FileExists=CBool(0)
  End If
End Function

Dim WShell
Set WShell = CreateObject("WScript.Shell")
File = CreateObject("Scripting.FileSystemObject").GetBaseName(WScript.ScriptName) 
If FileExists(File & ".exe") Then
	WShell.Run File & ".exe", 0 
ElseIf FileExists(File & ".py") Then
	WShell.Run File & ".py", 0 
Else
	WScript.Echo "Error File '" & File & ".exe' Or '" & File & ".py' Does No Exist Exiting"
End If
Set WShell = Nothing