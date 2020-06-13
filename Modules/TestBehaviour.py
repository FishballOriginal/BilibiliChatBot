from ChatBehaviour import ChatBehaviour

class TestBehaviour(ChatBehaviour):

    # called once when the module is loaded at the start of the whole program
    def Activate(self):
        print('Test Activate')
    
    # called every time when the main loop execute, before every other functions
    def Update(self):
        pass

chatBehaviour = TestBehaviour()