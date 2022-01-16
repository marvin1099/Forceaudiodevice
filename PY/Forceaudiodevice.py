import urllib.request
import threading
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

def InputTimeout(caption = "\\/\\/\\/ ",timeout = 5, default = ""):
    class KeyboardThread(threading.Thread):
        def run(self):
            self.timedout = False
            self.input = ''
            print(caption)
            while True:
                if msvcrt.kbhit():
                    chr = msvcrt.getche()
                    if ord(chr) == 13:
                        break
                    elif ord(chr) >= 32:
                        self.input += str(chr)[2]
                if len(self.input) == 0 and self.timedout:
                    break

    #sys.stdout.write('%s'%(caption));
    result = default
    it = KeyboardThread()
    it.start()
    it.join(timeout)
    it.timedout = True
    if len(it.input) > 0:
        #wait for rest of input
        it.join()
        result = it.input
    print("")  # needed to move to next line
    return result

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
            os.system(FullCmd)
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

def DownloadFromULR(url,itime = 5,TargetFileList = Pathsplit("DownFile"),DownloadError = "Error Downloading Type New Url\n>>> ",DownloadTime = 10):
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
                    ExitWait(60)
                else:
                    itime = 5
                    url = nurl
        else:
            url = ""
        itime -= 1
    if TargetFileList[-1] == "zip":
        Unzip(SoundVVZipPa,TargetFileList[0] + TargetFileList[1])
        os.remove(SoundVVZipPa)
    return #Downloads a file from a url and Unzips it if the Given file ends with zip

def Unzip(zip,dir):
    try:
        with zipfile.ZipFile(zip) as z:
            z.extractall(dir)
    except:
        print("Invalid File To Extract Exiting")
        ExitWait(60)
    return #Unzips a zip file to taget directory

def ExitWait(Time = 120,ExitCode = ""):
    if ExitCode == "":
        ExitCode = None
    else:
        try:
            ExitCode = int(ExitCode)
        except:
            print("The Exit Code Can Only Be An Intenger Or An Empty String")
            ExitCode = None
    print("")
    try:
        InputTimeout("Push Enter To Exit ", Time)
    except:
        pass
    exit(ExitCode)

def main():
    Args = sys.argv
    Script = Pathsplit(Args[0])
    Args.pop(0)
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
                ExitWait()
    print("Add 'help' As Argument To Show A List Of Availible Arguments")
    AudioDDFilePa = Connectlisttostr(AudioDDFileSp)
    SoundVolumeViewPa = Connectlisttostr(SoundVolumeViewSp)
    AudioDeviceFilePa = Connectlisttostr(AudioDeviceFileSp)

    VVJsonSp = Pathsplit("SoundVolumeViewTemp.json")
    VVJsonPa = Connectlisttostr(VVJsonSp)
    print("Starting " + SoundVolumeViewSp[2] + " With The Argument To Create A Json File")
    Start(SoundVolumeViewSp[2],'/sjson "' + VVJsonPa + '"',True)
    if not os.path.exists(VVJsonPa):
        Start(SoundVolumeViewPa,'/sjson "' + VVJsonPa + '"',True)
    print("\n\n")
    if not os.path.exists(VVJsonPa):
        SoundVVZipSp = Pathsplit("SoundVolumeViewTemp.zip")
        Url = "https://www.nirsoft.net/utils/soundvolumeview-x64.zip"
        DownloadFromULR(Url,5,SoundVVZipSp,"Type The URL For The Nirsoft Soundvolumeview Zib\n\tThe Default Url Didn't Work It Was:\n\t\t" + Url + "\nLeave Empty To Exit\n",20)
        Start(SoundVolumeViewSp[2],"/sjson " + VVJsonPa,True)
    if not os.path.exists(VVJsonPa):
        print("Error SoundVolumeView Missing")
        ExitWait(60)
    f = open(VVJsonPa, encoding='UTF-16')
    try:
        ConfigJson = json.load(f)
    except:
        f.close()
        os.remove(VVJsonPa)
        print("Error SoundVolumeView Json Missing")
        ExitWait(60)
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
        print("\tSpeakers")
        for i in AudioDevicesS:
            print(str(i[0]) + " " + i[3] + " : " + i[1])
        print("\n\tMicrofons")
        for i in AudioDevicesR:
            print(str(i[0]) + " " + i[3] + " : " + i[1])
        Unvalid = [100,0]
        DefNumTimeout = 20
        while Unvalid[0] > 0:
            DefD = ["",""]
            DefC = ["",""]
            DefD = InputTimeout("Input The Device Nummbers That Shold Be Used As Default (Separated By Kommas E.G. 1,4) \\/\\/\\/ ",DefNumTimeout).split(",") + [""]
            DefC = InputTimeout("Input The Device Nummbers That Shold Be Used As Default Communications (Separated By Kommas E.G. 3,10) \\/\\/\\/ ",DefNumTimeout).split(",") + [""]
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
                    ExitWait(60)
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
                        ExitWait(60)
                else:
                    Unvalid[0] = 0
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
                    DefaultList.pop(4)
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
        Argsstr = ""
        for i in Args:
            Argsstr = Argsstr + " " + i
        Start(Connectlisttostr(Script),Argsstr[1:],True)
        exit()
    if os.path.exists(SoundVolumeViewPa):
        UseSVPA = True
    else:
        UseSVPA = False
    if Vexit == 1:
        ExitWait(60)
    f = open(AudioDDFilePa,"w")
    f.write(AudioDeviceFilePa)
    f.close()
    print("Done Prossesing\nStarting Audio Device Loop\n")
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
            ExitWait(60)
        f = open(VVJsonPa, encoding='UTF-16')
        try:
            ConfigJson = json.load(f)
        except:
            f.close()
            os.remove(VVJsonPa)
            print("Error SoundVolumeView Json Missing")
            ExitWait(60)
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
