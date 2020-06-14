import time
import os, sys

import requests
import json

from bs4 import BeautifulSoup

import ChatEngineFunctions.SessionGet as SessionGet
import ChatEngineFunctions.ChatHistoryGet as ChatHistoryGet
import ChatEngineFunctions.HeaderTransfer as HeaderTransfer

'''
=====MAIN FUNCTION OF BILIBILI CHAT BOT=====



'''

# ==================== VARIABLES ====================

# delta time betweem two main loop
deltaTime = 1

# root folder path of all the headers
headersPathRoot = os.getcwd() + '\\Headers\\'
# headers to get sessions
sessionHeaders = {}
# headers to get chat history
chatHistoryHeaders = {}

# root folder path of all the modules
modulePathRoot = os.getcwd() + '\\Modules\\'
# all the modules(ChatBehaviour objects)
chatBehaviours = []


# ==================== PRIVATE FUNCTIONS ====================

# load all the headers in the Headers folder
# session headers are saved in SessionHeader.txt
# chat history headers are saved in the ChatHistoryHeader.txt
def LoadHeaders():
    global sessionHeaders
    global chatHistoryHeaders

    headersFileLits = os.listdir(headersPathRoot)
    if 'SessionHeader.txt' in headersFileLits:
        with open(headersPathRoot + 'SessionHeader.txt', 'r') as sessionHeaderFile:
            sessionHeaders = HeaderTransfer.TransferHeader(sessionHeaderFile.read())
    if 'ChatHistoryHeader.txt' in headersFileLits:
        with open(headersPathRoot + 'ChatHistoryHeader.txt', 'r') as chatHistoryHeaderFile:
            chatHistoryHeaders = HeaderTransfer.TransferHeader(chatHistoryHeaderFile.read())

# load all the modules in the Modules folder
def LoadModules():
    global modulePathRoot

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


# ==================== MAIN FUNCTION ====================

def Loop():
    global sessionHeaders

    # run the Update() of each ChatBehaviour
    for chatBehaviour in chatBehaviours:
        chatBehaviour.Update()
    
    # get all the sessions
    SessionGet.GetSession(sessionHeaders)

    # run the LateUpdate() of each ChatBehaviour
    for chatBehaviour in chatBehaviours:
        chatBehaviour.LateUpdate()

# the main function of the behaviour
def Main():
    global deltaTime

    # load all the headers
    LoadHeaders()

    # load all the modules using reflect
    LoadModules()

    # run Activate() for all ChatBehaviours
    for chatBehaviour in chatBehaviours:
        chatBehaviour.Activate()
    
    # main loop of the program
    while True:
        Loop()

        time.sleep(deltaTime)

if __name__ == "__main__":
    Main()