# Force Default Audiodevice (Python Update)
This Python script will use the nirsoft.net tool SoundVolumeView to check:
- default comunication playback audio device
- default playback audio device
- default comunication recording audio device
- default recording audio device       

And change it to what you set it to if it is nessesery.

The Python script is unsing the librarys (only needed for the .py not the .exe):  
urllib.request, threading, zipfile, msvcrt, json, time, sys, os 

It also only uses the command line as input for if it needs to be deploied on a windows server.  

# IMPORTANT
Allways enter the ***number*** in ***front*** of the audio device you want to use.	    
The ***name*** or the ***id*** of the devices will spitt out an error.	    
To change the default audiodevices after setup delete,	     
"***INPUT_SCRIPT_NAME_HERE***-AudioDevices.json" (the default name is "Forceaudiodevice-AudioDevices.json").	          
You can also rename it or move it to use it later (for that to work just rename it back or move it back).	        

# Installation
Download the newest:
- .zip (full project, Unzib somewhere it can stay),
- .exe and .vbs (esay script and script to start it hidden, move somewhere it can stay), 
- .py and .vbs (sorce coce script and script to start it hidden, move somewhere it can stay), 

by opening the releases section or open this link:     
https://github.com/marvin1099/Force_Audiodevice/releases  
When you run it in the next step,  
run it inside a folder so it doesn't create a mess.   
Run the ***INPUT_SCRIPT_NAME_HERE***.exe or ***INPUT_SCRIPT_NAME_HERE***.py it will ask you for:
- default playback and recording audio device (Here enter the numbers of what you want)
- - This can be left emty to skip or given only a speaker / microfon or given both
- default comunication playback and comunication recording audio device
- - This can be left emty to skip or given only a speaker / microfon or given both

This will save the ***IDs*** of the speakers and / or microfons in to "***INPUT_SCRIPT_NAME_HERE***-AudioDevices.json",           
this can be canged while it is running by editing the path inside the "***INPUT_SCRIPT_NAME_HERE***-AudioDDesination.txt".         
both files can be switched while the script runs but if the:      
- "***INPUT_SCRIPT_NAME_HERE***-AudioDevices.json" is missing it will exit the script after 60 seconds if not replaced in that time
- "***INPUT_SCRIPT_NAME_HERE***-AudioDDesination.txt" is missing it will exit the script after 20 seconds if not replaced in that time
