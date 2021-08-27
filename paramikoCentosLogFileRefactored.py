import paramiko

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
        client.connect(hostname, port=22, username='centos',
                       password='')
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


def readLogFile(cmdOutputString):
    successString1 = '"AuthType":"FID","Status":"success"'
    successString2 = '"AuthType":"FID","Status":"Y"'
    failString1 = '"AuthType":"FID","Status":"failed"'
    failString2 = '"AuthType":"FID","Status":"N"'
    emptyAuthType = '"AuthType":""'
    successCount = 0
    failCount = 0
    emptyAuthTypeCount = 0
    successCount = cmdOutputString.count(successString1) + cmdOutputString.count(successString2)
    failCount = cmdOutputString.count(failString1) + cmdOutputString.count(failString2)
    emptyAuthTypeCount = cmdOutputString.count(emptyAuthType)
    return (successCount, failCount, emptyAuthTypeCount)

def printResult(count):
    print('Successful FaceAuth Count:',count[0])
    print('Failed FaceAuth Count:', count[1])
    print('Empty FaceAuth Count:', count[2])

def main():
    remoteOutput = paramiko_Centos('86.107.243.9', 'cat ishanCode/logFolder/logfile.txt')
    faceAuthCount = readLogFile(remoteOutput)
    printResult(faceAuthCount)

if __name__=='__main__':
    main()