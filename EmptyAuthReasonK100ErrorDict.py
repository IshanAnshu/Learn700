import json, os, sys, xml.etree.ElementTree as ET, base64
successCount =0
failCount =0
emptyAuthCount =0
dictErrorCount = {}
dictEmptyAuthReasonCount = {}
dictK100Types = {}


def readLogFileJSONWay(fileName):
    global successCount, failCount , emptyAuthCount, dictErrorCount, dictEmptyAuthReasonCount, dictK100Types
    logFile = open(fileName, 'r')
    for line in logFile:
        logJsonArr = line.split()[5:]
        JsonStr = " ".join(logJsonArr)
        if len(JsonStr) > 0 and JsonStr[0] == '{':
            logJson = json.loads(JsonStr)
            # print(logJson)
            if logJson.get('AuthType') != None:
                if (logJson['AuthType'] == 'FID' and logJson['Status'] == 'failed') or (
                        logJson['AuthType'] == 'FID' and logJson['Status'] == 'N'):
                    failCount = failCount + 1
                    if logJson['ErrorCode'] in dictErrorCount.keys():
                        dictErrorCount[logJson['ErrorCode']] = dictErrorCount[logJson['ErrorCode']] + 1
                    else:
                        dictErrorCount[logJson['ErrorCode']] = 1
                    if logJson['ErrorCode'] == "K-100":
                        root = ET.fromstring(logJson["ResponseXML"])
                        origRar = ""
                        for child in root:
                            if child.tag == "Rar":
                                origRar = child.text
                        RarDecoded = base64.b64decode(origRar)
                        try:
                            root = ET.fromstring(RarDecoded)
                            K100Err = root.attrib["err"]
                        except:
                            print('', end='')
                        else:
                            if K100Err in dictK100Types:
                                dictK100Types[K100Err] += 1
                            else:
                                dictK100Types[K100Err] = 1
                elif (logJson['AuthType'] == 'FID' and logJson['Status'] == 'success') or (
                        logJson['AuthType'] == 'FID' and logJson['Status'] == 'Y'):
                    successCount = successCount + 1
                elif logJson['AuthType'] == '':
                    emptyAuthCount = emptyAuthCount + 1
                    if logJson['Reason'] in dictEmptyAuthReasonCount.keys():
                        dictEmptyAuthReasonCount[logJson['Reason']] = dictEmptyAuthReasonCount[logJson['Reason']] + 1
                    else:
                        dictEmptyAuthReasonCount[logJson['Reason']] = 1
    return (successCount, failCount, emptyAuthCount)


def printResult(count):
    global successCount, failCount, emptyAuthCount, dictErrorCount, dictEmptyAuthReasonCount, dictK100Types
    print('\n\nFinal Result is: ')
    print('Successful FaceAuth Count:', count[0])
    print('Failed FaceAuth Count:', count[1])
    print('Empty FaceAuth Count:', count[2])
    print('\n\nError Count is:')
    print('<ErrorCode>  -------------- <Count of the Error> ')
    for keys, values in dictErrorCount.items():
        print(keys, '----------->> has error count of ------------>>', values)
    print('\n\nEmpty AuthType Reason Count is:')
    print('<Reason>  -------------- <Count of the Reason> ')
    for keys, values in dictEmptyAuthReasonCount.items():
        print(keys, '-------------->> has reason count of ----------->>', values)
    print('\n\n<K-100 Error Type>  -------------- <Count of the Error Type> ')
    for keys, values in dictK100Types.items():
        print(keys, '-------------->> has count of ----------->>', values)

    successCount = 0
    failCount = 0
    emptyAuthCount = 0
    dictErrorCount = {}
    dictEmptyAuthReasonCount = {}
    dictK100Types = {}


def main():
    n = len(sys.argv)

    for i in range(1, n):
        fileNameString = []
        cwd = os.getcwd()
        for (root,dirs,files) in os.walk(r'{}/{}'.format(cwd,sys.argv[i]), topdown=True):
            for file in files:
                fileNameString.append(r'{}/{}'.format(root, file))
        i2 = 0
        totalNumofFiles = len(fileNameString)
        for file in fileNameString:
            i2 = i2 + 1
            print('(', i2, ')', ' of ', totalNumofFiles, 'Working on file = ', file)
            readLogFileJSONWay(file)
        printResult((successCount,failCount,emptyAuthCount))


if __name__ == '__main__':
    main()
