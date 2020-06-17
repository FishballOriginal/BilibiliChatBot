import requests
from bs4 import BeautifulSoup
import re
import json
import time


class UserInfoTracker:
    
    '''
    METHOD : GetUserName -- A method to get user's user name with certain UID

    INPUT : UID

    UID -- the UID of target user

    OUTPUT : userName

    userName -- user name(string) of target user

    HISTORY:
    17/6/2020 Fangjun Zhou : Create
    '''
    def GetUserName(self, UID):
        url = 'https://space.bilibili.com/' + str(UID)

        urlResponse = requests.get(url)

        # resolve html into beautiful soup
        soup = BeautifulSoup(urlResponse.text, 'lxml')

        content = soup.find('meta', {'name': 'description'})['content']

        # regex find all chinese characters, english characters and numbers
        pattern =re.compile(u"([\u4e00-\u9fa5_a-zA-Z0-9]+)，")
        userName = re.findall(pattern, content)[0]

        return userName
    
    '''
    METHOD : GetUserFollowStatus -- A Method to get the relationship status between you and certain user

    INPUT : headers, UID

    header -- the request header
    UID -- the UID of target user

    OUTPUT : relationshipStatus

    relationshipStatus -- the relationship between you and certain user
        relationshipStatus=2 -- the user didn't followed you
        relationshipStatus=6 -- the user is following you

    HISTORY:
    17/6/2020 Fangjun Zhou : Create
    '''
    def GetUserFollowStatus(self, headers, UID):
        # userRelation API and userRelation modify API
        userRelationUrl = 'https://api.bilibili.com/x/relation' + '?fid=' + str(UID)
        userRelationModifyUrl = 'https://api.bilibili.com/x/relation/modify'

        # get user relation before modify
        responseBeforeFollow = requests.get(userRelationUrl, headers=headers)
        dataBeforeFollow = json.loads(responseBeforeFollow.text)
        relationshipBeforeFollow = dataBeforeFollow['data']['attribute']
        print('Relationship before follow operation:' + str(relationshipBeforeFollow))
        
        # unfollow only if not following before
        if (str(relationshipBeforeFollow) == '0'):

            # use regex to extract csrf modification code
            csrfCode = re.findall(r'bili_jct=(.+);', json.dumps(headers))[0]
            print('csrfCode extracted')
            # construct form data
            followFormData = {
                'fid': str(UID),
                'act': '1',
                're_src': '11',
                'jsonp': 'jsonp',
                'csrf': str(csrfCode)
            }
            # post modify data to userRelationModifyUrl
            responseFollow = requests.post(userRelationModifyUrl, data=followFormData, headers=headers)
            print(responseFollow)
            print(responseFollow.text)

            # sleep for 3 seconds for server to response
            print('Wait for server to response...')
            time.sleep(3)

            # check relation status again to check the relationship
            responseAfterFollow = requests.get(userRelationUrl, headers=headers)
            dataAfterFollow = json.loads(responseAfterFollow.text)
            relationshipAfterFollow = dataAfterFollow['data']['attribute']
            print ('Relationship before follow operation:' + str(relationshipAfterFollow))
        
            unfollowFormData = {
                'fid': str(UID),
                'act': '2',
                're_src': '11',
                'jsonp': 'jsonp',
                'csrf': str(csrfCode)
            }
            # post unfollow modify data to userRelationModifyUrl
            responseUnfollow = requests.post(userRelationModifyUrl, data=unfollowFormData, headers=headers)
            print(responseUnfollow)
            print(responseUnfollow.text)

            if str(relationshipAfterFollow) == '2':
                return 2
            elif str(relationshipAfterFollow) == '6':
                return 6


        else:
            
            print('Already following, stop unfollowing')

            if str(relationshipBeforeFollow) == '2':
                return 2
            elif str(relationshipBeforeFollow) == '6':
                return 6
