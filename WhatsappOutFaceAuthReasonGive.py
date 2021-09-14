import json, os, sys, xml.etree.ElementTree as ET, base64
successCount =0
failCount =0
emptyAuthCount =0
dictErrorCount = {}
dictEmptyErrorCodeReasonCount = {}
dictK100Types = {}
dictInputHash = {}
totalInputHash = 0

def readLogFileJSONWay(fileName):
    global successCount, failCount , emptyAuthCount, dictErrorCount, dictEmptyErrorCodeReasonCount, dictK100Types, dictInputHash, totalInputHash
    logFile = open(fileName, 'r')
    for line in logFile:
        logJsonArr = line.split()[5:]
        JsonStr = " ".join(logJsonArr)
        if len(JsonStr) > 0 and JsonStr[0] == '{':
            logJson = json.loads(JsonStr)
            # print(logJson)
            if logJson.get('InputHash') != None:
                 if logJson['InputHash'] not in dictInputHash.keys() and logJson.get('AuthType') != None and logJson['AuthType'] == 'FID' :
                    dictInputHash[logJson['InputHash']] = []
                    dictInputHash[logJson['InputHash']].append(0)
                    dictInputHash[logJson['InputHash']].append(0)
            if logJson.get('AuthType') != None:
                if (logJson['AuthType'] == 'FID' and logJson['Status'] == 'failed') or (
                        logJson['AuthType'] == 'FID' and logJson['Status'] == 'N'):
                    failCount = failCount + 1
                    dictInputHash[logJson['InputHash']][0] = dictInputHash[logJson['InputHash']][0] + 1
                    #Changes for K-100 type error inclusion in unique fail count list
                    if logJson['ErrorCode'] != "K-100":
                        dictInputHash[logJson['InputHash']].append(logJson['ErrorCode'])
                    if logJson['ErrorCode'] == "":
                        dictInputHash[logJson['InputHash']].append(logJson['Reason'])
                        if logJson['Reason'] in dictEmptyErrorCodeReasonCount.keys():
                            dictEmptyErrorCodeReasonCount[logJson['Reason']] = dictEmptyErrorCodeReasonCount[logJson['Reason']] + 1
                        else:
                            dictEmptyErrorCodeReasonCount[logJson['Reason']] = 1
                        if logJson['Reason'] in dictErrorCount.keys():
                            dictErrorCount[logJson['Reason']] = dictErrorCount[logJson['Reason']] + 1
                        else:
                            dictErrorCount[logJson['Reason']] = 1
                    else:
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
                            if K100Err == "930":
                                dictInputHash[logJson['InputHash']].append("930")
                            if K100Err == "935":
                                dictInputHash[logJson['InputHash']].append("935")
                            if K100Err == "933":
                                dictInputHash[logJson['InputHash']].append("933")
                            if K100Err in dictK100Types:
                                dictK100Types[K100Err] += 1
                            else:
                                dictK100Types[K100Err] = 1
                elif (logJson['AuthType'] == 'FID' and logJson['Status'] == 'success') or (
                        logJson['AuthType'] == 'FID' and logJson['Status'] == 'Y'):
                    successCount = successCount + 1
                    dictInputHash[logJson['InputHash']][1] = dictInputHash[logJson['InputHash']][1] + 1
                # elif logJson['AuthType'] == '':
                #     emptyAuthCount = emptyAuthCount + 1
                #     if logJson['Reason'] in dictEmptyErrorCodeReasonCount.keys():
                #         dictEmptyErrorCodeReasonCount[logJson['Reason']] = dictEmptyErrorCodeReasonCount[logJson['Reason']] + 1
                #     else:
                #         dictEmptyErrorCodeReasonCount[logJson['Reason']] = 1
    return (successCount, failCount, emptyAuthCount)


