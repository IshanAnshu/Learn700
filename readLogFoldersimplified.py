import json, os, sys
successCount =0
failCount =0
emptyAuthCount =0
dictErrorCount = {}

def readLogFileJSONWay(fileName):
    global successCount, failCount , emptyAuthCount, dictErrorCount
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
                elif (logJson['AuthType'] == 'FID' and logJson['Status'] == 'success') or (
                        logJson['AuthType'] == 'FID' and logJson['Status'] == 'Y'):
                    successCount = successCount + 1
                elif logJson['AuthType'] == '':
                    emptyAuthCount = emptyAuthCount + 1
    return (successCount, failCount, emptyAuthCount)


def printResult(count):
    global successCount, failCount, emptyAuthCount, dictErrorCount
    print('Final Result is: ')
    print('Successful FaceAuth Count:', count[0])
    print('Failed FaceAuth Count:', count[1])
    print('Empty FaceAuth Count:', count[2])
    print('Error Count is:')
    print('<ErrorCode>  -------------- <Count of the Error> ')
    for keys, values in dictErrorCount.items():
        print(keys, ' has error count of ', values)
    successCount = 0
    failCount = 0
    emptyAuthCount = 0
    dictErrorCount = {}

def main():
    n = len(sys.argv)
    for i in range(1, n):
        fileNameString = []
        for (root,dirs,files) in os.walk(r'E:\Learning700\{}'.format(sys.argv[i]), topdown=True):
            for file in files:
                fileNameString.append(r'{}\{}'.format(root, file))
        i2 = 0
        totalNumofFiles = len(fileNameString)
        for file in fileNameString:
            i2 = i2 + 1
            print('(', i2, ')', ' of ', totalNumofFiles, 'Working on file = ', file)
            readLogFileJSONWay(file)
        printResult((successCount,failCount,emptyAuthCount))


if __name__ == '__main__':
    main()
