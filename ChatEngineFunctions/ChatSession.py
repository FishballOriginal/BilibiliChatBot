import requests
import json
import time
from bs4 import BeautifulSoup

import ChatEngineFunctions.HeaderTransfer as HeaderTransfer

'''
CLASS: ChatSession -- A class that handle the chat session with on specific user

ATTRIBUTE: headers. talker_id

headers -- headers of API 'https://api.vc.bilibili.com/svr_sync/v1/svr_sync/fetch_session_msgs'
talker_id -- the UID of the talker you currently want to get

METHOD: GetChatHistory

GetChatHistory -- Get the chat history with current user within specific seqno

HISTORY:
14/6/2020 Fangjun Zhou : Create
'''
class ChatSession:

    def __init__(self, headersIn, talker_idIn, selfUIDIn):
        self.headers = {}
        self.talker_id = ''
        self.selfUID = ''

        self.headers = headersIn
        self.talker_id = talker_idIn
        self.selfUID = selfUIDIn

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

        # json resolve
        chatHistoryJson = json.loads(getChatRes.text)


        messages = chatHistoryJson['data']['messages']

        return messages
    
    def SendMessage(self, message):
        url = 'https://api.vc.bilibili.com/web_im/v1/web_im/send_msg'

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
            'csrf_token': '50d81a6bc8ad02135bb493e129da9f56',
        }

        messageSendResponse = requests.post(url, formData, headers=self.headers)

        return messageSendResponse