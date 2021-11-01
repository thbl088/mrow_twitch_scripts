import datetime
import sys
import io
import clr
import os
import glob
import os.path
from os import path
import random
import time
import re
import json
import ast

clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")

ScriptName = "!players"
Website = "https://www.twitch.tv/th_mrow"
Description = "Gives you the amount of players in your spellbreak game."
Creator = "th_mrow"
Version = "1.5.1"

m_CommandPermission = "moderator"
m_LogFileFolderPath = r'%LOCALAPPDATA%\g3\Saved\Logs'
m_FileType = '\*log'
m_LookFor = "blob data for"
m_LookForStreamerTeam = "PublicBlobData"

#return the path of the lastest log file create
def LastestFile():
    files = glob.glob(path.expandvars(m_LogFileFolderPath) + m_FileType)
    max_file = max(files, key=os.path.getctime)
    return max_file

def WriteLastestFile(file):
    latestFile = os.path.join(os.path.dirname(__file__), "LatestLogPath.txt")
    latestFileWrite = open(latestFile, "w")
    latestFileWrite.write('%s' % str(file))
    latestFileWrite.close()
    return

def GetLastestFile():
    latestFile = os.path.join(os.path.dirname(__file__), "LatestLogPath.txt")
    latestFileRead = open(latestFile, "r")
    latestFile_str = latestFileRead.readline()
    latestFileRead.close()
    return latestFile_str

def ReadOldPlayers():
    oldPlayers = os.path.join(os.path.dirname(__file__), "PreviousTotalPlayers.txt")
    oldPlayersRead = open(oldPlayers, "r")
    oldPlayers_str = oldPlayersRead.readline()
    oldPlayersRead.close()
    return int(float(oldPlayers_str))

def ResetOldPlayers():
    oldPlayers = os.path.join(os.path.dirname(__file__), "PreviousTotalPlayers.txt")
    oldPlayersWrite = open(oldPlayers, "w")
    oldPlayersWrite.write('%s' % str(0))
    oldPlayersWrite.close()
    return

def ChangeOldPlayers(newPlayers):
    oldPlayers = os.path.join(os.path.dirname(__file__), "PreviousTotalPlayers.txt")
    oldPlayersWrite = open(oldPlayers, "w")
    oldPlayersWrite.write('%s' % str(newPlayers))
    oldPlayersWrite.close()
    return

def AddOldPlayers(newPlayers):
    formerOldPlayers = ReadOldPlayers()
    totalOldPlayers = formerOldPlayers + newPlayers
    oldPlayers = os.path.join(os.path.dirname(__file__), "PreviousTotalPlayers.txt")
    oldPlayersWrite = open(oldPlayers, "w")
    oldPlayersWrite.write('%s' % str(totalOldPlayers))
    oldPlayersWrite.close()
    return

def ReadPlayers():
    players = os.path.join(os.path.dirname(__file__), "TotalPlayers.txt")
    playersRead = open(players, "r")
    players_str = playersRead.readline()
    playersRead.close()
    return int(float(players_str))

def ResetPlayers():
    players = os.path.join(os.path.dirname(__file__), "TotalPlayers.txt")
    playersWrite = open(players, "w")
    resetVal = ReadOldPlayers()
    playersWrite.write('%s' % str(resetVal))
    playersWrite.close()
    return

def ChangePlayers(newPlayers):
    players = os.path.join(os.path.dirname(__file__), "TotalPlayers.txt")
    playersWrite = open(players, "w")
    playersWrite.write('%s' % str(newPlayers))
    playersWrite.close()
    return

def ReadSavePlayers():
    players = os.path.join(os.path.dirname(__file__), "Players.txt")
    playersRead = open(players, "r")
    players_str = playersRead.readline()
    playersRead.close()
    return int(float(players_str))

def ResetSavePlayers():
    players = os.path.join(os.path.dirname(__file__), "Players.txt")
    playersWrite = open(players, "w")
    playersWrite.write('%s' % str(0))
    playersWrite.close()
    return

