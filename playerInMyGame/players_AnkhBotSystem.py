import os
import glob
import os.path
from os import path
import json
import ast
import clr
import unicodedata
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")

# App datas, don't forgot to follow me ;)
ScriptName = "!players"
Website = "https://www.twitch.tv/th_mrow"
Description = "Gives you the amount of players in your spellbreak game."
Creator = "th_mrow"
Version = "1.7.0"

# Parameters
m_CommandPermission = "moderator"
m_LogFileFolderPath = r'%LOCALAPPDATA%\g3\Saved\Logs'
m_FileType = '\*log'
m_LookFor = "blob data for"
m_LookForStreamerTeam = "PublicBlobData"
m_LookForNewGame = "InteractiveManager /Game/Maps/Longshot/Alpha/Alpha_Resculpt OnMatchStarted"

# All the wiki url
url_outfit = "https://spellbreak.fandom.com/wiki/"


# All the file use to save data
file_LatestLogPath = "LatestLogPath.txt"
file_PreviousTotalPlayers = "PreviousTotalPlayers.txt"
file_TotalPlayers = "TotalPlayers.txt"
file_Players = "Players.txt"
file_PlayersData = "PlayersData.txt"
file_StreamerTeamNumber = "StreamerTeamNumber.txt"
file_PlayersName = "PlayersName.txt"
file_StreamerTeamDatas = "StreamerTeamDatas.txt"
file_StreamerStats = "StreamerStats.txt"
file_PlayersInfo = "PlayersXp.txt"
file_NbMatches = "NbMatches.txt"
file_HasSound = "HasSound.txt"
file_Volume = "Volume.txt"

sound_miaou = "miaou.mp3"


def GetSoundPath(soundName):
    soundPath = os.path.join(os.path.dirname(__file__) + "\\sound\\", soundName)
    return soundPath

#return the path of the lastest log file create
def LastestFile():
    files = glob.glob(path.expandvars(m_LogFileFolderPath) + m_FileType)
    max_file = max(files, key=os.path.getctime)
    return max_file

# Write file ("file.txt") with message
def WriteFile(file, message):
    writeFile = os.path.join(os.path.dirname(__file__), file)
    writeFileWrite = open(writeFile, "w")
    writeFileWrite.write('%s' % str(message))
    writeFileWrite.close()
    return

# Read file and return the lecture in type
def ReadFile(file, type):
    readFile = os.path.join(os.path.dirname(__file__), file)
    readFileRead = open(readFile, "r")
    if type == "int":
        read = readFileRead.readline()
        read = int(float(read))
    elif type == "float":
        read = readFileRead.readline()
        read = float(read)
    elif type == "string":
        read = readFileRead.readline()
    elif type == "list":
        read = readFileRead.readlines()
    else:
        read = ""
        Parent.Log(ScriptName, "ReadFile : Wrong type, available types are int, string, list." )
    readFileRead.close()
    return read

# Read the more recent logfile and return the amount of new players with m_LookFor because that variable is there only for new players
def GetLogPLayers(logPath):
    playersRead = open(logPath, "r")
    players_str = playersRead.read()
    amount = players_str.count(m_LookFor)
    playersRead.close()
    return amount

# If we have more players now than before then new lobby with "total players now in the log" - "previous amount of players in the log"
def StartPlayers():
    totalOldPlayers = ReadFile(file_PreviousTotalPlayers, "int")
    totalPlayers = ReadFile(file_TotalPlayers, "int")
    players = totalPlayers - totalOldPlayers
    if players != 0:
        WriteFile(file_Players, players)
    return players

# We read players data and convert it to a valid list.
def ReadPlayerData():
    players = os.path.join(os.path.dirname(__file__) , "PlayersData.txt")
    playersRead = open(players, "r")
    players_str = playersRead.read()
    playersRead.close()
    players_list = ast.literal_eval(players_str)
    return players_list

def WritePlayerName(data):
    players = os.path.join(os.path.dirname(__file__) , "PlayersName.txt")
    playersWrite = open(players, "a")
    playersWrite.write('%s' % str(data) + "\n")
    playersWrite.close()
    return

