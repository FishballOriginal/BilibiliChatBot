import requests
import json
import time
import re
from bs4 import BeautifulSoup

import ChatEngineFunctions.HeaderTransfer as HeaderTransfer

'''
CLASS: ChatSession -- A class that handle the chat session with on specific user

ATTRIBUTE: session, headers. talker_id, latest_seqno, selfUID, sessionRecordData

session -- the session info of the current ChatSession
headers -- headers of API 'https://api.vc.bilibili.com/svr_sync/v1/svr_sync/fetch_session_msgs'
talker_id -- the UID of the talker you currently want to get
latest_seqno -- the latest chat seqno info, used to determine the statrt of GetChatHistory()
selfUID -- your own UID
sessionRecordData -- the extend data saved in the session(disctionary), you can customize data in the session

METHOD: GetChatHistory, SendMessage, LoadSessionRecord

GetChatHistory -- Get the chat history with current user within specific seqno
SendMessage -- A function that send message to the current user
LoadSessionRecord -- A function that load the json string into sessionRecordData

HISTORY:
14/6/2020 Fangjun Zhou : Create
'''
class ChatSession:

    def __init__(self, headersIn, sessionIn, selfUIDIn):

        # API Info
        self.session = sessionIn
        self.headers = headersIn
        self.talker_id = sessionIn['talker_id']
        self.latest_seqno = sessionIn['last_msg']['msg_seqno']
        self.selfUID = selfUIDIn

        # session record
        self.sessionRecordData = {}

    '''
    METHOD: GetChatHistory -- Method that get the chat history with specific user within specific span

    INPUT: talker_id, begin_seqno, headers

    begin_seqno -- the start message index of the history you want to get.
        the earlier message will have a smaller index.
        for example, the first message's index is 1
        however, let begin_seqno equals to 0 went you want to get the history from the first message to the current one

    OUTPUT: messages

    message -- a list of all the message you got
    elements in 'message' -- a dictionary wich contains sender_uid, receiver_type, receiver_id, msg_type, content, msg_seqno, time_stamp, msk_key, msg_status, notify_code
        sender_uid -- the UID of the sender of this message
        receiver_id -- the UID of the receiver of the message, usually is your own UID
        content -- the main text of the message, also the most important part
        msg_seqno -- the seqno of the message
        time_stamp -- the time stamp(UNIX TIMESTAMP) when the message was sent

    HISTORY:
    13/6/2020 Fangjun Zhou : Create
    '''
    def GetChatHistory(self, begin_seqno):
        # API to get specific chat history with a certain user
        # direct the user through 'talker_id'
        # designate the start of the histor through 'begin_seqno'
        url = 'https://api.vc.bilibili.com/svr_sync/v1/svr_sync/fetch_session_msgs' + '?talker_id=' + str(self.talker_id) + '&session_type=1' + '&begin_seqno=' + str(begin_seqno)

        # chat history response
        getChatRes = requests.get(url, headers=self.headers)
        getChatRes.encoding = 'utf-8'
        print("Get chat response:" + getChatRes.text)

        # json resolve
        chatHistoryJson = json.loads(getChatRes.text)

        messages = chatHistoryJson['data']['messages']

        return messages

    '''
    METHOD : SendMessage -- A function that send message to the current user

    INPUT : message

    message -- text message to send(string)

    OUTPUT : messageSendResponse

    messageSendResponse -- http respons with post requests to send_msg API

    HISTORY:
    14/5/2020 Fangjun Zhou : Create
    '''
    
    def SendMessage(self, message):
        url = 'https://api.vc.bilibili.com/web_im/v1/web_im/send_msg'

        # use regex to extract csrf modification code
        csrfCode = re.findall(r'bili_jct=(.+);', json.dumps(self.headers))[0]
        print('csrfCode extracted')

        formData = {
            'msg[sender_uid]': self.selfUID,
            'msg[receiver_id]': self.talker_id,
            'msg[receiver_type]': '1',
            'msg[msg_type]': '1',
            'msg[msg_status]': '0',
            'msg[content]': '{\"content\":\"' + message + '\"}',
            'msg[timestamp]': str(time.time),
            'msg[dev_id]': '3A978B3B-9F97-4B9A-B35C-F472129BD033',
            'build': '0',
            'mobi_app': 'web',
            'csrf_token': str(csrfCode),
        }

        messageSendResponse = requests.post(url, formData, headers=self.headers)
        print('Send message response:' + messageSendResponse.text)

        return messageSendResponse
    
    '''
    METHOD : LoadSessionRecord -- A function that load the json string into sessionRecordData

    INPUT : jsonText

    jsonText -- json string that stores all the session data, usually store in a text file and load it when needed

    OUTPUT : None

    HISTORY:
    14/5/2020 Fangjun Zhou : Create
    '''

    def LoadSessionRecord(self, jsonText):
        self.sessionRecordData = json.loads(str(jsonText))