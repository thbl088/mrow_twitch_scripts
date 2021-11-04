import clr
import os
import glob
import os.path
from os import path
import json
import ast

ScriptName = "!players"
Website = "https://www.twitch.tv/th_mrow"
Description = "Gives you the amount of players in your spellbreak game."
Creator = "th_mrow"
Version = "1.5.5"

m_CommandPermission = "moderator"
m_LogFileFolderPath = r'%LOCALAPPDATA%\g3\Saved\Logs'
m_FileType = '\*log'
m_LookFor = "blob data for"
m_LookForStreamerTeam = "PublicBlobData"

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
    elif type == "string":
        read = readFileRead.readline()
    elif type == "list":
        read = readFileRead.readlines()
    else:
        read = ""
        Parent.Log(ScriptName, "ReadFile : Wrong type, available types are int, string, list." )
    readFileRead.close()
    return read

def GetLogPLayers(logPath):
    playersRead = open(logPath, "r")
    players_str = playersRead.read()
    amount = players_str.count(m_LookFor)
    playersRead.close()
    return amount

def StartPlayers():
    totalOldPlayers = ReadFile(file_PreviousTotalPlayers, "int")
    totalPlayers = ReadFile(file_TotalPlayers, "int")
    players = totalPlayers - totalOldPlayers
    if players != 0:
        WriteFile(file_Players, players)
    return players

def ReadPlayerData():
    players = os.path.join(os.path.dirname(__file__), "PlayersData.txt")
    playersRead = open(players, "r")
    players_str = playersRead.read()
    playersRead.close()
    players_list = ast.literal_eval(players_str)
    return players_list

def WritePlayerName(data):
    players = os.path.join(os.path.dirname(__file__), "PlayersName.txt")
    playersWrite = open(players, "a")
    playersWrite.write('%s' % str(data) + "\n")
    playersWrite.close()
    return

def WriteStreamerTeamData(data):
    players = os.path.join(os.path.dirname(__file__), "StreamerTeamDatas.txt")
    playersWrite = open(players, "a")
    playersWrite.write('%s' % str(data) + "\n")
    playersWrite.close()
    return

def ChangeStats(data):
    players = os.path.join(os.path.dirname(__file__), "StreamerStats.txt")
    playersWrite = open(players, "a")
    playersWrite.write('%s' % str(data) + "\n")
    playersWrite.close()
    return

def WriteStats(data):
    players = os.path.join(os.path.dirname(__file__), "StreamerStats.txt")
    playersWrite = open(players, "w")
    playersWrite.write('%s' % str(data) + "\n")
    playersWrite.close()
    return

def WritePlayerXp(data):
    players = os.path.join(os.path.dirname(__file__), "PlayersXp.txt")
    playersWrite = open(players, "a")
    playersWrite.write('%s' % str(data) + "\n")
    playersWrite.close()
    return

def ConvertToJson(line):
    lineJson = json.loads(line)
    return lineJson

def GetJsonLine(line):
    excla = line.count("!")
    separate = line.split("!", excla)
    answer = separate[0]
    separate2 = answer.split(":", 5)
    answer2 = separate2[5]
    return answer2

def GetJsonLine2(line):
    separate = line.split("!", 1)
    answer = separate[0]
    separate = answer.split(">", 1)
    answer2 = separate[1]
    answer2 = answer2[:-2]
    return answer2

def FoundPlayersInfo(logPath):
    list = []
    logRead = open(logPath, "r")
    log_list = logRead.readlines()
    logRead.close()
    for line in log_list:
        if line.count(m_LookFor) !=0 :
            json = GetJsonLine(line)
            list.append(json)
    WriteFile(file_PlayersData, list)
    return

def WrotePlayersName():
    WriteFile(file_PlayersName, "")
    list = ReadPlayerData()
    nbPlayers = ReadFile(file_Players, "int")
    for i in range(len(list)-nbPlayers, len(list)):
        lineJson = ConvertToJson(list[i])
        WritePlayerName(lineJson['DisplayName'])
    return

def GetPlayersInfo(name, info):
    list = ReadPlayerData()
    nbPlayers = ReadFile(file_Players, "int")
    for i in range(len(list)-nbPlayers, len(list)):
        lineJson = ConvertToJson(list[i])
        if lineJson['DisplayName'] == name:
            Parent.SendTwitchMessage(str(lineJson[info]))
            return
    return

def WrotePlayersXP():
    WriteFile(file_PlayersInfo, "")
    list = ReadPlayerData()
    nbPlayers = ReadFile(file_Players, "int")
    #if nbPlayers == len(list):
    #    nbPlayers = 0
    for i in range(len(list)-nbPlayers, len(list)):
        infoList = []
        lineJson = ConvertToJson(list[i])
        infoList.append(lineJson['DisplayName'])
        infoList.append(lineJson['TotalXP'])
        WritePlayerXp(infoList)
    return

