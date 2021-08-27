def readLogFile():
    successString1 = '"AuthType":"FID","Status":"success"'
    successString2 = '"AuthType":"FID","Status":"Y"'
    failString1 = '"AuthType":"FID","Status":"failed"'
    failString2 = '"AuthType":"FID","Status":"N"'
    emptyAuthType = '"AuthType":""'
    successCount = 0
    failCount = 0
    emptyAuthTypeCount = 0
    # dict ={(success[],sc), ()}
    file1 = open("logfile.txt", "r")
    for line in file1:
        if successString1 in line or successString2 in line:
            successCount = successCount + 1
        elif failString1 in line or failString2 in line:
            failCount = failCount + 1
        elif emptyAuthType in line:
            emptyAuthTypeCount = emptyAuthTypeCount + 1
    return (successCount, failCount, emptyAuthTypeCount)

def printResult(count):
    print('Successful FaceAuth Count:',count[0])
    print('Failed FaceAuth Count:', count[1])
    print('Empty FaceAuth Count:', count[2])

def main():
    printResult(readLogFile())

if __name__=='__main__':
    main()