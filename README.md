# Force Default Audiodevice (Python Update) --- Table Of Contents
- Script Info | L8 | Some info of the Script
- IMPORTANT | L22 | Important things to know when using thsi script
- Installation | L33 | The instalation of the script
- PARRAMETERS | L57 | Parrameters / Arguments to run with the script
- OPERATING SYSTEM | L68 | Info about Windows only support (no Mac and Linux support)

# Script Info | L8 
This Python script will use the nirsoft.net tool SoundVolumeView that ***ONLY WORKS ON WINDOWS*** to check and change the:
- default comunication playback audio device
- default playback audio device
- default comunication recording audio device
- default recording audio device       

to what you set it to if it is nessesery.

The Python script is unsing the librarys (only needed for the .py not the .exe):  
urllib.request, threading, zipfile, msvcrt, json, time, sys, os 

It also only uses the command line as input for if it needs to be deploied on a windows server.  

# IMPORTANT | L22
The new python script is ***NOT COMPATIBLE*** with the old autohotkey / powershell config files from versions before 1.0.   
Because of the dependency of the nirsoft.net tool SoundVolumeView it still ***ONLY WORKS ON WINDOWS***.     
Allways enter the ***number*** in ***front*** of the audio device you want to use.	    
The ***name*** or the ***id*** of the devices will spitt out an error.       
First time run it inside a emty folder where it can stay so it doesn't create a mess and is easy to find.  

To change the default audiodevices after setup delete,	     
"***INPUT_SCRIPT_NAME_HERE***-AudioDevices.json" (the default name is "Forceaudiodevice-AudioDevices.json").	          
You can also rename it or move it to use it later (for that to work just rename it back or move it back).	        

# Installation | L33
Download the newest:
- .zip (full project, unzib somewhere it can stay),
- .exe (easy script, place it somewhere it can stay), 
- .py (sorce code script, place it somewhere it can stay), 

by opening the releases section or open this link:     
https://github.com/marvin1099/Force_Audiodevice/releases  
When you run it in the next step,  
keep in mind to allways run it inside a the folder so the files wont replace anything as sayed in important.   
Run the ***INPUT_SCRIPT_NAME_HERE***.exe or ***INPUT_SCRIPT_NAME_HERE***.py it will ask you for:
- default playback and recording audio device (Here enter the numbers of what you want)
- - This can be left emty to skip, given only a speaker / microfon or given both
- default comunication playback and comunication recording audio device
- - This can be left emty to skip, given only a speaker / microfon or given both

After this change a audio device to something wrong and see if it changes to what you set it up for.

This will save the ***IDs*** of the speakers and / or microfons in to "***INPUT_SCRIPT_NAME_HERE***-AudioDevices.json",           
this can be canged while it is running by editing the path inside the "***INPUT_SCRIPT_NAME_HERE***-AudioDDesination.txt".         
both files can be switched while the script runs but if the:      
- "***INPUT_SCRIPT_NAME_HERE***-AudioDevices.json" is missing it will exit the script after 60 seconds if not replaced in that time
- "***INPUT_SCRIPT_NAME_HERE***-AudioDDesination.txt" is missing it will exit the script after 20 seconds if not replaced in that time

# PARRAMETERS | L57
Availible arguments are       
- 'help' to dsplay this in the commandline       
- 'exit' to only run the configuration and exit       
- Any argument that includes Soundvolumeview will be used as the Soundvolumeview file       
- Any argument that ends with 'json' or 'ini' will be used as the save location for the device config file")       
- Any argument that ends with 'txt' will be used to create a file.       
- - Inside of it you can change the device config file location.       
- - - It will aply while the programm runs.
                

# OPERATING SYSTEM | L68
This script could technically run on mac or linux but SoundVolumeView is windows only.       
Other operating systems will probably have a easyer way of doing this (linux will for shure).
