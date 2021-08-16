import psycopg2
from xlwt import Workbook

def databaseConnect():
    global conn, cur
    conn = psycopg2.connect(database="testdb", user="postgres", password="pass123", host="127.0.0.1", port="5432")
    print("Opened database successfully")
    cur = conn.cursor()

def writeColHeads():
    global wb, sheet1
    wb = Workbook()
    sheet1 = wb.add_sheet('Sheet 1') # add_sheet is used to create sheet.
    sheet1.write(0, 0, 'State')
    sheet1.write(0, 1, 'Health ID Number')
    sheet1.write(0, 2, 'District')
    sheet1.write(0, 3, 'Pin Code')
    sheet1.write(0, 4, 'Created Date')
    sheet1.write(0, 5, 'Sub Dist')
    sheet1.write(0, 6, 'Street')

def writeDataOnExcel():
    file1 = open("face_auth_xml_uid_15.txt", "r+")
    i = 1
    for line1 in file1:
        line1 = line1.strip()
        index = line1.find(":")
        xml_uid = line1[(index + 2):(len(line1) - 1)]
        query = "select state, health_id_number, dist, pincode, created_date, subdist, street from user_ekyc where xml_uid='{xml_uidCopy}';".format(xml_uidCopy=xml_uid)
        cur.execute(query)
        queryResult = cur.fetchall()
        for eachRow in queryResult:
            for j in range (6):
                sheet1.write(i, j, eachRow[j])
         i = i + 1
    file1.close()

def main():
    global conn
    databaseConnect()
    writeColHeads()
    writeDataOnExcel()
    wb.save('OutputRefactored.xls')
    print("Operation done successfully")
    conn.close()



if __name__ == '__main__':
    main()
