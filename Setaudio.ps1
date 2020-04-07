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

if(!(Test-Path .\AudioDevices1.txt)){
Start-Process powershell -ArgumentList "-noexit -command ""Get-AudioDevice -List"""
$1 = $null
while(-NOT (($1) -OR ($1 -eq "f") -OR ($1 -eq " "))){$1 = Start-App -Nr "1"}
$2 = $null
while(-NOT (($2) -OR ($2 -eq "f") -OR ($2 -eq " "))){$2 = Start-App -Nr "2"}
$3 = $null
while(-NOT (($3) -OR ($3 -eq "f") -OR ($3 -eq " "))){$3 = Start-App -Nr "3"}
$4 = $null
while(-NOT (($4) -OR ($4 -eq "f") -OR ($4 -eq " "))){$4 = Start-App -Nr "4"}
Add-Content -Path .\AudioDevices1.txt "Line 2 Playback Default Audio Device ID, Line 3 Playback Communications Audio Device Name, Line 4 Recording Default Audio Device ID, Line 5 Recording Communications Audio Device Name"
Add-Content -Path .\AudioDevices1.txt $1
Add-Content -Path .\AudioDevices1.txt $2
Add-Content -Path .\AudioDevices1.txt $3
Add-Content -Path .\AudioDevices1.txt $4
}

if(Test-Path .\AudioDevices1.txt){
$File = (Get-Content -Path .\AudioDevices1.txt -TotalCount 5)
Remove-Item .\AudioDevices1.txt
Add-Content -Path .\AudioDevices1.txt $File
$AudioDevice_DP = (Get-Content -Path .\AudioDevices1.txt -TotalCount 2)[-1]
$AudioDevice_CP = (Get-Content -Path .\AudioDevices1.txt -TotalCount 3)[-1]
$AudioDevice_DR = (Get-Content -Path .\AudioDevices1.txt -TotalCount 4)[-1]
$AudioDevice_CR = (Get-Content -Path .\AudioDevices1.txt -TotalCount 5)[-1]
$power = (Get-Content -Path .\AudioDevices1.txt -TotalCount 6)[-1]
if ($power -eq "PowerShell"){
     $File = (Get-Content -Path .\AudioDevices1.txt -TotalCount 5)
     Remove-Item .\AudioDevices1.txt
     Add-Content -Path .\AudioDevices1.txt $File
     Start-Process powershell -ArgumentList "-noexit -command ""Get-AudioDevice -List"""
}
while(Test-Path .\AudioDevices1.txt){
    $DefaultPlayback = Get-AudioDevice -Playback
    $DefaultRecording = Get-AudioDevice -Recording

    If ($DefaultPlayback.ID -ne $AudioDevice_DP) {
        $power = (Get-Content -Path .\AudioDevices1.txt -TotalCount 6)[-1]
        if ($power -eq "PowerShell"){
            $File = (Get-Content -Path .\AudioDevices1.txt -TotalCount 5)
            Remove-Item .\AudioDevices1.txt
            Add-Content -Path .\AudioDevices1.txt $File
            Start-Process powershell -ArgumentList "-noexit -command ""Get-AudioDevice -List"""
        }
        Set-AudioDevice -ID $AudioDevice_DP
        Start-Process "nircmd.exe" "setdefaultsounddevice `"$AudioDevice_CP`" 2"
        $AudioDevice_DP = (Get-Content -Path .\AudioDevices1.txt -TotalCount 2)[-1]
        $AudioDevice_CP = (Get-Content -Path .\AudioDevices1.txt -TotalCount 3)[-1]
        Start-Sleep -Seconds 0.1
    }
    If ($DefaultRecording.ID -ne $AudioDevice_DR) {
        $power = (Get-Content -Path .\AudioDevices1.txt -TotalCount 6)[-1]
        if ($power -eq "PowerShell"){
            $File = (Get-Content -Path .\AudioDevices1.txt -TotalCount 5)
            Remove-Item .\AudioDevices1.txt
            Add-Content -Path .\AudioDevices1.txt $File
            Start-Process powershell -ArgumentList "-noexit -command ""Get-AudioDevice -List"""
        }
        Set-AudioDevice -ID $AudioDevice_DR
        Start-Process "nircmd.exe" "setdefaultsounddevice `"$AudioDevice_CR`" 2"
        $AudioDevice_DR = (Get-Content -Path .\AudioDevices1.txt -TotalCount 4)[-1]
        $AudioDevice_CR = (Get-Content -Path .\AudioDevices1.txt -TotalCount 5)[-1]
        Start-Sleep -Seconds 0.1
    }
    Start-Sleep -Seconds 0.1
}
}
