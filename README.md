# Force Default Audiodevice (Python Update V1.2) 
# Table of Contents
- Script Info | L10 | Some info of the Script
- IMPORTANT | L24 | Important things to know when using thsi script
- Installation | L39 | The instalation of the script
- ARGUMENTS | L65 | Parrameters / Arguments to run with the script
- CREATED FILES | 75 | Files that the script creates
- OPERATING SYSTEM | L90 | Info about Windows only support (no Mac and Linux support)

# Script Info | L10
This Python script will use the nirsoft.net tool SoundVolumeView (also vbs and the bat files) that ***ONLY WORKS ON WINDOWS*** to check and change the:
- default comunication playback audio device
- default playback audio device
- default comunication recording audio device
- default recording audio device       

To what you set it to if it is nessesery.

The Python script is unsing the librarys (only needed for the .py not the .exe):  
urllib.request, subprocess, zipfile, msvcrt, json, time, sys, os 

It also only uses the command line as input for if it needs to be deploied on a windows server.  

# IMPORTANT | L24
The new python script is ***NOT COMPATIBLE*** with the old autohotkey / powershell config files from versions before 1.0.   
Because of the dependency of the nirsoft.net tool SoundVolumeView (also the vbs and the bat files) it still ***ONLY WORKS ON WINDOWS***.     
Allways enter the ***number*** in ***front*** of the audio device you want to use.	    
The ***name*** or the ***id*** of the devices will spitt out an error.       
First time run it inside a emty folder where it can stay so it doesn't create a mess and is easy to find.  
Version 1.2 will be the last version in 1.x.   
Any future work will use a reworked version.      
This is far in the future if ever an update will be made.       
Right now this will be the final version.    

To change the default audiodevices after setup delete,	     
"***INPUT_SCRIPT_NAME_HERE***-AudioDevices.json" (the default name is "Forceaudiodevice-AudioDevices.json").	          
You can also rename it or move it to use it later (for that to work just rename it back or move it back later).	        

# Installation | L39
Download the newest:
- .zip (full project, unzib somewhere it can stay),
- .exe (easy script, place it somewhere it can stay), 
- .py (sorce code script, place it somewhere it can stay), 

by opening the releases section or open this link:     
https://github.com/marvin1099/Forceaudiodevice/releases     
When you run it in the next step,  
keep in mind to allways run it inside a the folder so the files won't replace anything as sayed in important.   
Run the ***INPUT_SCRIPT_NAME_HERE***.exe or ***INPUT_SCRIPT_NAME_HERE***.py it will ask you for:
- Default playback and recording audio device (Here enter the numbers of what you want)
- - This can be left emty to skip, given only a speaker / microfon or given both
- Default comunication playback and comunication recording audio device
- - This can be left emty to skip, given only a speaker / microfon or given both
- If you like to have a shorcut it in the statup folder 
- - If you say yes it wil start by itself when you start the pc

After this change a audio device to something wrong and see if it changes to what you set it up for.

This will save the ***IDs*** of the speakers and / or microfons in to "***INPUT_SCRIPT_NAME_HERE***-AudioDevices.json".           
This path can be canged while it is running by editing the path inside the "***INPUT_SCRIPT_NAME_HERE***-AudioDDesination.txt".         
Both files can be switched while the script runs but if the:      
- "***INPUT_SCRIPT_NAME_HERE***-AudioDevices.json" is missing it will exit the script after 60 seconds if not replaced in that time.
- "***INPUT_SCRIPT_NAME_HERE***-AudioDDesination.txt" is missing it will exit the script after 20 seconds if not replaced in that time.

# ARGUMENTS | L65
Availible arguments / parrameters are       
- 'help' to dsplay this in the commandline       
- 'exit' to only run the configuration and exit       
- Any argument that includes Soundvolumeview will be used as the Soundvolumeview file       
- Any argument that ends with 'json' or 'ini' will be used as the save location for the device config file       
- Any argument that ends with 'txt' will be used to create a file.       
- - Inside of it you can change the device config file location.       
- - - It will aply while the programm runs.
                
# CREATED FILES | L75
This script creates multiple files and a few temorary files:
- "***INPUT_SCRIPT_NAME_HERE***-AudioDevices.json" is where the script saves the ids of the audio devices.
- "***INPUT_SCRIPT_NAME_HERE***-AudioDDesination.txt" is where you can change the file path for the file above while the script runns.
- "***INPUT_SCRIPT_NAME_HERE***.vbs" is the file to start the script hidden.
- "SoundVolumeView.exe" is the tool that changes the audio devices and scans them.

Now the temporrary files (all of them will olny exist shortly):
- "SoundVolumeViewTemp.json" is the audio devices scan report file from SoundVolumeView.
- "CreateShortcut.vbs" is the file that creates the shortcut in the autostart folder.
- "input.bat" is the file that is used to grab user input with timeout.
- "pause.bat" is the file that is used to exit with any key or timeout.

All of these files will be inside the script directory if to specified otherwise.

# OPERATING SYSTEM | L90
This script could technically run on mac or linux but SoundVolumeView (also the vbs and the bat files) is windows only.       
Other operating systems will probably have a easyer way of doing this (linux will for shure).
