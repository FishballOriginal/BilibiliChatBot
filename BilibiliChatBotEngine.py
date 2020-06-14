import time
import os, sys

import requests
import json

from bs4 import BeautifulSoup

import ChatEngineFunctions.SessionGet as SessionGet
import ChatEngineFunctions.ChatSession as ChatSession
import ChatEngineFunctions.HeaderTransfer as HeaderTransfer
import ChatEngineFunctions.ChatEngine as ChatEngine

'''
=====MAIN FUNCTION OF BILIBILI CHAT BOT=====



'''

# ==================== VARIABLES ====================

# the total time from the start of the main loop
totalTime = 0
# delta time betweem two main loop
deltaTime = 1
# time interval between two session checks
sessionCheckTime = 5

# root folder path of all the headers
headersPathRoot = os.getcwd() + '\\Headers\\'
# headers to get sessions
requestHeaders = {}

# root folder path of all the modules
modulePathRoot = os.getcwd() + '\\Modules\\'
# all the modules(ChatBehaviour objects)
chatBehaviours = []

# root folder path of other program data
dataPathRoot = os.getcwd() + '\\Data\\'


# the latest session's time stamp recorded in the last updated
latestSessionTS = 0
# stores all the chat sessions in the list
allChatSessions = []

# the user's UID

selfUid = ''


# ==================== PROGRAM INITIALIZE ====================

# load all the headers in the Headers folder
# the headers file should be saved in the Header.txt
def LoadHeaders():
    global headersPathRoot
    global requestHeaders

    headersFileLits = os.listdir(headersPathRoot)

    # load header
    if 'Header.txt' in headersFileLits:
        with open(headersPathRoot + 'Header.txt', 'r') as sessionHeaderFile:
            requestHeaders = HeaderTransfer.TransferHeader(sessionHeaderFile.read())

def LoadUID():
    global dataPathRoot
    global selfUid

    # get all the data file in the Data folder
    dataFileList = os.listdir(dataPathRoot)

    # load user's UID
    if 'SelfUID.txt' in dataFileList:
        with open(dataPathRoot + 'SelfUID.txt', 'r') as uidFile:
            selfUid = int(uidFile.read())

# load all the modules in the Modules folder
def LoadModules():
    global modulePathRoot
    global chatBehaviours

    # get all the module file in the Modules folder
    moduleList = os.listdir(modulePathRoot)

    # ergodic all the module file name and load the module
    for moduleFileName in moduleList:
        if moduleFileName[len(moduleFileName) - 3:] == '.py':
            # add the path to sys in order to import module dynamically
            sys.path.append(modulePathRoot)
            module = __import__(moduleFileName[:len(moduleFileName) - 3])
            
            if hasattr(module, 'chatBehaviour'):
                chatBehaviours.append(getattr(module, 'chatBehaviour'))

# load the lastes session's time stamp into 'latestSessionTS'
def LoadLatestSessionTS():
    global dataPathRoot
    global latestSessionTS

    # get all the data file in the Data folder
    dataFileList = os.listdir(dataPathRoot)

    # load latest chat session's time stamp
    if 'LatestSessionTS.txt' in dataFileList:
        with open(dataPathRoot + 'LatestSessionTS.txt', 'r') as sessionTSFile:
            latestSessionTS = int(sessionTSFile.read())

# save the latest session's time stamp into 'LatestSessionTS.txt'
def SaveLatestSessionTS():
    global latestSessionTS
    global dataPathRoot

    # get all the data file in the Data folder
    dataFileList = os.listdir(dataPathRoot)

    # load latest chat session's time stamp
    if 'LatestSessionTS.txt' in dataFileList:
        with open(dataPathRoot + 'LatestSessionTS.txt', 'w') as sessionTSFile:
            sessionTSFile.write(str(latestSessionTS))

# Initialize all the ChatBehaviour, including setup request headers, set data path
def ChatBehaviourInitialize():
    global requestHeaders
    global dataPathRoot

    # set headers for all the ChatBehaviour
    for chatBehaviour in chatBehaviours:
        chatBehaviour.headers = requestHeaders
    
    for chatBehaviour in chatBehaviours:
        chatBehaviour.dataPath = dataPathRoot



# ==================== LIFE CYCLE FUNCTIONS ====================


# check all the new sessions happens after time 'latestSessionTS'
# return a list of all the new sessions
# all the elements in the list are the same as that in SessionGet.GetSession(header)[0] returns

def CheckNewSessions():
    global allChatSessions
    global latestSessionTS
    global selfUid

    newSessions = []

    # a list that stores all the new sessions happens after 'latestSessionTS' and exclude messages sent by ourselves
    for session in allChatSessions:
        if session['last_msg']['timestamp'] > latestSessionTS and str(session['last_msg']['sender_uid']) != str(selfUid):
            newSessions.append(session)
    
    latestSessionTS = allChatSessions[0]['last_msg']['timestamp']

    # rewrite latest session time stamp into ts file
    SaveLatestSessionTS()
    
    return newSessions



# ==================== MAIN FUNCTION ====================

def Loop():
    global requestHeaders
    global allChatSessions
    global sessionCheckTime
    
    # run the Update() of each ChatBehaviour
    for chatBehaviour in chatBehaviours:
        chatBehaviour.Update()
    
    # get all the sessions every 10 second
    if (totalTime % sessionCheckTime == 0):
        allChatSessions = SessionGet.GetSession(requestHeaders)[0]
        print('Got new session')
        for chatBehaviour in chatBehaviours:
            chatBehaviour.chatSessions = allChatSessions
    
    # check if there's new session, if so call the OnMessageReceive()
    newChatSessionsList = CheckNewSessions()
    # pass all the new chat sessions to ChatBehaviour
    for chatBehaviour in chatBehaviours:
        chatBehaviour.newChatSessions = newChatSessionsList
    if len(newChatSessionsList) != 0:
        for chatBehaviour in chatBehaviours:
            chatBehaviour.OnMessageReceive()

    # run the LateUpdate() of each ChatBehaviour
    for chatBehaviour in chatBehaviours:
        chatBehaviour.LateUpdate()

# the main function of the behaviour
def Main():
    global deltaTime
    global totalTime
    global latestSessionTS
    global requestHeaders

    # load all the headers
    LoadHeaders()
    # load the lastest session's time stamp
    LoadLatestSessionTS()
    # load the user's UID
    LoadUID()

    # load all the modules using reflect
    LoadModules()

    # initialize all the ChatBehaviour class
    ChatBehaviourInitialize()

    # run Activate() for all ChatBehaviours
    for chatBehaviour in chatBehaviours:
        chatBehaviour.Activate()
    
    # main loop of the program
    while True:
        Loop()

        time.sleep(deltaTime)
        totalTime += deltaTime

if __name__ == "__main__":
    Main()