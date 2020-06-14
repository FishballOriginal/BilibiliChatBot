import time
import json
import threading
import os

import ChatEngineFunctions.ChatSession as ChatSession
import ChatEngineFunctions.ChatEngine as ChatEngine
from ChatBehaviour import ChatBehaviour

class TestBehaviour(ChatBehaviour):

    # ==================== ATTRIBUTE ====================

    def __init__(self):
        # attribute of base class
        ChatBehaviour.__init__(self)

        # session which the behaviour is currently handling
        self.handlingSessions = []

        # session data

        self.sessionRecordPath = os.getcwd() + '\\SessionData'
        self.defaultSessionData = {
            'latestSeqno' : 0
        }
    
    # ==================== LIFE CYCLE ====================

    # called once when the module is loaded at the start of the whole program
    def Activate(self):
        print('Test Behaviour Activated')
    
    # called every time when the main loop execute, before every other functions
    def Update(self):
        print(time.asctime())
        # print(self.newChatSessions)
    
    # ==================== CALLBACK FUNCTIONS ====================
    
    # called when receive new message
    def OnMessageReceive(self):
        print('New Message Receive!')
        print('active threading: ' + str(threading.active_count()))
        
        self.OperateNewSessions()

    

    # ==================== OPERATE ALL NEW SESSIONS ====================

    def OperateNewSessions(self):
        # ergodic all the new sessions
        for session in self.newChatSessions:

            # initialize session
            handleSession = ChatSession.ChatSession(self.headers, session, self.UID)
            # load session data
            handleSession = self.SessionRecordLoad(handleSession)

            print('session ' + str(handleSession.talker_id) + '\'s session data:\n' + str(handleSession.sessionRecordData))
            
            # print(session)
            # a list of chat history
            newChatHistory = []
            for history in handleSession.GetChatHistory(handleSession.sessionRecordData['latestSeqno']):
                newChatHistory.append(json.loads(history['content'])['content'])
            print(newChatHistory)
            
            # check if target senetnce in the new message list
            if ('测试语句1' in newChatHistory):
                handleSession.SendMessage("收到消息“测试语句1”，自动回复")
            
            handleSession.sessionRecordData['latestSeqno'] = handleSession.latest_seqno
            self.SessionRecordSave(handleSession)
    
    # ==================== SESSION DATA OPERATION ====================
    
    def SessionRecordLoad(self, chatSession):
        # get the session data folder
        if ('SessionData' in os.listdir(os.getcwd())):
            talker_id = str(chatSession.talker_id)

            # current session's data file exist, load the file
            if (talker_id + '.txt' in os.listdir(self.sessionRecordPath)):
                with open(self.sessionRecordPath + '\\' + talker_id + '.txt ', 'r') as sessionRecordFile:
                    chatSession.LoadSessionRecord(sessionRecordFile.read())
            
            # current session's data file doesn't exist, create one, load current data file with default session record data
            else:
                with open(self.sessionRecordPath + '\\' + talker_id + '.txt ', 'w') as sessionRecordFile:
                    pass
                chatSession.sessionRecordData=self.defaultSessionData
            
            self.SessionRecordSave(chatSession)
            
            return chatSession
        
        # data folder doesn't exist, create one
        else:
            os.mkdir(self.sessionRecordPath)
            return self.SessionRecordLoad(chatSession)
    
    def SessionRecordSave(self, chatSession):
        # get the session data folder
        if ('SessionData' in os.listdir(os.getcwd())):
            talker_id = str(chatSession.talker_id)

            # write session data to the file
            with open(self.sessionRecordPath + '\\' + talker_id + '.txt ', 'w') as sessionRecordFile:
                sessionRecordFile.write(json.dumps(chatSession.sessionRecordData))
            
            return chatSession
        
        # data folder doesn't exist, create one
        else:
            os.mkdir(self.sessionRecordPath)
            self.SessionRecordLoad(chatSession)


chatBehaviour = TestBehaviour()