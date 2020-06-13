import time
import os, sys

import requests
import json

from bs4 import BeautifulSoup

import ChatEngineFunctions.SessionGet, ChatEngineFunctions.ChatHistoryGet, ChatEngineFunctions.HeaderTransfer

'''
=====MAIN FUNCTION OF BILIBILI CHAT BOT=====



'''

# ==================== VARIABLES ====================

# delta time betweem two main loop
deltaTime = 1

# root folder path of all the modules
modulePathRoot = os.getcwd() + '\\Modules\\'
# all the modules(ChatBehaviour objects)
chatBehaviours = []


# ==================== PRIVATE FUNCTIONS ====================

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
    # run the Update() of each ChatBehaviour
    for chatBehaviour in chatBehaviours:
        chatBehaviour.Update()
    
    # get all the sessions

    # run the LateUpdate() of each ChatBehaviour
    for chatBehaviour in chatBehaviours:
        chatBehaviour.LateUpdate()

# the main function of the behaviour
def Main():
    global deltaTime

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