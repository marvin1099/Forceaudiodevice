import urllib.request
import subprocess
import zipfile
import msvcrt
import json
import time
import sys
import os

def Pathsplit(PathToSplit):
    """
    Splits a fullpath in to: dir, slash, file, dot, ext
    and returns it as a list
        for example: Pathsplit("/test/file/here/text.txt")
            will return: ["/test/file/here","/","text",".","txt"]
    """
    if PathToSplit == "\\":
        PathToSplit = ""
    FullPath = os.path.realpath(PathToSplit)
    Directory = os.path.dirname(FullPath)
    FileName = os.path.basename(FullPath)
    Shlash = FullPath[len(Directory)]
    NamePlusExt = list(os.path.splitext(FileName))
    Name = NamePlusExt[0]
    if len(NamePlusExt[1]) == 0:
        Dot = ""
        Ext = ""
    elif len(NamePlusExt[1]) == 1:
        Dot = NamePlusExt[1]
        Ext = ""
    else:
        Dot = NamePlusExt[1][0]
        Ext = NamePlusExt[1][1:]
    SplitList = [Directory,Shlash,Name,Dot,Ext]
    return SplitList #Splits Path into its cotents

def Connectlisttostr(CombindeList,PartsToCombinde = []):
    """
    Combindes parts of a list that you speify in the second list with text or not into a string which it returns
    first imput a list that you want to have as a string
    than give it all the numbers for witch item you want to use (-1 uses the last Entry)
        for example: Connectlisttostr(["this","is","the,"first","list"],[0," ",1," ",2," ",3," ",-1," or is it"])
            will return: "this is the first list or is it"
    """
    EndStr = ""
    for i in PartsToCombinde:
        if str(type(i)) == "<class 'int'>":
            if i < 0:
                i = len(CombindeList)+i
            for a in range(len(CombindeList)):
                if i == a:
                    EndStr = EndStr + CombindeList[a]
        else:
            EndStr = EndStr + str(i)
    if PartsToCombinde == []:
        for a in CombindeList:
            if EndStr == "":
                EndStr = a
            else:
                EndStr = EndStr + a
    return EndStr #Connects a list to a string based on the second list given

def InputTimeout(caption = "\\/\\/\\/",Timeout = 5, default = ""):
    InputFile = "input.bat"
    if not os.path.exists(InputFile):
        f = open(InputFile, "w")
        s = '@echo off\nset /p id=""\necho %id%'
        f.write(s)
        f.close()
    print(caption)
    try:
        retu = subprocess.run(InputFile, stdout=subprocess.PIPE, timeout=Timeout)
        retu = str(retu.stdout)[2:][:-5].replace("ECHO is off.","",1)
    except:
        retu = ""
    if os.path.exists(InputFile):
        os.remove(InputFile)
    if retu == "":
        return default
    else:
        return retu

def Start(Cmd,Args = "",Wait = False):
    """
    Starts programms an example is:
        Start("cmd"," /c echo hi", True)
    This will start "cmd",
    with the argumets " /c echo hi" and
    it will wait
    """
    if Wait == True:
        FullCmd = Cmd + " " + Args
        try:
            subprocess.run(FullCmd, stdout=subprocess.PIPE)
        except:
            pass
    else:
        if Args == "" or Args == None:
            Args == " "
        try:
            os.spawnl(os.P_DETACH, Cmd, Args)
        except:
            pass
    return #Starts Programms

