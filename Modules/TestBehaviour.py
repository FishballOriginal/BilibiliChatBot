import time
import json

import ChatEngineFunctions.ChatSession as ChatSession
import ChatEngineFunctions.ChatEngine as ChatEngine
from ChatBehaviour import ChatBehaviour

class TestBehaviour(ChatBehaviour):

    def __init__(self):
        # attribute of base class
        ChatBehaviour.__init__(self)

        self.handlingSessions = []
        self.UID = '15654501'

    # called once when the module is loaded at the start of the whole program
    def Activate(self):
        print('Test Activate')
    
    # called every time when the main loop execute, before every other functions
    def Update(self):
        print(time.asctime())
        # print(self.newChatSessions)
    
    # called when receive new message
    def OnMessageReceive(self):
        print('New Message Receive!')
        for session in self.newChatSessions:
            # print(session)
            handleSession = ChatSession.ChatSession(self.headers, session['talker_id'], self.UID)
            if (json.loads(handleSession.GetChatHistory(0)[0]['content'])['content'] == '测试语句1'):
                handleSession.SendMessage("收到消息“测试语句1”，自动回复")


chatBehaviour = TestBehaviour()