def ChangeSavePlayers(newPlayers):
    players = os.path.join(os.path.dirname(__file__), "Players.txt")
    playersWrite = open(players, "w")
    playersWrite.write('%s' % str(newPlayers))
    playersWrite.close()
    return

def GetLogPLayers(logPath):
    playersRead = open(logPath, "r")
    players_str = playersRead.read()
    amount = players_str.count(m_LookFor)
    playersRead.close()
    return amount

def StartPlayers():
    totalOldPlayers = ReadOldPlayers()
    totalPlayers = ReadPlayers()
    players = totalPlayers - totalOldPlayers
    if players != 0:
        ChangeSavePlayers(players)
    return players

def WritePlayerData(data):
    players = os.path.join(os.path.dirname(__file__), "PlayersData.txt")
    playersWrite = open(players, "w")
    playersWrite.write('%s' % str(data))
    playersWrite.close()
    return

def ResetPlayerData():
    players = os.path.join(os.path.dirname(__file__), "PlayersData.txt")
    playersWrite = open(players, "w")
    playersWrite.write('%s' % str(""))
    playersWrite.close()
    return

def ReadPlayerData():
    players = os.path.join(os.path.dirname(__file__), "PlayersData.txt")
    playersRead = open(players, "r")
    players_str = playersRead.read()
    playersRead.close()
    players_list = ast.literal_eval(players_str)
    return players_list

def WriteStreamerTeamNumb(data):
    players = os.path.join(os.path.dirname(__file__), "StreamerTeamNumber.txt")
    playersWrite = open(players, "w")
    playersWrite.write('%s' % str(data))
    playersWrite.close()
    return

def ResetStreamerTeamNumb():
    players = os.path.join(os.path.dirname(__file__), "StreamerTeamNumber.txt")
    playersWrite = open(players, "w")
    playersWrite.write('%s' % str(0))
    playersWrite.close()
    return

def ReadStreamerTeamNumb():
    oldPlayers = os.path.join(os.path.dirname(__file__), "StreamerTeamNumber.txt")
    oldPlayersRead = open(oldPlayers, "r")
    oldPlayers_str = oldPlayersRead.readline()
    oldPlayersRead.close()
    return int(float(oldPlayers_str))

def WritePlayerName(data):
    players = os.path.join(os.path.dirname(__file__), "PlayersName.txt")
    playersWrite = open(players, "a")
    playersWrite.write('%s' % str(data) + "\n")
    playersWrite.close()
    return

def ResetPlayerName():
    players = os.path.join(os.path.dirname(__file__), "PlayersName.txt")
    playersWrite = open(players, "w")
    playersWrite.write('%s' % str(""))
    playersWrite.close()
    return

def ReadPlayerName():
    players = os.path.join(os.path.dirname(__file__), "PlayersName.txt")
    playersRead = open(players, "r")
    players_list = playersRead.readlines()
    playersRead.close()
    return players_list

def WriteStreamerTeamData(data):
    players = os.path.join(os.path.dirname(__file__), "StreamerTeamDatas.txt")
    playersWrite = open(players, "a")
    playersWrite.write('%s' % str(data) + "\n")
    playersWrite.close()
    return

def ResetStreamerTeamData():
    players = os.path.join(os.path.dirname(__file__), "StreamerTeamDatas.txt")
    playersWrite = open(players, "w")
    playersWrite.write('%s' % str(""))
    playersWrite.close()
    return

def ReadStreamerTeamData():
    players = os.path.join(os.path.dirname(__file__), "StreamerTeamDatas.txt")
    playersRead = open(players, "r")
    players_list = playersRead.readlines()
    playersRead.close()
    return players_list

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

def ResetStats():
    players = os.path.join(os.path.dirname(__file__), "StreamerStats.txt")
    playersWrite = open(players, "w")
    playersWrite.write('%s' % str(""))
    playersWrite.close()
    return

def ReadStats():
    players = os.path.join(os.path.dirname(__file__), "StreamerStats.txt")
    playersRead = open(players, "r")
    players_list = playersRead.readlines()
    playersRead.close()
    return players_list