def DownloadFromULR(url,itime = 5,TargetFileList = Pathsplit("DownFile"),DownloadError = "Error Downloading Type New Url\n\\/\\/\\/ ",DownloadTime = 10,FilesToDelete = []):
    """
    Downloads a file from a url and Unzips it if the Given file ends with zip
    """
    SoundVVZipPa = Connectlisttostr(TargetFileList)
    while url != "":
        try:
            urllib.request.urlretrieve(url, SoundVVZipPa)
        except:
            if itime == 0:
                nurl = InputTimeout(DownloadError,DownloadTime)
                if nurl == "":
                    print("No Url Given Exiting")
                    ExitWait(20)
                else:
                    itime = 5
                    url = nurl
        else:
            url = ""
        itime -= 1
    if TargetFileList[-1] == "zip":
        Unzip(SoundVVZipPa,TargetFileList[0] + TargetFileList[1])
        os.remove(SoundVVZipPa)
    if type(FilesToDelete) == type([]):
        for i in FilesToDelete:
            e = TargetFileList[0] + Connectlisttostr(Pathsplit(i),[1,2,3,4])
            if os.path.exists(e):
                os.remove(e)
            elif os.path.exists(i):
                os.remove(i)
    return #Downloads a file from a url and Unzips it if the Given file ends with zip

def Unzip(zip,dir):
    try:
        with zipfile.ZipFile(zip) as z:
            z.extractall(dir)
    except:
        print("Invalid File To Extract Exiting")
        ExitWait(20)
    return #Unzips a zip file to taget directory

def ExitWait(Time = 60,ExitCode = ""):
    if ExitCode == "":
        ExitCode = None
    else:
        try:
            if Time == "":
                Time = 0
            else:
                Time = int(Time)
            ExitCode = int(ExitCode)
        except:
            print("The Exit Code And The Wait Time Can Only Be An Intenger Or An Empty String")
            ExitCode = None
    pausefile = "pause.bat"
    if not os.path.exists(pausefile):
        f = open(pausefile, "w")
        s = '@echo off\npause'
        f.write(s)
        f.close()
    try:
        subprocess.run(pausefile, timeout=Time)
    except:
        pass
    os.remove(pausefile)
    sys.exit(ExitCode)

