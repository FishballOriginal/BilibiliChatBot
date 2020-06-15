import time
import json
import threading
import os

from ChatBehaviour import ChatBehaviour
import ChatEngineFunctions.ChatSession as ChatSession
import ChatEngineFunctions.ChatEngine as ChatEngine
from ChatEngineFunctions.SessionDataIO import SessionDataIO

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
            handleSession = SessionDataIO().SessionRecordLoad(handleSession, self.sessionRecordPath, self.defaultSessionData)

            print('session ' + str(handleSession.talker_id) + '\'s session data:\n' + str(handleSession.sessionRecordData))
            
            # a list of chat history
            newChatHistory = []
            # get session chat history from 'handleSession.sessionRecordData['latestSeqno']'
            for history in handleSession.GetChatHistory(handleSession.sessionRecordData['latestSeqno']):
                newChatHistory.append(json.loads(history['content'])['content'])
            print(newChatHistory)
            
            # check if target senetnce in the new message list
            if ('测试语句1' in newChatHistory):
                handleSession.SendMessage("收到消息“测试语句1”，自动回复")
                # add seqno because we replied 1 message
                handleSession.latest_seqno += 1
            
            # write latestSeqno data back to dictionary and save it into session data
            handleSession.sessionRecordData['latestSeqno'] = handleSession.latest_seqno
            SessionDataIO().SessionRecordSave(handleSession, self.sessionRecordPath, self.defaultSessionData)
    
    # ==================== SESSION DATA OPERATION ====================


chatBehaviour = TestBehaviour()