def WriteStreamerTeamData(data):
    players = os.path.join(os.path.dirname(__file__) , "StreamerTeamDatas.txt")
    playersWrite = open(players, "a")
    playersWrite.write('%s' % str(data) + "\n")
    playersWrite.close()
    return

def ChangeStats(data):
    players = os.path.join(os.path.dirname(__file__) , "StreamerStats.txt")
    playersWrite = open(players, "a")
    playersWrite.write('%s' % str(data) + "\n")
    playersWrite.close()
    return

def WriteStats(data):
    players = os.path.join(os.path.dirname(__file__) , "StreamerStats.txt")
    playersWrite = open(players, "w")
    playersWrite.write('%s' % str(data) + "\n")
    playersWrite.close()
    return

def WritePlayerXp(data):
    players = os.path.join(os.path.dirname(__file__) , "PlayersXp.txt")
    playersWrite = open(players, "a")
    playersWrite.write('%s' % str(data) + "\n")
    playersWrite.close()
    return

# We convert a line containing a Json to a Json
def ConvertToJson(line):
    lineJson = json.loads(line)
    return lineJson

# We get the Json part of the line containing a new players by cutting the end and the beginning
# Yes that's ugly af, but that's working.
def GetJsonLine(line):
    excla = line.count("!")
    separate = line.split("!", excla)
    answer = separate[0]
    separate2 = answer.split(":", 5)
    answer2 = separate2[5]
    return answer2

# We get the Json part of the line containing a new teammate, yes the name is explicit :)
def GetJsonLine2(line):
    separate = line.split("!", 1)
    answer = separate[0]
    separate = answer.split(">", 1)
    answer2 = separate[1]
    answer2 = answer2[:-2]
    return answer2

# We read the log file, and collect all the new player line, convert it to a Json then write it in the playersData file in a List
def FoundPlayersInfo(logPath):
    list = []
    logRead = open(logPath, "r")
    log_list = logRead.readlines()
    logRead.close()
    for line in log_list:
        if line.count(m_LookFor) !=0 :
            excl = line.count("!")
            dot = line.count(":")
            if excl == 1:
                json = GetJsonLine(line)
                list.append(json)
    WriteFile(file_PlayersData, list)
    return

# We read the playerData file, and convert all the line(of the list) to a Json then write all the name.
# We can access the element of a Json like with a Hash map (["Key"])
def WrotePlayersName():
    WriteFile(file_PlayersName, "")
    list = ReadPlayerData()
    nbPlayers = ReadFile(file_Players, "int")
    for i in range(len(list)-nbPlayers, len(list)):
        lineJson = ConvertToJson(list[i])
        WritePlayerName(lineJson['DisplayName'])
    return

# We read the last nbplayers (amount of players in your game) of the list, and if the name correspond we read the info corresponding
def GetPlayersInfo(name, info):
    list = ReadPlayerData()
    nbPlayers = ReadFile(file_Players, "int")
    for i in range(len(list)-nbPlayers, len(list)):
        lineJson = ConvertToJson(list[i])
        if lineJson['DisplayName'] == name:
            Parent.SendTwitchMessage(str(lineJson[info]))
            return
    return

# We read the last nbplayers of the list, and add their name + totalxp in a list.
def WrotePlayersXP():
    WriteFile(file_PlayersInfo, "")
    list = ReadPlayerData()
    nbPlayers = ReadFile(file_Players, "int")
    #if nbPlayers == len(list):
    #    nbPlayers = 0
    for i in range(len(list)-nbPlayers, len(list)):
        infoList = []
        lineJson = ConvertToJson(list[i])
        name = lineJson['DisplayName']
        ret = unicode(name.strip('"'), encoding='utf-8', errors='ignore')
        Parent.Log(ScriptName, "xp name : " + ret)
        infoList.append(ret)
        infoList.append(lineJson['TotalXP'])
        WritePlayerXp(infoList)
    return

