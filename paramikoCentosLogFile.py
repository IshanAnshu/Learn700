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
                       password='dumfold@123456')
        print('SSH Connection Established')

        # below line command will actually
        # execute in your remote machine
        (stdin, stdout, stderr) = client.exec_command(command)

        # redirecting all the output in cmd_output
        # variable
        print('stdout is : ',stdout)
        print('Type of stdout is = ', type(stdout))
        cmd_output = stdout.read()
        print('Type of cmd_output is = ',type(cmd_output))
        cmd_output_string = cmd_output.decode("ASCII")
                                    # file2 = open('decodedString.txt','w')
                                    # file2.write(cmd_output_string)
                                    # file2.close()
        print('Type of cmd_output_string is = ', type(cmd_output_string))

        printResult(readLogFile(cmd_output_string))

        #print('log printinf: ', command, cmd_output)

        # we are creating file which will read our
        # cmd_output and write it in output_file
        #with open(output_file, "w+") as file:
            #file.write(str(cmd_output))

        # we are returning the output
        #return output_file
    finally:
        client.close()


def readLogFile(file1):
    #print('file1 is:', file1)
    # file2 = open('decodedStringFromFxn.txt','w')
    # file2.write(file1)
    # file2.close()
    successString1 = '"AuthType":"FID","Status":"success"'
    successString2 = '"AuthType":"FID","Status":"Y"'
    failString1 = '"AuthType":"FID","Status":"failed"'
    failString2 = '"AuthType":"FID","Status":"N"'
    emptyAuthType = '"AuthType":""'
    successCount = 0
    failCount = 0
    emptyAuthTypeCount = 0
    # dict ={(success[],sc), ()}
    #file1 = open("logfile.txt", "r")
    #j = 1
    # for line in file1:
    #     if successString1 in line or successString2 in line:
    #         successCount = successCount + 1
    #     elif failString1 in line or failString2 in line:
    #         failCount = failCount + 1
    #     elif emptyAuthType in line:
    #         emptyAuthTypeCount = emptyAuthTypeCount + 1
    successCount = file1.count(successString1) + file1.count(successString2)
    failCount = file1.count(failString1) + file1.count(failString2)
    emptyAuthTypeCount = file1.count(emptyAuthType)
    return (successCount, failCount, emptyAuthTypeCount)

def printResult(count):
    print('Successful FaceAuth Count:',count[0])
    print('Failed FaceAuth Count:', count[1])
    print('Empty FaceAuth Count:', count[2])

def main():
    paramiko_Centos('86.107.243.9', 'cat ishanCode/logFolder/logfile.txt')
    #printResult(readLogFile())

if __name__=='__main__':
    main()