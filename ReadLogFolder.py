import json, os


def readLogFileJSONWay(fileName):
    successCount = failCount = emptyAuthCount = 0
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
    print('Final Result is: ')
    print('Successful FaceAuth Count:', sum(count[0]))
    print('Failed FaceAuth Count:', sum(count[1]))
    print('Empty FaceAuth Count:', sum(count[2]))
    print('Error Count is:')
    print('<ErrorCode>  -------------- <Count of the Error> ')
    for keys, values in dictErrorCount.items():
        print(keys, ' has error count of ', values)


def main():
    date = input('Enter the date of logs :')
    #logFilesPerIP = input('Enter the number of log Files per machine :')
    machines = ['100.65.137.166', '100.65.137.167', '100.65.137.168', '100.65.137.169', '100.65.137.177',
                '100.65.137.178', '100.65.137.179', '100.65.137.180']
    fileNameString = []
    for (root,dirs,files) in os.walk(r'E:\Learning700\{}'.format(date), topdown=True):
        for file in files:
            fileNameString.append(r'{}\{}'.format(root, file))
    result = []

    global dictErrorCount
    dictErrorCount = {}
    i = 0
    totalNumofFiles = len(fileNameString)
    for file in fileNameString:
        i = i + 1
        print('(', i, ')', ' of ', totalNumofFiles, 'Working on file = ', file)
        result.append(readLogFileJSONWay(file))
    countResultZipObj = zip(result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7],
                            result[8], result[9], result[10], result[11], result[12], result[13], result[14],
                            result[15])
    countResultList = list(countResultZipObj)
    printResult(countResultList)


if __name__ == '__main__':
    main()
