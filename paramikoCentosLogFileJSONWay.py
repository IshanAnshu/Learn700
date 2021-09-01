import paramiko, json

def paramiko_Centos(hostname, command):
    print('Running SSH function')
    try:
        port = '22'
        # created client using paramiko
        client = paramiko.SSHClient()

        # here we are loading the system
        # host keys
        client.load_system_host_keys()

        # connecting paramiko using host
        # name and password
        client.connect(hostname, port=22, username='centos',password='dumfold@123456')
        print('SSH Connection Established')

        # below line command will actually
        # execute in your remote machine
        (stdin, stdout, stderr) = client.exec_command(command)

        # redirecting all the output in cmd_output
        # variable
        cmdOutput = stdout.read()
        cmdOutputString = cmdOutput.decode("utf-8")
        return cmdOutputString

    finally:
        client.close()

def readLogFileJSONWayFromString(stringFile):
    successCount = failCount = emptyAuthCount = 0
    line = stringFile.splitlines()
    for eachLine in line:
        logJsonArr = eachLine.split()[5:]
        #print(logJsonArr)
        JsonStr = " ".join(logJsonArr)
        if len(JsonStr) > 0 and JsonStr[0] == '{':
            logJson = json.loads(JsonStr)
            # print(logJson)
            if logJson.get('AuthType') != None:
                if (logJson['AuthType'] == 'FID' and logJson['Status'] == 'failed') or (
                        logJson['AuthType'] == 'FID' and logJson['Status'] == 'N'):
                    failCount = failCount + 1
                elif (logJson['AuthType'] == 'FID' and logJson['Status'] == 'success') or (
                        logJson['AuthType'] == 'FID' and logJson['Status'] == 'Y'):
                    successCount = successCount + 1
                elif logJson['AuthType'] == '':
                    emptyAuthCount = emptyAuthCount + 1
    return (successCount, failCount, emptyAuthCount)

def printResult(count):
    print('Final Result is: ')
    print('Successful FaceAuth Count:',sum(count[0]))
    print('Failed FaceAuth Count:', sum(count[1]))
    print('Empty FaceAuth Count:', sum(count[2]))

def main():
    print('On machine: 1')
    remoteOutput = paramiko_Centos('86.107.243.9', 'cat ishanCode/logFolder/logfile.txt')
    faceAuthCount1 = readLogFileJSONWayFromString(remoteOutput)
    print('On machine: 2')
    remoteOutput = paramiko_Centos('86.107.243.9', 'cat ishanCode/logFolder2/logfile.txt')
    faceAuthCount2 = readLogFileJSONWayFromString(remoteOutput)
    print('On machine: 3')
    remoteOutput = paramiko_Centos('86.107.243.9', 'cat ishanCode/logFolder3/logfile.txt')
    faceAuthCount3 = readLogFileJSONWayFromString(remoteOutput)
    print('On machine: 4')
    remoteOutput = paramiko_Centos('86.107.243.9', 'cat ishanCode/logFolder4/logfile.txt')
    faceAuthCount4 = readLogFileJSONWayFromString(remoteOutput)
    countResultZipObj = zip(faceAuthCount1,faceAuthCount2,faceAuthCount3,faceAuthCount4)
    countResultList = list(countResultZipObj)
    printResult(countResultList)

if __name__=='__main__':
    main()