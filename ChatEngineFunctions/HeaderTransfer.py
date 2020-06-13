import json

'''
METHOD: TransferHeader -- Method that transfer your header to a dictionary

INPUT: header

header -- the original header in string format

OUTPUT: headerOutput

headerOutput -- header in dictionary format

HISTORY:
14/6/2020 Fangjun Zhou : Create
'''

def TransferHeader(header):
    headerElementList = header.split('\n')

    del headerElementList[0]
    del headerElementList[len(headerElementList) - 1]

    headerOutputString = '{\n'

    #遍历每个key和value
    for element in headerElementList:
        keynValue = element.split(': ')
        headerOutputString += "\"" + keynValue[0] + "\": \"" + keynValue[1] + "\",\n"

    headerOutputString = headerOutputString[:len(headerOutputString)-2]
    headerOutputString += '\n}'

    headerOutput = json.loads(headerOutputString)

    return headerOutput