# We read the last nbplayers of the list, and add their name + wanted rank (solo, duo, squad) in a list. Nobody cares about dominion.
def WrotePlayersRank(rank):
    WriteFile(file_PlayersInfo, "")
    list = ReadPlayerData()
    nbPlayers = ReadFile(file_Players, "int")
    for i in range(len(list)-nbPlayers, len(list)):
        infoList = []
        lineJson = ConvertToJson(list[i])
        name = lineJson['DisplayName']
        ret = unicode(name.strip('"'), encoding='utf-8', errors='ignore')
        Parent.Log(ScriptName, "xp name : " + ret)
        infoList.append(ret)
        playerRank = lineJson['LeagueTierIds']['UnrankedTierIds'][rank]
        l = playerRank.split("_", 4)
        trueRank = l[4]
        infoList.append(trueRank)
        WritePlayerXp(infoList)
    return


def WrotePlayersSkin(rank):
    WriteFile(file_PlayersInfo, "")
    list = ReadPlayerData()
    nbPlayers = ReadFile(file_Players, "int")
    for i in range(len(list)-nbPlayers, len(list)):
        infoList = []
        lineJson = ConvertToJson(list[i])
        name = lineJson['DisplayName']
        ret = unicode(name.strip('"'), encoding='utf-8', errors='ignore')
        Parent.Log(ScriptName,  "xp name : " + ret)
        infoList.append(ret)
        playerRank = lineJson['CosmeticLoadout'][rank]
        l = playerRank.split("_", 3)
        trueRank = l[3]
        infoList.append(trueRank)
        WritePlayerXp(infoList)
    return

# We read the last nbplayers of the list, and add their name + class xp in a list. But doesn't display his class because that would be cheating.
def WrotePlayersClassXp(xp):
    WriteFile(file_PlayersInfo, "")
    list = ReadPlayerData()
    nbPlayers = ReadFile(file_Players, "int")
    for i in range(len(list)-nbPlayers, len(list)):
        infoList = []
        lineJson = ConvertToJson(list[i])
        name = lineJson['DisplayName']
        ret = unicode(name.strip('"'), encoding='utf-8', errors='ignore')
        Parent.Log(ScriptName,  "xp name : " + ret)
        infoList.append(ret)

        playerRank = lineJson[xp]
        infoList.append(playerRank)
        WritePlayerXp(infoList)
    return
# We read the last nbplayers of the list, and add their name + platform
def WrotePlayersClassPlateform(xp):
    WriteFile(file_PlayersInfo, "")
    list = ReadPlayerData()
    nbPlayers = ReadFile(file_Players, "int")
    for i in range(len(list)-nbPlayers, len(list)):
        infoList = []
        lineJson = ConvertToJson(list[i])
        name = lineJson['DisplayName']
        ret = unicode(name.strip('"'), encoding='utf-8', errors='ignore')
        Parent.Log(ScriptName,  "xp name : " + ret)
        infoList.append(ret)
        playerRank = lineJson[xp].split(":", 1)
        playerRank = playerRank[0].replace("\\", "")
        infoList.append(playerRank)
        WritePlayerXp(infoList)
    return

# Return the name of a random player in the lobby
def GetTarget(playerList):
    targetNumber = Parent.GetRandom(0,len(playerList))
    return playerList[targetNumber]

# Get the data of the streamer team. And do some "complex" shit.
def GetStreamerTeamData(logPath):
    WriteFile(file_StreamerTeamDatas, "")
    list = []
    logRead = open(logPath, "r")
    log_list = logRead.readlines()
    logRead.close()
    for line in log_list:
        if line.count(m_LookForStreamerTeam) != 0:
            json = GetJsonLine2(line)
            list.append(json)
    nbTeamStrea = ReadFile(file_StreamerTeamNumber, "int")
    fromNb = nbTeamStrea
    if fromNb == len(list) :
        fromNb = 0
    for i in range (fromNb, len(list)):
        lineJson = ConvertToJson(list[i])
        WriteStreamerTeamData(str(lineJson['DisplayName']))
    WriteFile(file_StreamerTeamNumber, len(list))
    return

