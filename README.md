# Force Default Audiodevice
This powershell script will change your default playback and recording audio device to the one you want

# IMPORTANT
When it ask you for a ***ID*** for the playback or recording default device,  
just copy the id field from the the wanted audio device

When it ask you for a ***NAME*** for the playback or recording communication device,  
only copy the name ***BEFORE*** the brackets

# Installation
Required is AudioDeviceCmdlets which is a audio managing libary for Powershell  
https://github.com/frgnca/AudioDeviceCmdlets

The main version of this script requires nircmd ***IN THE SAME FOLDER AS THE SCRIPT OR AS A SYSTEM VARIABLE*** to change the communicatinos device  
https://www.nirsoft.net/utils/nircmd-x64.zip

# Working
Still working an auto installer   
You want to run it add this to the Task Scheduler:   
- add trigger for on system start  
- select run with highest privileges 
- select run wehether user is loged on
- select do not store password
- add run a progamm in actions with this:  
  - script: C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe  
  - argument: -windowstyle hidden .\Setaudio.ps1   
  - start in: ***YOUR SCRIPT PATH***   
