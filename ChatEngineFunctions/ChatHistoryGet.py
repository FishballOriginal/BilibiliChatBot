import requests
import json
from bs4 import BeautifulSoup

'''
METHOD: GetChatHistory -- Method that get the chat history with specific user within specific span

INPUT: talker_id, begin_seqno, headers

talker_id -- the UID of the talker you currently want to get
begin_seqno -- the start message index of the history you want to get.
    the earlier message will have a smaller index.
    for example, the first message's index is 1
    however, let begin_seqno equals to 0 went you want to get the history from the first message to the current one
headers -- headers of API 'https://api.vc.bilibili.com/svr_sync/v1/svr_sync/fetch_session_msgs'

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
def GetChatHistory(talker_id, begin_seqno, headers):
    # API to get specific chat history with a certain user
    # direct the user through 'talker_id'
    # designate the start of the histor through 'begin_seqno'
    url = 'https://api.vc.bilibili.com/svr_sync/v1/svr_sync/fetch_session_msgs' + '?talker_id=' + talker_id + '&session_type=1' + '&begin_seqno=' + begin_seqno

    # chat history response
    getChatRes = requests.get(url, headers=headers)
    getChatRes.encoding = 'utf-8'

    # json resolve
    chatHistoryJson = json.loads(getChatRes.text)

    messages = chatHistoryJson['data']['messages']

    return messages