import json

def readLogFileJSONWay(fileName):
    successCount = failCount = emptyAuthCount =0
    logFile = open(fileName, 'r')
    for line in logFile:
        logJsonArr = line.split()[5:]
        JsonStr = " ".join(logJsonArr)
        if len(JsonStr) > 0 and JsonStr[0] == '{':
            logJson = json.loads(JsonStr)
            #print(logJson)
            if logJson.get('AuthType')!=None:
                if (logJson['AuthType']=='FID' and logJson['Status']=='failed') or (logJson['AuthType']=='FID' and logJson['Status']=='N'):
                    failCount = failCount+1
                elif (logJson['AuthType'] == 'FID' and logJson['Status'] == 'success') or (logJson['AuthType'] == 'FID' and logJson['Status'] == 'Y'):
                    successCount = successCount+1
                elif logJson['AuthType'] == '':
                    emptyAuthCount = emptyAuthCount+1
    return (successCount,failCount,emptyAuthCount)

def printResult(count):
    print('Final Result is: ')
    print('Successful FaceAuth Count:',sum(count[0]))
    print('Failed FaceAuth Count:', sum(count[1]))
    print('Empty FaceAuth Count:', sum(count[2]))

def main():
    fileName = ['2021-08-30/100.65.137.166/aadhar_service.2021-08-30.0.log']
    fileName.append('2021-08-30/100.65.137.166/aadhar_service.2021-08-30.1.log')
    fileName.append('2021-08-30/100.65.137.167/aadhar_service.2021-08-30.0.log')
    fileName.append('2021-08-30/100.65.137.167/aadhar_service.2021-08-30.1.log')
    fileName.append('2021-08-30/100.65.137.168/aadhar_service.2021-08-30.0.log')
    fileName.append('2021-08-30/100.65.137.168/aadhar_service.2021-08-30.1.log')
    fileName.append('2021-08-30/100.65.137.169/aadhar_service.2021-08-30.0.log')
    fileName.append('2021-08-30/100.65.137.169/aadhar_service.2021-08-30.1.log')
    fileName.append('2021-08-30/100.65.137.177/aadhar_service.2021-08-30.0.log')
    fileName.append('2021-08-30/100.65.137.177/aadhar_service.2021-08-30.1.log')
    fileName.append('2021-08-30/100.65.137.178/aadhar_service.2021-08-30.0.log')
    fileName.append('2021-08-30/100.65.137.178/aadhar_service.2021-08-30.1.log')
    fileName.append('2021-08-30/100.65.137.179/aadhar_service.2021-08-30.0.log')
    fileName.append('2021-08-30/100.65.137.179/aadhar_service.2021-08-30.1.log')
    fileName.append('2021-08-30/100.65.137.180/aadhar_service.2021-08-30.0.log')
    fileName.append('2021-08-30/100.65.137.180/aadhar_service.2021-08-30.1.log')
    result = []
    i=0
    for file in fileName:
        print('Working on file = ',file)
        result.append(readLogFileJSONWay(file))
    countResultZipObj = zip(result[0],result[1],result[2],result[3],result[4],result[5],result[6],result[7],result[8],result[9],result[10],result[11],result[12],result[13],result[14],result[15])
    countResultList = list(countResultZipObj)
    printResult(countResultList)





if __name__=='__main__':
    main()