# Check if we have a new match.
def IsNewMatch(logPath):
    amountMatches_old = ReadFile(file_NbMatches, "int")
    logRead = open(logPath, "r")
    log_list = logRead.readlines()
    logRead.close()
    count = 0
    for line in log_list:
        if line.count(m_LookForNewGame) !=0: count+=1
    if count > amountMatches_old:
        Parent.Log(ScriptName, "New Match")
        WriteFile(file_NbMatches, amountMatches_old+1)
        Parent.SendTwitchMessage("New match")
        if ReadFile(file_HasSound, "string") == "True":
            volume = ReadFile(file_Volume, "float")
            soundPath = GetSoundPath(sound_miaou)
            miaou = Parent.PlaySound(soundPath, volume)
        NewGame()


# Check if the players is in the streamerStat. And either complete it depending of his team, or create a new row. Also do some "complex" shit
def IsInStat(playerName, stats, mate):
    toChange = True
    toWrite = False
    i=0
    for player in stats :
        player = ast.literal_eval(player)
        if player['UserName'] == playerName:
            if mate:
                updateStat = r'{"UserName" : "' + playerName + r'", "Enemy" :' + str(player['Enemy']) + r', "Ally" :' + str(player['Ally']+1) + r'}.'
            else:
                updateStat = r'{"UserName" : "' + playerName + r'", "Enemy" :' + str(player['Enemy']+1) + r', "Ally" :' + str(player['Ally']) + r'}.'
            stats[i] = updateStat
            toChange = False
            WriteFile(file_StreamerStats, "")
            for stat in stats:
                ChangeStats(stat[:-1])
        else:
            newStat = r'{"UserName" : "' + playerName + r'", "Enemy" :' + str(1 - mate) + r', "Ally" :' + str(mate) + r'}'  # .format(playerName)#.format(playerName[:-1])
            #ChangeStats(newStat)
            #toChange.append(newStat)
        i+=1
    if toChange:
        ChangeStats(newStat)
    if toWrite:
        WriteStats(stats)
    #WriteStats(toWrite)
    return

# Add a player to the streamer stat
def AddStats(playerName, mate):
    stats = ReadFile(file_StreamerStats, "list")
    if len(stats) == 0 :
        newStat = r'{"UserName" : "' + playerName + r'", "Enemy" :'+ str(1-mate) + r', "Ally" :' +  str(mate) + r'}'# 1-mate useless but cool
        #stats.append(newStat)
        ChangeStats(newStat)
    else:
        IsInStat(playerName,stats, mate)
    return

# Bla bla bla do everything for the streamer stat
def DoStats():
    path = LastestFile()
    FoundPlayersInfo(path)
    WrotePlayersName()
    playerList = ReadFile(file_PlayersName, "list")
    teamMates1 = ReadFile(file_StreamerTeamDatas, "list")
    teamMates = []
    for mate in teamMates1:
        new_mate = mate[:-1]
        teamMates.append(new_mate)

    for player in playerList:
        player = player[:-1]
        if player in teamMates:
            #Parent.Log(ScriptName, "Ally : " + str(player))
            AddStats(player, 1)
        else :
            #Parent.Log(ScriptName, "Enemy : " + str(player))
            AddStats(player, 0)
    return

def NewGame():
    path = LastestFile()
    totPlayers = GetLogPLayers(path)
    WriteFile(file_TotalPlayers, totPlayers)
    players = StartPlayers()
    if players != 0:
        answer = "There is " + str(players) + " players, including your team."
        WriteFile(file_PreviousTotalPlayers, totPlayers)
        GetStreamerTeamData(path)
        Parent.SendTwitchMessage(answer)
        DoStats()
        WriteFile(file_PlayersData, "")
    else:
        Parent.SendTwitchMessage("You are still in the same match")
    return

def turnOnMatchAlert(state):
    if state:
        WriteFile(file_HasSound, "True")
    else:
        WriteFile(file_HasSound, "False")
    return

