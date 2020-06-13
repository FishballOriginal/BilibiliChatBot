import requests
import json
from bs4 import BeautifulSoup

'''
METHOD: GetSession -- Method that get chat sessions and chat users' UID 

INPUT: headers

headers -- headers of API 'https://api.vc.bilibili.com/session_svr/v1/session_svr/get_sessions'

OUTPUT: [sessionList, talkerUIDList]

sessionList -- the json object of the whole session including talker_id, unread_count, last_msg
    talker_id -- the UID of the talker of this session
    unread_count -- the number of unreaded messages in this session
    last_message -- the data of the last message, including content, msg_seqno, timestamp
        content -- the main content text of the last message
        msg_seqno --  the last message's seqno index, compare this index with the latest seqno index you stored in your storage, you can tell how many new messages the sender sent
        timestamp -- the time stamp(UNIX TIMESTAMP) of the last message when it was sent
talkerUIDList -- a list of all the talkers' UID in the session

HISTORY:
12/6/2020 Fangjun Zhou : Create
13/6/2020 Fangjun Zhou : Change the name of the method to 'GetSession'
'''
def GetSession(headers):

    # API to get chat session
    url = 'https://api.vc.bilibili.com/session_svr/v1/session_svr/get_sessions?session_type=1&group_fold=1&unfollow_fold=0&sort_rule=2'

    # get the chat sessions
    getSessionRes = requests.get(url, headers=headers)
    getSessionRes.encoding = 'utf-8'

    # json resolve
    sessionJson = json.loads(getSessionRes.text)

    # get the session data
    # ATTENTION: session data are in the data/session_list node
    sessionList = sessionJson['data']['session_list']

    # get all the UID of sessions we got, we can use these UIDs to get chat histories
    talkerUIDList = []
    for session in sessionList:
        talkerUIDList.append(session['talker_id'])
    
    return [sessionList, talkerUIDList]