def printResult(count):
    global successCount, failCount, emptyAuthCount, dictErrorCount, dictEmptyErrorCodeReasonCount, dictK100Types, dictInputHash, totalInputHash
    print('\n\nFinal Result is: ')
    print('Successful FaceAuth Count:', count[0])
    print('Failed FaceAuth Count:', count[1])
    print('Empty FaceAuth Count:', count[2])
    print('\n\nError Count is:')
    print('<ErrorCode>  -------------- <Count of the Error> ')
    for keys, values in dictErrorCount.items():
        print(keys, '----------->> has error count of ------------>>', values)
    print('\n\nEmpty ErrorCode Reason Count is:')
    print('<Reason>  -------------- <Count of the Reason> ')
    for keys, values in dictEmptyErrorCodeReasonCount.items():
        print(keys, '-------------->> has reason count of ----------->>', values)
    print('\n\n<K-100 Error Type>  -------------- <Count of the Error Type> ')
    for keys, values in dictK100Types.items():
        print(keys, '-------------->> has count of ----------->>', values)
    print('\n\nUnique InputHash with FID = ',len(dictInputHash))
    uniqueSuccessCount=0
    uniqueFailedCount = 0
    dictUniqueFailedCountErrorList = {}
    err300OnePerUnqUser = 0
    for values in dictInputHash.values():
        if values[1]>0:
            uniqueSuccessCount = uniqueSuccessCount+1

        flag=0
        if len(values) > 2:
            for eachValue in values[2:]:
                if flag ==0:
                    if eachValue =="300":
                        err300OnePerUnqUser +=1
                        flag=1
        if values[1] == 0:
            uniqueFailedCount = uniqueFailedCount + 1
            for eachValue in values[2:]:
                if eachValue in dictUniqueFailedCountErrorList.keys():
                   dictUniqueFailedCountErrorList[eachValue]+=1
                else:
                   dictUniqueFailedCountErrorList[eachValue] = 1

    print('Unique Successful InputHash = ',uniqueSuccessCount)
    print('Unique Failed InputHash = ', uniqueFailedCount)
    print('\n\nNever Succeeded InputHash Error Distribution is as follows :')
    print('\n\n<Error Type>  -------------- <Count of the Error Type> ')
    for keys, values in dictUniqueFailedCountErrorList.items():
        print(keys, '-------------->> has count of ----------->>', values)
    print("Error 300 on clubbing for individual  user\n{")
    print("Biometric data did not match '300': ",err300OnePerUnqUser,"\n}")


def WhatsappOutput(count):
    global successCount, failCount, emptyAuthCount, dictErrorCount, dictEmptyErrorCodeReasonCount, dictK100Types, dictInputHash, totalInputHash
    dictErrorDescription = \
        {
            "300" : "Biometric data did not match '300':",
            "330" : "Biometrics locked by Aadhaar holder '330':",
            "997" : "Aadhaar Suspended '997':",
            "563" : "Duplicate request (this error occurs when exactly same authentication request was re-sent by AUA)  '563':",
            "996" : "Aadhaar Cancelled '996':",
            "K-100" : "'K-100':",
            "ASA-Timeout" : "'ASA-Timeout':",
            "1201" : "1201:",
            "1204" : "1204:",
            "K-955" : "K-955:",
            "Connection reset":"Connection reset:",
            "":"<Empty Error Code>:", #Spaces in keys are important
            "5xx Server exception receieved from ASA.":"5xx Server exception receieved from ASA:",
            "930" : "Technical error that are internal to authentication server  '930': ",
            "933": "Technical error that are internal to authentication server  '933': ",
            "935" : "Technical error that are internal to authentication server  '935':"
        }
    print('\n\nWhatsapp Output is :\n\n')
    print('\n\nFace Auth {} :'.format(sys.argv[1]),"\n\n{")
    for keys, values in dictErrorCount.items():
        print(dictErrorDescription[keys], values)
    print("}\n\n{")
    for keys, values in dictK100Types.items():
        print(dictErrorDescription[keys], values)
    print("}")
    print('Success FaceID:', count[0], end='')
    print(' || Failed FaceID:', count[1])
    print('\nUnique Users:', len(dictInputHash))
    uniqueSuccessCount = 0
    uniqueFailedCount = 0
    dictUniqueFailedCountErrorList = {}
    err300OnePerUnqUser = 0
    for values in dictInputHash.values():
        if values[1] > 0:
            uniqueSuccessCount = uniqueSuccessCount + 1

        flag = 0
        if len(values) > 2:
            for eachValue in values[2:]:
                if flag == 0:
                    if eachValue == "300":
                        err300OnePerUnqUser += 1
                        flag = 1
        if values[1] == 0:
            uniqueFailedCount = uniqueFailedCount + 1
            for eachValue in values[2:]:
                if eachValue in dictUniqueFailedCountErrorList.keys():
                    dictUniqueFailedCountErrorList[eachValue] += 1
                else:
                    dictUniqueFailedCountErrorList[eachValue] = 1

    print('Unique Successful Users:', uniqueSuccessCount)
    print("\n\nError 300 on clubbing for individual  user\n{")
    print("Biometric data did not match '300': ", err300OnePerUnqUser, "\n}")
    print('\n\nError distribution for  all users with all failed  txns:\n{')
    for keys, values in dictUniqueFailedCountErrorList.items():
        print(dictErrorDescription[keys], values)
    print("}")

    successCount = 0
    failCount = 0
    emptyAuthCount = 0
    dictErrorCount = {}
    dictEmptyErrorCodeReasonCount = {}
    dictK100Types = {}
    dictInputHash = {}

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
        WhatsappOutput((successCount,failCount,emptyAuthCount))


if __name__ == '__main__':
    main()
