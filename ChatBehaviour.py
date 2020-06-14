import requests
import json
from bs4 import BeautifulSoup

'''
CLASS: ChatBehaiour


ATTRIBUTES:
chatSessions -- all the chat sessions the main program currently holds


METHODS:
Activate -- the callback function that being called after the module has been loaded

Update -- called every life cycle before every other functions

LateUpdate -- called every life cycle after every other functions

OnMessageReceive -- called when new message is received


HISTORY:
14/6/2020 Fangjun Zhou : Create
'''
class ChatBehaviour:

    # attributes of ChatBehaviour
    def __init__(self):
        # work Directory
        self.dataPath = ''

        # the main header of the program
        self.headers = {}

        # all the chat sessions the main program is currently processing
        self.chatSessions = []
        self.newChatSessions = []
    
    # called once when the module is loaded at the start of the whole program
    def Activate(self):
        pass

    # called every time when the main loop execute, before every other functions
    def Update(self):
        pass
    
    # called every time when the main loop execute, after every other functions
    def LateUpdate(self):
        pass

    
    # called when new messages are received
    def OnMessageReceive(self):
        pass