def WritePlayerXp(data):
    players = os.path.join(os.path.dirname(__file__), "PlayersXp.txt")
    playersWrite = open(players, "a")
    playersWrite.write('%s' % str(data) + "\n")
    playersWrite.close()
    return

def ResetPlayerXp():
    players = os.path.join(os.path.dirname(__file__), "PlayersXp.txt")
    playersWrite = open(players, "w")
    playersWrite.write('%s' % str(""))
    playersWrite.close()
    return

def ReadPlayerXp():
    players = os.path.join(os.path.dirname(__file__), "PlayersXp.txt")
    playersRead = open(players, "r")
    players_list = playersRead.readlines()
    playersRead.close()
    return players_list

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
    WritePlayerData(list)
    return

def WrotePlayersName():
    ResetPlayerName()
    list = ReadPlayerData()
    nbPlayers = ReadSavePlayers()
    for i in range(len(list)-nbPlayers, len(list)):
        lineJson = ConvertToJson(list[i])
        WritePlayerName(lineJson['DisplayName'])
    return

def GetPlayersInfo(name, info):
    list = ReadPlayerData()
    nbPlayers = ReadSavePlayers()
    for i in range(len(list)-nbPlayers, len(list)):
        lineJson = ConvertToJson(list[i])
        if lineJson['DisplayName'] == name:
            Parent.SendTwitchMessage(str(lineJson[info]))
            return
    return


def WrotePlayersXP():
    ResetPlayerXp()
    list = ReadPlayerData()
    nbPlayers = ReadSavePlayers()
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
    ResetPlayerXp()
    list = ReadPlayerData()
    nbPlayers = ReadSavePlayers()
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

def GetTarget(playerList):
    targetNumber = Parent.GetRandom(0,len(playerList))
    return playerList[targetNumber]