def changeVolume(volume):
    if volume < 2:
        WriteFile(file_Volume, volume)
        soundPath = GetSoundPath(sound_miaou)
        miaou = Parent.PlaySound(soundPath, float(volume))
    else:
        Parent.SendTwitchMessage("Sound too loud")
    return

def InitGame():
    lastest = LastestFile()
    lastestMemory = ReadFile(file_LatestLogPath, "string")
    if (lastest != lastestMemory):
        WriteFile(file_LatestLogPath, lastest)
        WriteFile(file_PreviousTotalPlayers, "0")
        WriteFile(file_NbMatches, 0)
        Parent.SendTwitchMessage("Hello world")
    WriteFile(file_Players, "0")
    resetVal = ReadFile(file_PreviousTotalPlayers, "int")
    WriteFile(file_TotalPlayers, resetVal)
    return

# Useless for now
def Init():
    InitGame()
    return

# Main function
def Execute(data):
    if data.IsChatMessage():
        # ----------------Sounds commands--------------------------------------
        if data.GetParam(0) == "!sound" and Parent.HasPermission(data.User, m_CommandPermission,"Change sound"):
            if data.GetParamCount() == 1:
                Parent.SendTwitchMessage("!sound + number below 1, for example !sound 0.1")
            if data.GetParam(1) == "off":
                turnOnMatchAlert(False)
            if data.GetParam(1) == "on":
                turnOnMatchAlert(True)
                volume = ReadFile(file_Volume, "float")
                soundPath = GetSoundPath(sound_miaou)
                miaou = Parent.PlaySound(soundPath, volume)
            else:
                newVolume = float(data.GetParam(1))
                if isinstance(newVolume, float) and newVolume < 5.0:
                    changeVolume(data.GetParam(1))
            return
        # ----------------misc commands--------------------------------------
        if data.GetParam(0) == "!th_mrow" and (Parent.HasPermission(data.User, m_CommandPermission,"easter egg") or data.UserName == "th_mrow"):
                Parent.SendTwitchMessage("This was a triumph. I'm making a note here: HUGE SUCCESS. It's hard to overstate my satisfaction.")
                return

        # ----------------Play commands--------------------------------------
        if data.GetParam(0) == "!play" or data.GetParam(0) == "!cunt":
            if data.GetParamCount() == 1 and data.GetParam(0) == "!cunt":
                Parent.SendTwitchMessage(data.UserName + " is a cunt!")
                return

            if data.GetParam(1) == "cunthunt" or data.GetParam(1) == "hunt":
                path = LastestFile()
                FoundPlayersInfo(path)
                WrotePlayersName()
                list = ReadFile(file_PlayersName, "list")
                target = GetTarget(list)
                message = "You must hunt " + str(target)
                Parent.SendTwitchMessage(message)
                return

            if data.GetParam(1).lower() == "protectcunt" or data.GetParam(1).lower() == "protect":
                list = ReadFile(file_StreamerTeamDatas, "list")
                target = GetTarget(list)
                message = "You must protect " + str(target)
                Parent.SendTwitchMessage(message)
                return

        # ----------------Skin commands-----------------------------------------
        if data.GetParam(0) == "!skin":
            if data.GetParamCount() == 2:
                skin = url_outfit + data.GetParam(1)
                Parent.SendTwitchMessage(skin)
            else:
                Parent.SendTwitchMessage("The command is !skin + name of the skin got with !players skin")
            return

        # ----------------Players commands--------------------------------------
        if data.GetParam(0) == "!players":
            if (data.GetParamCount() == 1):
                players = ReadFile(file_Players, "int")
                answer = "There is " + str(players) + " players, including the streamer team."
                Parent.SendTwitchMessage(answer)
                return
            # ----------------streamer commands--------------------------------------
            #Check if there is a new log and reset old players if yes
            if data.GetParam(1) == "init" and Parent.HasPermission(data.User, m_CommandPermission,"Get the most recent log file and reset if new one"):
                InitGame()
                return

            if data.GetParam(1) == "update" and Parent.HasPermission(data.User, m_CommandPermission,"Get the amount of player in your lobby"):
                path = LastestFile()
                totPlayers = GetLogPLayers(path)
                WriteFile(file_TotalPlayers, totPlayers)
                players = StartPlayers() + ReadFile(file_Players, "int")
                answer = "There is " + str(players) + " players, including your team."
                WriteFile(file_Players, players)
                WriteFile(file_PreviousTotalPlayers, totPlayers)
                Parent.SendTwitchMessage(answer)
                return

            if (data.GetParam(1) == "newGame" or data.GetParam(1) == "ng") and Parent.HasPermission(data.User, m_CommandPermission,"Reset players and old players"):
                NewGame()

            if data.GetParam(1) == "reset" and Parent.HasPermission(data.User, m_CommandPermission,"Reset players and old players"):
                resetVal = ReadFile(file_PreviousTotalPlayers, "int")
                WriteFile(file_TotalPlayers, resetVal)
                WriteFile(file_PreviousTotalPlayers, "0")
                WriteFile(file_Players, "0")
                WriteFile(file_PlayersData, "")
                WriteFile(file_PlayersName, "")
                Parent.SendTwitchMessage("reset done")
                return

            # ----------------Viewer commands--------------------------------------
            if data.GetParam(1) == "xp":
                path = LastestFile()
                FoundPlayersInfo(path)
                WrotePlayersXP()
                list = ReadFile(file_PlayersInfo, "list")
                msg = repr(list).decode('unicode-escape')
                allNames = "".join(msg.splitlines())
                Parent.SendTwitchMessage(str(allNames).replace(r"\n", ""))
                return

            if data.GetParam(1) == "solo":
                path = LastestFile()
                FoundPlayersInfo(path)
                WrotePlayersRank("GameModeInfo:DA_BattleRoyale_Solo")
                list = ReadFile(file_PlayersInfo, "list")
                Parent.SendTwitchMessage(str(list).replace(r"\n", ""))
                return

            if data.GetParam(1) == "duo":
                path = LastestFile()
                FoundPlayersInfo(path)
                WrotePlayersRank("GameModeInfo:DA_BattleRoyale_Duo")
                list = ReadFile(file_PlayersInfo, "list")
                Parent.SendTwitchMessage(str(list).replace(r"\n", ""))
                return

            if data.GetParam(1) == "squad":
                path = LastestFile()
                FoundPlayersInfo(path)
                WrotePlayersRank("GameModeInfo:DA_BattleRoyale_Squad")
                list = ReadFile(file_PlayersInfo, "list")
                Parent.SendTwitchMessage(str(list).replace(r"\n", ""))
                return

            if data.GetParam(1) == "skin":
                path = LastestFile()
                FoundPlayersInfo(path)
                WrotePlayersSkin("SkinId")
                list = ReadFile(file_PlayersInfo, "list")
                Parent.SendTwitchMessage(str(list).replace(r"\n", ""))
                return

            if data.GetParam(1) == "artifact":
                path = LastestFile()
                FoundPlayersInfo(path)
                WrotePlayersSkin("ArtifactId")
                list = ReadFile(file_PlayersInfo, "list")
                Parent.SendTwitchMessage(str(list).replace(r"\n", ""))
                return

            if data.GetParam(1) == "cloudburst":
                path = LastestFile()
                FoundPlayersInfo(path)
                WrotePlayersSkin("DropTrailID")
                list = ReadFile(file_PlayersInfo, "list")
                Parent.SendTwitchMessage(str(list).replace(r"\n", ""))
                return

            if data.GetParam(1) == "afterglow":
                path = LastestFile()
                FoundPlayersInfo(path)
                WrotePlayersSkin("RunTrailID")
                list = ReadFile(file_PlayersInfo, "list")
                Parent.SendTwitchMessage(str(list).replace(r"\n", ""))
                return

            if data.GetParam(1) == "badge":
                path = LastestFile()
                FoundPlayersInfo(path)
                WrotePlayersSkin("BadgeId")
                list = ReadFile(file_PlayersInfo, "list")
                Parent.SendTwitchMessage(str(list).replace(r"\n", ""))
                return

            if data.GetParam(1) == "title":
                path = LastestFile()
                FoundPlayersInfo(path)
                WrotePlayersSkin("TitleId")
                list = ReadFile(file_PlayersInfo, "list")
                Parent.SendTwitchMessage(str(list).replace(r"\n", ""))
                return

            if data.GetParam(1) == "card":
                path = LastestFile()
                FoundPlayersInfo(path)
                WrotePlayersSkin("CardId")
                list = ReadFile(file_PlayersInfo, "list")
                Parent.SendTwitchMessage(str(list).replace(r"\n", ""))
                return

            if data.GetParam(1) == "platform":
                path = LastestFile()
                FoundPlayersInfo(path)
                WrotePlayersClassPlateform("CurrentAccount")
                list = ReadFile(file_PlayersInfo, "list")
                Parent.SendTwitchMessage(str(list).replace(r"\n", ""))
                return

            if data.GetParam(1) == "triumph":
                path = LastestFile()
                Parent.SendTwitchMessage("Imagine having another triumph emote.")
                return

            if data.GetParam(1) == "class":
                path = LastestFile()
                FoundPlayersInfo(path)
                WrotePlayersClassXp("CharacterClassXP")
                list = ReadFile(file_PlayersInfo, "list")
                Parent.SendTwitchMessage(str(list).replace(r"\n", ""))
                return

            if data.GetParam(1) == "name":
                path = LastestFile()
                FoundPlayersInfo(path)
                WrotePlayersName()
                list = ReadFile(file_PlayersName, "list")
                names = []
                for playerName in list:
                    ret = unicode(playerName.strip('"'), encoding='utf-8', errors='ignore')
                    names.append(ret)
                msg = repr(names).decode('unicode-escape')
                allNames = "".join(msg.splitlines())
                Parent.SendTwitchMessage(allNames)
                return

            if data.GetParam(1) == "team":
                list = ReadFile(file_StreamerTeamDatas, "list")
                Parent.SendTwitchMessage(str(list).replace(r"\n", ""))
                return

            # ----------------Players misc commands--------------------------------------
            if data.GetParam(1) == "discord":
                Parent.SendTwitchMessage("There is the invitation to join the discord of mrow's script : https://discord.gg/NCHEraagAB")
                return

            if data.GetParam(1) == "how":
                Parent.SendTwitchMessage("That script is only available on pc. I'm reading the log file to see all the players who logs in the lobby.")
                return

            # ----------------Admin commands--------------------------------------
            if data.GetParam(1) == "stat" and Parent.HasPermission(data.User, "broadcaster","Reset players and old players"):
                path = LastestFile()
                GetStreamerTeamData(path)
                DoStats()
                return

            if data.GetParam(1) == "resetstat" and Parent.HasPermission(data.User, "broadcaster", "Reset players and old players"):
                WriteFile(file_StreamerStats, "")
                Parent.SendTwitchMessage("reset stat done")
                return

            if data.GetParam(1) == "fullReset" and Parent.HasPermission(data.User, "broadcaster","Reset players and old players"):
                resetVal = ReadFile(file_PreviousTotalPlayers, "int")
                WriteFile(file_TotalPlayers, resetVal)

                WriteFile(file_StreamerTeamDatas, "")
                WriteFile(file_PlayersData, "")
                WriteFile(file_PlayersName, "")
                WriteFile(file_PlayersInfo, "")
                WriteFile(file_Players, "0")
                WriteFile(file_PreviousTotalPlayers, "0")
                WriteFile(file_StreamerTeamNumber, "0")
                WriteFile(file_StreamerTeamDatas, "")
                Parent.SendTwitchMessage("Full reset done")
                return
        return
    return

# Auto-check if we are in a new game
def Tick():
    path = LastestFile()
    IsNewMatch(path)
    return