import sys, os
import json

class SessionDataIO:
    '''
    METHOD : SessionRecordLoad -- Method that load session data from json file

    INPUT : chatSession, sessionRecordPath, defaultSessionData

    chatSession -- the session object that pass into the method
    sessionRecordPath -- the path of json data
    defaultSessionData -- if there's no json file in the data folder, create one with default session data

    OUTPUT : chatSession

    chatSession -- session object that successfully load session data

    HISTORY:
    15/6/2020 Fangjun Zhou : Create
    '''
    def SessionRecordLoad(self, chatSession, sessionRecordPath, defaultSessionData):
        # get the session data folder
        if ('SessionData' in os.listdir(os.getcwd())):
            talker_id = str(chatSession.talker_id)

            # current session's data file exist, load the file
            if (talker_id + '.txt' in os.listdir(sessionRecordPath)):
                with open(sessionRecordPath + '\\' + talker_id + '.txt ', 'r') as sessionRecordFile:
                    chatSession.LoadSessionRecord(sessionRecordFile.read())
            
            # current session's data file doesn't exist, create one, load current data file with default session record data
            else:
                with open(sessionRecordPath + '\\' + talker_id + '.txt ', 'w') as sessionRecordFile:
                    pass
                chatSession.sessionRecordData=defaultSessionData
            
            self.SessionRecordSave(chatSession, sessionRecordPath, defaultSessionData)
            
            return chatSession
        
        # data folder doesn't exist, create one
        else:
            os.mkdir(sessionRecordPath)
            return self.SessionRecordLoad(chatSession, sessionRecordPath, defaultSessionData)

    '''
    METHOD : SessionRecordSave

    INPUT : chatSession, sessionRecordPath, defaultSessionData

    chatSession -- session that you want to save session data
    sessionRecordPath -- data path of target session
    defaultSessionData -- if there's no data file of target session, create one with default session data

    OUTPUT : chatSession

    chatSession -- original chat session

    HISTORY:
    15/6/2020 Fangjun Zhou : Create
    '''

    def SessionRecordSave(self, chatSession, sessionRecordPath, defaultSessionData):
        # get the session data folder
        if ('SessionData' in os.listdir(os.getcwd())):
            talker_id = str(chatSession.talker_id)

            # write session data to the file
            with open(sessionRecordPath + '\\' + talker_id + '.txt ', 'w') as sessionRecordFile:
                sessionRecordFile.write(json.dumps(chatSession.sessionRecordData))
            
            return chatSession
        
        # data folder doesn't exist, create one
        else:
            os.mkdir(sessionRecordPath)
            self.SessionRecordLoad(chatSession, sessionRecordPath, defaultSessionData)