def GetStreamerTeamData(logPath):
    ResetStreamerTeamData()
    list = []
    logRead = open(logPath, "r")
    log_list = logRead.readlines()
    logRead.close()
    for line in log_list:
        if line.count(m_LookForStreamerTeam) != 0:
            json = GetJsonLine2(line)
            list.append(json)
    nbTeamStrea = ReadStreamerTeamNumb()
    fromNb = nbTeamStrea
    if fromNb == len(list) :
        fromNb = 0
    for i in range (fromNb, len(list)):
        lineJson = ConvertToJson(list[i])
        WriteStreamerTeamData(str(lineJson['DisplayName']))
    WriteStreamerTeamNumb(len(list))
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
            ResetStats()
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
    stats = ReadStats()
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
    playerList = ReadPlayerName()
    teamMates1 = ReadStreamerTeamData()
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
                list = ReadPlayerName()
                target = GetTarget(list)
                message = "You must hunt " + str(target)
                Parent.SendTwitchMessage(message)
                return

            if data.GetParam(1).lower() == "protectcunt" or data.GetParam(1).lower() == "protect":
                list = ReadStreamerTeamData()
                target = GetTarget(list)
                message = "You must protect " + str(target)
                Parent.SendTwitchMessage(message)
                return

        if data.GetParam(0) == "!players":

            if (data.GetParamCount() == 1):
                players = ReadSavePlayers()
                answer = "There is " + str(players) + " players, including the streamer team."
                Parent.SendTwitchMessage(answer)
                return

            #Check if there is a new log and reset old players if yes
            if data.GetParam(1) == "init" and Parent.HasPermission(data.User, m_CommandPermission,"Get the most recent log file and reset if new one"):
                lastest = LastestFile()
                lastestMemory = GetLastestFile()
                if (lastest != lastestMemory):
                    WriteLastestFile(lastest)
                    ResetOldPlayers()
                    Parent.SendTwitchMessage("Old players reset")
                ResetSavePlayers()
                ResetPlayers()
                Parent.SendTwitchMessage("Init done")
                return

            if data.GetParam(1) == "update" and Parent.HasPermission(data.User, m_CommandPermission,"Get the amount of player in your lobby"):
                path = LastestFile()
                totPlayers = GetLogPLayers(path)
                ChangePlayers(totPlayers)
                players = StartPlayers() + ReadSavePlayers()
                answer = "There is " + str(players) + " players, including your team."
                ChangeSavePlayers(players)
                ChangeOldPlayers(totPlayers)
                Parent.SendTwitchMessage(answer)
                return

            if (data.GetParam(1) == "newGame" or data.GetParam(1) == "ng") and Parent.HasPermission(data.User, m_CommandPermission,"Reset players and old players"):
                path = LastestFile()
                totPlayers = GetLogPLayers(path)
                ChangePlayers(totPlayers)
                players = StartPlayers()
                if players != 0:
                    answer = "There is " + str(players) + " players, including your team."
                    ChangeOldPlayers(totPlayers)
                    GetStreamerTeamData(path)
                    Parent.SendTwitchMessage(answer)
                    DoStats()
                    ResetPlayerData()
                else:
                    Parent.SendTwitchMessage("You are still in the same match")
                return

            if data.GetParam(1) == "reset" and Parent.HasPermission(data.User, m_CommandPermission,"Reset players and old players"):
                ResetPlayers()
                ResetOldPlayers()
                ResetSavePlayers()
                ResetPlayerData()
                ResetPlayerName()
                Parent.SendTwitchMessage("reset done")
                return

            if data.GetParam(1) == "xp":
                path = LastestFile()
                FoundPlayersInfo(path)
                WrotePlayersXP()
                list = ReadPlayerXp()
                Parent.SendTwitchMessage(str(list).replace(r"\n", ""))
                return

            if data.GetParam(1) == "solo":
                path = LastestFile()
                FoundPlayersInfo(path)
                WrotePlayersRank("GameModeInfo:DA_BattleRoyale_Solo")
                list = ReadPlayerXp()
                Parent.SendTwitchMessage(str(list).replace(r"\n", ""))
                return

            if data.GetParam(1) == "duo":
                path = LastestFile()
                FoundPlayersInfo(path)
                WrotePlayersRank("GameModeInfo:DA_BattleRoyale_Duo")
                list = ReadPlayerXp()
                Parent.SendTwitchMessage(str(list).replace(r"\n", ""))
                return

            if data.GetParam(1) == "squad":
                path = LastestFile()
                FoundPlayersInfo(path)
                WrotePlayersRank("GameModeInfo:DA_BattleRoyale_Squad")
                list = ReadPlayerXp()
                Parent.SendTwitchMessage(str(list).replace(r"\n", ""))
                return

            if data.GetParam(1) == "name":
                path = LastestFile()
                FoundPlayersInfo(path)
                WrotePlayersName()
                list = ReadPlayerName()
                Parent.SendTwitchMessage(str(list).replace(r"\n", ""))
                return

            if data.GetParam(1) == "team":
                list = ReadStreamerTeamData()
                Parent.SendTwitchMessage(str(list).replace(r"\n", ""))
                return

            if data.GetParam(1) == "stat" and Parent.HasPermission(data.User, "broadcaster","Reset players and old players"):
                path = LastestFile()
                GetStreamerTeamData(path)
                DoStats()
                return

            if data.GetParam(1) == "resetstat" and Parent.HasPermission(data.User, "broadcaster","Reset players and old players"):
                ResetStats()
                Parent.SendTwitchMessage("reset stat done")
                return

            if data.GetParam(1) == "fullReset" and Parent.HasPermission(data.User, "broadcaster","Reset players and old players"):
                ResetPlayers()
                ResetStreamerTeamData()
                ResetPlayerData()
                ResetPlayerName()
                ResetPlayerXp()
                ResetSavePlayers()
                ResetOldPlayers()
                ResetStreamerTeamNumb()
                ResetStreamerTeamData()
                ResetStreamerTeamNumb()
                Parent.SendTwitchMessage("Full reset done")
                return




        return
    return


def Tick():
    return