def WrotePlayersRank(rank):
    WriteFile(file_PlayersInfo, "")
    list = ReadPlayerData()
    nbPlayers = ReadFile(file_Players, "int")
    for i in range(len(list)-nbPlayers, len(list)):
        infoList = []
        lineJson = ConvertToJson(list[i])
        infoList.append(lineJson['DisplayName'])
        playerRank = lineJson['LeagueTierIds']['UnrankedTierIds'][rank]
        l = playerRank.split("_", 4)
        trueRank = l[4]
        infoList.append(trueRank)
        WritePlayerXp(infoList)
    return

def WrotePlayersClassXp(xp):
    WriteFile(file_PlayersInfo, "")
    list = ReadPlayerData()
    nbPlayers = ReadFile(file_Players, "int")
    for i in range(len(list)-nbPlayers, len(list)):
        infoList = []
        lineJson = ConvertToJson(list[i])
        infoList.append(lineJson['DisplayName'])
        playerRank = lineJson[xp]
        infoList.append(playerRank)
        WritePlayerXp(infoList)
    return

def GetTarget(playerList):
    targetNumber = Parent.GetRandom(0,len(playerList))
    return playerList[targetNumber]

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

def AddStats(playerName, mate):
    stats = ReadFile(file_StreamerStats, "list")
    if len(stats) == 0 :
        newStat = r'{"UserName" : "' + playerName + r'", "Enemy" :'+ str(1-mate) + r', "Ally" :' +  str(mate) + r'}'#.format(playerName)#.format(playerName[:-1])
        #stats.append(newStat)
        ChangeStats(newStat)
    else:
        IsInStat(playerName,stats, mate)
    return

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
            Parent.Log(ScriptName, "Ally : " + str(player))
            AddStats(player, 1)
        else :
            Parent.Log(ScriptName, "Enemy : " + str(player))
            AddStats(player, 0)
    return

def Init():
    return

def Execute(data):
    if data.IsChatMessage():
        if data.GetParam(0) == "!play" or data.GetParam(0) == "!cunt":
            if data.GetParamCount() == 1 and data.GetParam(0) == "!cunt":
                Parent.SendTwitchMessage(data.UserName + " is a cunt!")
                return

            if data.GetParam(1) == "cunthunt" or data.GetParam(1) == "hunt" :
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

        if data.GetParam(0) == "!players":

            if (data.GetParamCount() == 1):
                players = ReadFile(file_Players, "int")
                answer = "There is " + str(players) + " players, including the streamer team."
                Parent.SendTwitchMessage(answer)
                return

            #Check if there is a new log and reset old players if yes
            if data.GetParam(1) == "init" and Parent.HasPermission(data.User, m_CommandPermission,"Get the most recent log file and reset if new one"):
                lastest = LastestFile()
                lastestMemory = ReadFile(file_LatestLogPath, "string")
                if (lastest != lastestMemory):
                    WriteFile(file_LatestLogPath,lastest)
                    WriteFile(file_PreviousTotalPlayers, "0")
                    Parent.SendTwitchMessage("Old players reset")
                WriteFile(file_Players, "0")
                resetVal = ReadFile(file_PreviousTotalPlayers, "int")
                WriteFile(file_TotalPlayers, resetVal)
                Parent.SendTwitchMessage("Init done")
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

            if data.GetParam(1) == "reset" and Parent.HasPermission(data.User, m_CommandPermission,"Reset players and old players"):
                resetVal = ReadFile(file_PreviousTotalPlayers, "int")
                WriteFile(file_TotalPlayers, resetVal)
                WriteFile(file_PreviousTotalPlayers, "0")
                WriteFile(file_Players, "0")
                WriteFile(file_PlayersData, "")
                WriteFile(file_PlayersName, "")
                Parent.SendTwitchMessage("reset done")
                return

            if data.GetParam(1) == "xp":
                path = LastestFile()
                FoundPlayersInfo(path)
                WrotePlayersXP()
                list = ReadFile(file_PlayersInfo, "list")
                Parent.SendTwitchMessage(str(list).replace(r"\n", ""))
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
                Parent.SendTwitchMessage(str(list).replace(r"\n", ""))
                return

            if data.GetParam(1) == "team":
                list = ReadFile(file_StreamerTeamDatas, "list")
                Parent.SendTwitchMessage(str(list).replace(r"\n", ""))
                return

            if data.GetParam(1) == "stat" and Parent.HasPermission(data.User, "broadcaster","Reset players and old players"):
                path = LastestFile()
                GetStreamerTeamData(path)
                DoStats()
                return

            if data.GetParam(1) == "resetstat" and Parent.HasPermission(data.User, "broadcaster","Reset players and old players"):
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

def Tick():
    return