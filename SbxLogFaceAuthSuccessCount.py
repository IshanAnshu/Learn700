def declareInitialiseVariables():
    global successString1, successString2, failString1, failString2, emptyAuthType, emptyAuthType, emptyAuthTypeCount, successCount, failCount
    successString1 = '"AuthType":"FID","Status":"success"'
    successString2 = '"AuthType":"FID","Status":"Y"'
    failString1 = '"AuthType":"FID","Status":"failed"'
    failString2 = '"AuthType":"FID","Status":"N"'
    emptyAuthType = '"AuthType":""'
    successCount = 0
    failCount = 0
    emptyAuthTypeCount = 0


def readLogFile():
    global successString1, successString2, failString1, failString2, emptyAuthType, emptyAuthType, emptyAuthTypeCount, successCount, failCount
    file1 = open("logfile.txt", "r")

    for line in file1:
        if successString1 in line or successString2 in line:
            successCount = successCount + 1
        elif failString1 in line or failString2 in line:
            failCount = failCount + 1
        elif emptyAuthType in line:
            emptyAuthTypeCount = emptyAuthTypeCount + 1

def printResult():
    print('Successful FaceAuth Count:',successCount)
    print('Failed FaceAuth Count:', failCount)
    print('Empty FaceAuth Count:', emptyAuthTypeCount)

def main():
    declareInitialiseVariables()
    readLogFile()
    printResult()

if __name__=='__main__':
    main()