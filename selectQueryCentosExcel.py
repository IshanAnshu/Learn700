import psycopg2
from xlwt import Workbook

# Workbook is created
wb = Workbook()

# add_sheet is used to create sheet.
sheet1 = wb.add_sheet('Sheet 1')

conn = psycopg2.connect(database = "testdb", user = "postgres", password = "pass123", host = "127.0.0.1", port = "5432")
print("Opened database successfully")

cur = conn.cursor()
recid = input("Enter Number :")
z = "SELECT id, name, address, salary  from COMPANY WHERE id = {recidCopy};".format(recidCopy=recid)
cur.execute(z)
rows = cur.fetchall()
sheet1.write(0, 0, 'ID')
sheet1.write(0, 1, 'Name')
sheet1.write(0, 2, 'Address')
sheet1.write(0, 3, 'Salary')
for row in rows:
   # print("ID = ", row[0])
   # print("NAME = ", row[1])
   # print("ADDRESS = ", row[2])
   # print("SALARY = ", row[3], "\n")



   sheet1.write(1, 0, row[0])
   sheet1.write(1, 1, row[1])
   sheet1.write(1, 2, row[2])
   sheet1.write(1, 3, row[3])

wb.save('IshanExcelTestDB2.xls')
print("Operation done successfully")
conn.close()