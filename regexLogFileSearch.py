import json

def main():
    logFile = open('sampleLogFile.txt','r')
    #print('logFile is :',logFile)
    logFileString = str(logFile)
    #print('logFileString is =',logFileString)
    i=0
    for line in logFile:
        i=i+1
        print('i =',i)
        #print(line.split()[5:])
        logJsonArr = line.split()[5:]
        JsonStr = " ".join(logJsonArr)
        #print(JsonStr)
        if len(JsonStr)>0 and JsonStr[0]=='{':
            logJson = json.loads(JsonStr)
            print(logJson)
            print(logJson['Status'])

    #regex = '{/S*}'
    # regex = r"\s([{\[].*?[}\]])$"
    # match = re.findall(regex,logFileString)
    # print(match)
    # print('--------------------')
    # regex2 = '[{\[].*?[}\]]'
    # match = re.findall(regex,logFileString)
    # print(match)
    # logJSONArr = logFileString.split(" ")
    #
    # #JSONStr = " ".join(logJSONArr)
    #
    # #logJSON = json.loads(JSONStr)
    # print(logJSONArr)
    # for i in logJSONArr:
    #     print(i)






if __name__=='__main__':
    main()