def main():
    Args = sys.argv
    Script = Pathsplit(Args[0])
    Args.pop(0)
    Hiddenvbs = Script[0] + Script[1] + Script[2] + ".vbs"
    if not os.path.exists(Hiddenvbs):
        f = open(Hiddenvbs, "w")
        s = '''\
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
Set WShell = Nothing\
        '''
        f.write(s)
        f.close()
    Vexit = 0
    SoundVolumeViewSp = Pathsplit("SoundVolumeView")
    AudioDeviceFileSp = Pathsplit(Script[2] + "-AudioDevices.json")
    AudioDDFileSp = Pathsplit(Script[2] + "-AudioDDesination.txt")
    DefaultNames = ["Default Speaker","Default Microfon","Default Communication Speaker","Default Communication Microfon"]
    print("Script Started\nReading Arguments\n")
    if Args:
        for i in Args:
            PathList = Pathsplit(i)
            if PathList[2] == SoundVolumeViewSp[2]:
                SoundVolumeViewSp = PathList
            elif PathList[4] == "json":
                AudioDeviceFileSp = PathList
            elif PathList[4] == "ini":
                AudioDeviceFileSp = PathList
            elif PathList[4] == "txt":
                AudioDDFileSp = PathList
            elif i == "Exit" or i == "exit":
                Vexit = 1
            elif i == "Help" or i == "help":
                print("Availible Arguments Are")
                print("  'help' For This List")
                print("  'exit' To Only Run The Configuration And Exit")
                print("  Any Argument That Includes '" + SoundVolumeViewSp[2] + "' Will Be Used As The '" + SoundVolumeViewSp[2] + "' File")
                print("  Any Argument That Ends With 'json' or 'ini' Will Be Used As The Save Location For The Device Config File")
                print("  Any Argument That Ends With 'txt' Will Be Used To Create A File,\n   Inside Of It You Can Change The Device Config File Location\n    It Will Aply While The Programm Runs")
                ExitWait(40)
    print("Add 'help' As Argument To Show A List Of Availible Arguments")
    AudioDDFilePa = Connectlisttostr(AudioDDFileSp)
    SoundVolumeViewPa = Connectlisttostr(SoundVolumeViewSp)
    AudioDeviceFilePa = Connectlisttostr(AudioDeviceFileSp)

    VVJsonSp = Pathsplit("SoundVolumeViewTemp.json")
    VVJsonPa = Connectlisttostr(VVJsonSp)
    print("Starting " + SoundVolumeViewSp[2] + " With The Argument To Create A Json File")
    if os.path.exists(SoundVolumeViewPa):
        Start(SoundVolumeViewPa,'/sjson "' + VVJsonPa + '"',True)
    else:
        print("")
        Start(SoundVolumeViewSp[2],'/sjson "' + VVJsonPa + '"',True)
        print("")
    if not os.path.exists(VVJsonPa):
        SoundVVZipSp = Pathsplit("SoundVolumeViewTemp.zip")
        Url = "https://www.nirsoft.net/utils/soundvolumeview-x64.zip"
        DownloadFromULR(Url,5,SoundVVZipSp,"Type The URL For The Nirsoft Soundvolumeview Zib\n\tThe Default Url Didn't Work It Was:\n\t\t" + Url + "\nLeave Empty To Exit\n",20,[Connectlisttostr(SoundVVZipSp,[0,1]) + "readme.txt",Connectlisttostr(SoundVVZipSp,[0,1]) + "SoundVolumeView.chm"])
        Start(SoundVolumeViewSp[2],"/sjson " + VVJsonPa,True)
    if not os.path.exists(VVJsonPa):
        print("Error SoundVolumeView Missing")
        ExitWait(20)
    f = open(VVJsonPa, encoding='UTF-16')
    try:
        ConfigJson = json.load(f)
    except:
        f.close()
        os.remove(VVJsonPa)
        print("Error SoundVolumeView Json Missing")
        ExitWait(20)
    else:
        f.close()
        os.remove(VVJsonPa)
    print("Checking For Config File")
    if not os.path.exists(AudioDeviceFilePa):
        AudioDevicesS = []
        AudioDevicesR = []
        AudioDNRS = 0
        AudioDNRR = 0
        for i in range(len(ConfigJson)):
            if ConfigJson[i]["Type"] == "Device" and ConfigJson[i]["Direction"] == "Render":
                AudioDevicesS.append([AudioDNRS,ConfigJson[i]["Device Name"] + " (" + ConfigJson[i]["Name"] + ")",ConfigJson[i]["Item ID"],str("D" if ConfigJson[i]["Default"] != "" else " ") + str("C" if ConfigJson[i]["Default Communications"] != "" else " "),""])
                AudioDNRS += 1
            elif ConfigJson[i]["Type"] == "Device":
                AudioDevicesR.append([AudioDNRR,ConfigJson[i]["Device Name"] + " (" + ConfigJson[i]["Name"] + ")",ConfigJson[i]["Item ID"],str("D" if ConfigJson[i]["Default"] != "" else " ") + str("C" if ConfigJson[i]["Default Communications"] != "" else " "),""])
                AudioDNRR += 1

        for i in range(0,len(AudioDevicesR)):
            AudioDevicesR[i][0] = AudioDevicesR[i][0] + AudioDNRS
        print("\nNo Config File Found Input The Defaut Devices You Like From The Following List")
        Unvalid = [100,0]
        DefNumTimeout = 60
        while Unvalid[0] > 0:
            print("\tSpeakers")
            for i in AudioDevicesS:
                print(str(i[0]) + " " + i[3] + " : " + i[1])
            print("\n\tMicrofons")
            for i in AudioDevicesR:
                print(str(i[0]) + " " + i[3] + " : " + i[1])
            DefD = ["",""]
            DefC = ["",""]
            DefD = InputTimeout("Input The Device Nummbers That Shold Be Used As Default (Separated By Kommas E.G. 1,4)\n\\/\\/\\/",DefNumTimeout).split(",") + [""]
            DefC = InputTimeout("Input The Device Nummbers That Shold Be Used As Default Communications (Separated By Kommas E.G. 3,10)\n\\/\\/\\/",DefNumTimeout).split(",") + [""]
            Unvalid[1] = 0
            try:
                if DefD[0] != "":
                    DefD[0] = int(DefD[0])
                if DefD[1] != "":
                    DefD[1] = int(DefD[1])
                if DefC[0] != "":
                    DefC[0] = int(DefC[0])
                if DefC[1] != "":
                    DefC[1] = int(DefC[1])
            except:
                print(DefD + DefC)
                Unvalid[1] = "Error Please Only Type Hole Numbers from 0 to " + str(int(AudioDNRS+AudioDNRR-1))
            if Unvalid[1] != 0:
                print(Unvalid[1])
                Unvalid[0] -= 1
                if Unvalid[0] == 1:
                    print("Error User Could Not Input Valid Nummbers")
                    ExitWait(20)
            else:
                if DefD[0] != "":
                    if DefD[0] < int(AudioDNRS+AudioDNRR) and DefD[0] > -1:
                        pass
                    else:
                        Unvalid[1] = "The Given Input Is Not In Range from 0 to " + str(int(AudioDNRS+AudioDNRR-1))
                if DefD[1] != "":
                    if DefD[1] < int(AudioDNRS+AudioDNRR) and DefD[1] > -1:
                        if DefD[0] != "" and DefD[0] > AudioDNRS-1 and DefD[1] > AudioDNRS-1:
                            Unvalid[1] = "The To Inputs Are Both Microfons Please Select Only One"
                        elif DefD[0] != "" and DefD[0] < AudioDNRS and DefD[1] < AudioDNRS:
                            Unvalid[1] = "The To Inputs Are Both Speakers Please Select Only One"
                    else:
                        Unvalid[1] = "The Given Input Is Not In Range from 0 to " + str(int(AudioDNRS+AudioDNRR-1))
                if DefC[0] != "":
                    if DefC[0] < int(AudioDNRS+AudioDNRR) and DefC[0] > -1:
                        pass
                    else:
                        Unvalid[1] = "The Given Input Is Not In Range from 0 to " + str(int(AudioDNRS+AudioDNRR-1))
                if DefC[1] != "":
                    if DefC[1] < int(AudioDNRS+AudioDNRR) and DefD[1] > -1:
                        if DefC[0] != "" and DefC[0] > AudioDNRS-1 and DefC[1] > AudioDNRS-1:
                            Unvalid[1] = "The To Inputs Are Both Microfons Please Select Only One"
                        elif DefC[0] != "" and DefC[0] < AudioDNRS and DefC[1] < AudioDNRS:
                            Unvalid[1] = "The To Inputs Are Both Speakers Please Select Only One"
                    else:
                        Unvalid[1] = "The Given Input Is Not In Range from 0 to " + str(int(AudioDNRS+AudioDNRR-1))
                if Unvalid[1] != 0:
                    print(Unvalid[1])
                    Unvalid[0] -= 1
                    if Unvalid[0] == 1:
                        print("Error User Could Not Input Valid Nummbers")
                        ExitWait(20)
                else:
                    DefaultList = [DefD[0],DefD[1],DefC[0],DefC[1],""]
                    if DefaultList[0] != "" and DefaultList[0] > AudioDNRS-1:
                        DefaultList[4] = DefaultList[0]
                        DefaultList[0] = DefaultList[1]
                        DefaultList[1] = DefaultList[4]
                    if DefaultList[2] != "" and DefaultList[2] > AudioDNRS-1:
                        DefaultList[4] = DefaultList[2]
                        DefaultList[2] = DefaultList[3]
                        DefaultList[3] = DefaultList[4]
                    if DefaultList[1] != "" and DefaultList[1] < AudioDNRS:
                        DefaultList[0] = DefaultList[1]
                        DefaultList[1] = ""
                    if DefaultList[3] != "" and DefaultList[3] < AudioDNRS:
                        DefaultList[2] = DefaultList[3]
                        DefaultList[3] = ""
                    DefaultList[4] = ""
                    DefaultList[4] = -3
                    for i in DefaultList:
                        if i == "":
                            DefaultList[4] += 1
                    if DefaultList[4] < 1:
                        Unvalid[0] = 0
                    else:
                        Unvalid[0] -= 1
                        if Unvalid[0] == 1:
                            print("Error User Could Not Input Valid Nummbers")
                            ExitWait(20)
                        print("No Audio Devices Where Set Asking Again")
                    DefaultList.pop(4)
                if Unvalid[0] == 0:
                    for i in AudioDevicesS:
                        if i[0] == DefaultList[0]:
                            DefaultList[0] = i[2]
                            print("Using Default Speaker " + str(i[0]) + " : " + i[1] + "\n\tID: " + i[2])
                        if i[0] == DefaultList[2]:
                            DefaultList[2] = i[2]
                            print("Using Default Communication Speaker " + str(i[0]) + " : " + i[1] + "\n\tID: " + i[2])
                    for i in AudioDevicesR:
                        if i[0] == DefaultList[1]:
                            DefaultList[1] = i[2]
                            print("Using Default Microfon " + str(i[0]) + " : " + i[1] + "\n\tID: " + i[2])
                        if i[0] == DefaultList[3]:
                            DefaultList[3] = i[2]
                            print("Using Default Communication Microfon " + str(i[0]) + " : " + i[1] + "\n\tID: " + i[2])
        Save = {
            DefaultNames[0]:DefaultList[0],
            DefaultNames[1]:DefaultList[1],
            DefaultNames[2]:DefaultList[2],
            DefaultNames[3]:DefaultList[3]
        }
        f = open(AudioDeviceFilePa, 'w')
        json.dump(Save, f, sort_keys=False, indent=4, separators=(',', ': '))
        f.close()
        Startup = os.path.expanduser('~\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup')
        if os.path.exists(Startup):
            Shortcut = Script[1] + Script[2]
            StartupShortcut = Startup + Shortcut + ".lnk"
            if not os.path.exists(StartupShortcut):
                Shortnow = str(InputTimeout("You Like To Create Autostart Shortcut In '" + Startup + "'?\nY/N \\/\\/\\/",Timeout = 20, default = " ") + " ")[0]
                if Shortnow == "Y" or Shortnow == "y":
                    ShortScript = Script[0] + Script[1] + "CreateShortcut.vbs"
                    f = open(ShortScript, "w")
                    s = 'Set objShell = WScript.CreateObject("WScript.Shell")\nSet objShortCut = objShell.CreateShortcut("' + StartupShortcut + '")\nobjShortCut.TargetPath = "' + Hiddenvbs + '"\nobjShortCut.Description = "Run Force Audio Hidden"\nobjShortCut.WorkingDirectory = "' + Script[0] + Script[1] + '"\nobjShortCut.Save'
                    f.write(s)
                    f.close()
                    os.system(ShortScript)
                    os.remove(ShortScript)
                    print("Placed Shortcut In Autostart Folder\n")
                else:
                    print("")
    if os.path.exists(SoundVolumeViewPa):
        UseSVPA = True
    else:
        UseSVPA = False
    if Vexit == 1:
        ExitWait(20)
    f = open(AudioDDFilePa,"w")
    f.write(AudioDeviceFilePa)
    f.close()
    print("All Checks Successful Continuing\nStarting Audio Device Loop\n")
    while True:
        if os.path.exists(AudioDDFilePa):
            f = open(AudioDDFilePa,"r")
            AudioDeviceFileDest = Connectlisttostr(f.readlines()).replace("\n","")
            AudioDeviceFilePa = Connectlisttostr(Pathsplit(AudioDeviceFileDest))
            f.close()
        else:
            filetimeout = 20
            while not os.path.exists(AudioDDFilePa):
                if filetimeout == 0:
                    print("Audio Devices Json File Still Missing Exiting")
                    ExitWait(20)
                print('Audio Devices Json Config txt File Missing ("' + AudioDDFilePa + '")\nWaiting For ' + str(filetimeout) + " Seconds For It To Reapear")
                filetimeout -= 1
                time.sleep(1)
        if os.path.exists(AudioDeviceFilePa):
            f = open(AudioDeviceFilePa, 'r')
            try:
                Save = json.load(f)
            except:
                f.close()
                os.remove(AudioDeviceFilePa)
                print("Error AudioDeviceFile Json Damaged Deleting")
                ExitWait(20)
            else:
                f.close()
        else:
            filetimeout = 60
            while not os.path.exists(AudioDeviceFilePa):
                if filetimeout == 0:
                    print("Audio Devices Json File Still Missing Exiting")
                    ExitWait(20)
                print('Audio Devices Json File Missing ("' + AudioDeviceFilePa + '")\nWaiting For ' + str(filetimeout) + " Seconds For It To Reapear")
                filetimeout -= 1
                time.sleep(1)
        DevicesGo = ["","","",""]
        for i in Save:
            for e in range(len(DefaultNames)):
                if i == DefaultNames[e]:
                    DevicesGo[e] = str(Save[i])
        if UseSVPA:
            Start(SoundVolumeViewPa,'/sjson "' + VVJsonPa + '"',True)
        else:
            Start(SoundVolumeViewSp[2],'/sjson "' + VVJsonPa + '"',True)
        if not os.path.exists(VVJsonPa):
            print("Error SoundVolumeView Missing")
            ExitWait(20)
        f = open(VVJsonPa, encoding='UTF-16')
        try:
            ConfigJson = json.load(f)
        except:
            f.close()
            os.remove(VVJsonPa)
            print("Error SoundVolumeView Json Missing")
            ExitWait(20)
        else:
            f.close()
            os.remove(VVJsonPa)
        AudioDevIDs = []
        for i in range(len(ConfigJson)):
            if ConfigJson[i]["Type"] == "Device" and ConfigJson[i]["Direction"] == "Render":
                AudioDevIDs.append([ConfigJson[i]["Item ID"],str("D" if ConfigJson[i]["Default"] != "" else " ") + str("C" if ConfigJson[i]["Default Communications"] != "" else " "),""])
            elif ConfigJson[i]["Type"] == "Device":
                AudioDevIDs.append([ConfigJson[i]["Item ID"],str("D" if ConfigJson[i]["Default"] != "" else " ") + str("C" if ConfigJson[i]["Default Communications"] != "" else " "),""])
        for i in range(len(DevicesGo)):
            if DevicesGo[i] != "":
                if i == 0 or i == 1:
                    for e in AudioDevIDs:
                        if e[0] == DevicesGo[i] and e[1][0] == " ":
                            if UseSVPA:
                                print(SoundVolumeViewPa + ' /SetDefault "' + DevicesGo[i] + '" 0')
                                Start(SoundVolumeViewPa,'/SetDefault "' + DevicesGo[i] + '" 0',True)
                            else:
                                print(SoundVolumeViewSp[2] + ' /SetDefault "' + DevicesGo[i] + '" 0')
                                Start(SoundVolumeViewSp[2],'/SetDefault "' + DevicesGo[i] + '" 0',True)
                elif i == 2 or i == 3:
                    for e in AudioDevIDs:
                        if e[0] == DevicesGo[i] and e[1][1] == " ":
                            if UseSVPA:
                                print(SoundVolumeViewPa + ' /SetDefault "' + DevicesGo[i] + '" 2')
                                Start(SoundVolumeViewPa,'/SetDefault "' + DevicesGo[i] + '" 2',True)
                            else:
                                print(SoundVolumeViewSp[2] + ' /SetDefault "' + DevicesGo[i] + '" 2')
                                Start(SoundVolumeViewSp[2],'/SetDefault "' + DevicesGo[i] + '" 2',True)
        time.sleep(1)

if __name__ == "__main__": #Start ForceAudioDevice if not imported
    main()
else:
    pass #print("to start use:\n" + __name__ + ".main()")
