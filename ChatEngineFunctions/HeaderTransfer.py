
def TransferHeader(header):
    headerElementList = header.split('\n')

    del headerElementList[0]
    del headerElementList[len(headerElementList) - 1]

    headerOutput = '{\n'

    #遍历每个key和value
    for element in headerElementList:
        keynValue = element.split(': ')
        headerOutput += "\"" + keynValue[0] + "\": \"" + keynValue[1] + "\",\n"

    headerOutput = headerOutput[:len(headerOutput)-2]
    headerOutput += '\n}'

    return headerOutput
