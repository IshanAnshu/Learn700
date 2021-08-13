import psycopg2
from xlwt import Workbook


def main():
    #conn = psycopg2.connect(database="testdb", user="postgres", password="pass123", host="127.0.0.1", port="5432")
    #print("Opened database successfully")
    #cur = conn.cursor()

    wb = Workbook()

    # add_sheet is used to create sheet.
    sheet1 = wb.add_sheet('Sheet 1')
    sheet1.write(0, 0, 'State')
    sheet1.write(0, 1, 'Health ID Number')
    sheet1.write(0, 2, 'District')
    sheet1.write(0, 3, 'Pin Code')
    sheet1.write(0, 4, 'Created Date')
    sheet1.write(0, 5, 'Sub Dist')
    sheet1.write(0, 6, 'Street')

    file1 = open("face_auth_xml_uid_15.txt", "r+")
    i=1
    for line in file1:
        # #print("Output of Readline function is ")
        line1 = line
        line1 = line1.strip()
        # #print(line1)
        ind = line1.find(":")
        # #print(ind)
        # #print("Length",len(line1))
        xml_uid = line1[(ind + 2):(len(line1) - 1)]
        # print(lineSlice)
        z = "select state, health_id_number, dist, pincode, created_date, subdist, street from user_ekyc where xml_uid='{xml_uidCopy}';".format(
            xml_uidCopy=xml_uid)
        #cur.execute(z)
        #rows = cur.fetchall()


        # for row in rows:
        #     sheet1.write(i, 0, row[0])
        #     sheet1.write(i, 1, row[1])
        #     sheet1.write(i, 2, row[2])
        #     sheet1.write(i, 3, row[3])
        #     sheet1.write(i, 4, row[4])
        #     sheet1.write(i, 5, row[5])
        #     sheet1.write(i, 6, row[6])
        # i=i+1
        sheet1.write(i, 0, "State")
        sheet1.write(i, 1, "Health ID Number")
        sheet1.write(i, 2, "Dist")
        sheet1.write(i, 3, "Pin Code")
        sheet1.write(i, 4, "Created Date")
        sheet1.write(i, 5, "SubDist")
        sheet1.write(i, 6, "Street")
        i = i + 1

    wb.save('Output.xls')
    print("Operation done successfully")
    #conn.close()
    file1.close()


if __name__ == '__main__':
    main()
