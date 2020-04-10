SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.
Unz(sZip, sUnz) ;https://autohotkey.com/board/topic/60706-native-zip-and-unzip-xpvista7-ahk-l/
{
    fso := ComObjCreate("Scripting.FileSystemObject")
    If Not fso.FolderExists(sUnz)  ;http://www.autohotkey.com/forum/viewtopic.php?p=402574
       fso.CreateFolder(sUnz)
    psh  := ComObjCreate("Shell.Application")
    zippedItems := psh.Namespace( sZip ).items().count
    psh.Namespace( sUnz ).CopyHere( psh.Namespace( sZip ).items, 4|16 )
    Loop {
        sleep 50
        unzippedItems := psh.Namespace( sUnz ).items().count
        IfEqual,zippedItems,%unzippedItems%
            break
    }
}
full_command_line := DllCall("GetCommandLine", "str")
if not (A_IsAdmin or RegExMatch(full_command_line, " /restart(?!\S)"))
{
    try
    {
        if A_IsCompiled
            Run *RunAs "%A_ScriptFullPath%" /restart
        else
            Run *RunAs "%A_AhkPath%" /restart "%A_ScriptFullPath%"
    }
    ExitApp
}
Stop := 0
Nircmd := 0
While(Stop = 0)
{
MsgBox, 4, Audio Select, Use As Default Speaker Changer
IfMsgBox, Yes
{
Stop := 1
Speaker := 1
MsgBox, 4, Audio Select, Use As Communications Speaker Changer
IfMsgBox, Yes
{
Speaker1 := 1
Nircmd := 1
}
}
MsgBox, 4, Audio Select, Use As Default Microfon Changer
IfMsgBox, Yes
{
Stop := 1
Microfon := 1
MsgBox, 4, Audio Select, Use As Communications Microfon Changer
IfMsgBox, Yes
{
Microfon1 := 1
Nircmd := 1
}
}
If(Stop = 0)
MsgBox, 0, Audio Select, Please select something, 4
}
if(Nircmd = 1)
{
MsgBox, 4, Install, Install Nircmd?
IfMsgBox, Yes
{
http := ""
While(http = ""){
	InputBox, http, URL Downloader, Type url to nircmd`n the default should be fine, , 500, 160, , , , , https://www.nirsoft.net/utils/nircmd-x64.zip
	if(http = "")
		MsgBox, 0, URL Downloader, Please type something or use default, 4
}
sZip := A_ScriptDir "\Nircmd.zip"
sUnz := A_ScriptDir "\Nircmd"
UrlDownloadToFile, %http%, %sZip%
Unz(sZip,sUnz)
FileMove, %sUnz%\*.*, %A_ScriptDir% , 1
FileRemoveDir, %sUnz%
FileDelete, %sUnz%.zip
}
}
MsgBox, 4, Install, Install AudioDeviceCmdlets?
IfMsgBox, Yes
{
http := ""
While(http = ""){
	InputBox, http, URL Downloader, Type url to AudioDeviceCmdlets.dll`n the default should be fine, , 600, 160, , , , , https://github.com/frgnca/AudioDeviceCmdlets/releases/download/v3.0/AudioDeviceCmdlets.dll
	if(http = "")
		MsgBox, 0, URL Downloader, Please type something or use default, 4
}
UrlDownloadToFile, %http%, AudioDeviceCmdlets.dll
FileDelete, ImportAudioDeviceCmdlets.ps1
FileAppend, 
(
New-Item "$($profile | split-path)\Modules\AudioDeviceCmdlets" -Type directory -Force
Copy-Item "C:\Path\to\AudioDeviceCmdlets.dll" "$($profile | split-path)\Modules\AudioDeviceCmdlets\AudioDeviceCmdlets.dll"
Set-Location "$($profile | Split-Path)\Modules\AudioDeviceCmdlets"
Get-ChildItem | Unblock-File
Import-Module AudioDeviceCmdlets
), ImportAudioDeviceCmdlets.ps1
RunWait, Powershell -Command .\ImportAudioDeviceCmdlets.ps1, %A_ScriptDir%
FileDelete, ImportAudioDeviceCmdlets.ps1
FileDelete, AudioDeviceCmdlets.dll
}
FileDelete, Setaudio.ps1
FileAppend,
(
function Start-App($Nr){
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$form = New-Object System.Windows.Forms.Form
$form.Text = 'Data Entry Form'
$form.Size = New-Object System.Drawing.Size(300,200)
$form.StartPosition = 'CenterScreen'

$okButton = New-Object System.Windows.Forms.Button
$okButton.Location = New-Object System.Drawing.Point(75,120)
$okButton.Size = New-Object System.Drawing.Size(75,23)
$okButton.Text = 'OK'
$okButton.DialogResult = [System.Windows.Forms.DialogResult]::OK
$form.AcceptButton = $okButton
$form.Controls.Add($okButton)

$cancelButton = New-Object System.Windows.Forms.Button
$cancelButton.Location = New-Object System.Drawing.Point(150,120)
$cancelButton.Size = New-Object System.Drawing.Size(75,23)
$cancelButton.Text = 'Cancel'
$cancelButton.DialogResult = [System.Windows.Forms.DialogResult]::Cancel
$form.CancelButton = $cancelButton
$form.Controls.Add($cancelButton)

$label = New-Object System.Windows.Forms.Label
$label.Location = New-Object System.Drawing.Point(10,20)
$label.Size = New-Object System.Drawing.Size(280,20)
If ($Nr -eq 1){$label.Text = 'Enter wanted Default Speaker ID:'}
If ($Nr -eq 2){$label.Text = 'Enter wanted Communications Speaker Name:'}
If ($Nr -eq 3){$label.Text = 'Enter wanted Default Microfon ID:'}
If ($Nr -eq 4){$label.Text = 'Enter wanted Communications Microfon Name:'}
$form.Controls.Add($label)

$textBox = New-Object System.Windows.Forms.TextBox
$textBox.Location = New-Object System.Drawing.Point(10,40)
$textBox.Size = New-Object System.Drawing.Size(260,20)
$form.Controls.Add($textBox)

$form.Topmost = $true

$form.Add_Shown({$textBox.Select()})
$result = $form.ShowDialog()

if ($result -eq [System.Windows.Forms.DialogResult]::OK){$x = $textBox.Text}
return $x
}


$Script = $PSScriptRoot+"\"+(Get-Item $PSCommandPath ).Name
$INIPath = $PSScriptRoot+"\"+(Get-Item $PSCommandPath ).BaseName+".ini"


if(!(Test-Path $INIPath)){
Start-Process powershell -ArgumentList "-noexit -command ""Get-AudioDevice -List"""

), Setaudio.ps1

if(Speaker = 1)
FileAppend, 
(
$1 = $null
while(-NOT (($1) -OR ($1 -eq "f") -OR ($1 -eq " "))){$1 = Start-App -Nr "1"}

), Setaudio.ps1
else
FileAppend, 
(
$1 = "null"

), Setaudio.ps1
if(Speaker1 = 1)
FileAppend, 
(
$2 = $null
while(-NOT (($2) -OR ($2 -eq "f") -OR ($2 -eq " "))){$2 = Start-App -Nr "2"}

), Setaudio.ps1
else
FileAppend, 
(
$2 = "null"

), Setaudio.ps1
if(Microfon = 1)
FileAppend, 
(
$3 = $null
while(-NOT (($3) -OR ($3 -eq "f") -OR ($3 -eq " "))){$3 = Start-App -Nr "3"}

), Setaudio.ps1
else
FileAppend, 
(
$3 = "null"

), Setaudio.ps1
if(Microfon1 = 1)
FileAppend, 
(
$4 = $null
while(-NOT (($4) -OR ($4 -eq "f") -OR ($4 -eq " "))){$4 = Start-App -Nr "4"}

), Setaudio.ps1
else
FileAppend, 
(
$4 = "null"

), Setaudio.ps1
FileAppend,
(
$Trigger= New-ScheduledTaskTrigger -AtLogon # Specify the trigger settings
$Action= New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-windowstyle hidden '$Script'" # Specify what program to run and with its parameters
Register-ScheduledTask -TaskName "ForceDefaultAudio" -Trigger $Trigger -Action $Action -RunLevel Highest –Force # Specify the name of the task
Add-Content -Path $INIPath "Line 2 Playback Default Audio Device ID, Line 3 Playback Communications Audio Device Name, Line 4 Recording Default Audio Device ID, Line 5 Recording Communications Audio Device Name"
Add-Content -Path $INIPath $1
Add-Content -Path $INIPath $2
Add-Content -Path $INIPath $3
Add-Content -Path $INIPath $4
}

if(Test-Path $INIPath){
$AudioDevice_DP = (Get-Content -Path $INIPath -TotalCount 2)[-1]
$AudioDevice_CP = (Get-Content -Path $INIPath -TotalCount 3)[-1]
$AudioDevice_DR = (Get-Content -Path $INIPath -TotalCount 4)[-1]
$AudioDevice_CR = (Get-Content -Path $INIPath -TotalCount 5)[-1]
while(Test-Path $INIPath){
    $DefaultPlayback = Get-AudioDevice -Playback
    $DefaultRecording = Get-AudioDevice -Recording
	
), Setaudio.ps1
if(Speaker = 1)
FileAppend,
(
    If ($DefaultPlayback.ID -ne $AudioDevice_DP) {
		Set-AudioDevice -ID $AudioDevice_DP
		
), Setaudio.ps1
if(Speaker1 = 1)
FileAppend,
(
		Start-Process "nircmd.exe" "setdefaultsounddevice ``"$AudioDevice_CP``" 2"
		
), Setaudio.ps1
if(Speaker = 1)
FileAppend,
(
        $AudioDevice_DP = (Get-Content -Path $INIPath -TotalCount 2)[-1]
        $AudioDevice_CP = (Get-Content -Path $INIPath -TotalCount 3)[-1]
        Start-Sleep -Seconds 0.1
    }
	
), Setaudio.ps1
if(Microfon = 1)
FileAppend,
(
    If ($DefaultRecording.ID -ne $AudioDevice_DR) {
        Set-AudioDevice -ID $AudioDevice_DR
		
), Setaudio.ps1
if(Microfon1 = 1)
FileAppend,
(
        Start-Process "nircmd.exe" "setdefaultsounddevice ``"$AudioDevice_CR``" 2"
		
), Setaudio.ps1
if(Microfon = 1)
FileAppend,
(
        $AudioDevice_DR = (Get-Content -Path $INIPath -TotalCount 4)[-1]
        $AudioDevice_CR = (Get-Content -Path $INIPath -TotalCount 5)[-1]
        Start-Sleep -Seconds 0.1
    }
	
), Setaudio.ps1

FileAppend,
(
    Start-Sleep -Seconds 0.1
	}
}
), Setaudio.ps1
FileDelete, AudioList.bat
FileAppend,
(
start PowerShell.exe -noexit -command "Get-AudioDevice -List"
), AudioList.bat
Run, Powershell -windowstyle hidden -Command .\Setaudio.ps1, %A_ScriptDir%