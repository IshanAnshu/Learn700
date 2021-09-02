import os

if __name__ == "__main__":
     fileNameString = []
     result = []
     for i in range(16):
         result[i] = (i, i, i)
     for (root,dirs,files) in os.walk(r'E:\Learning700\2021-08-30', topdown=True):
         for file in files:
             fileNameString.append(r'{}\{}'.format(root,file))
     for file in fileNameString:
         print(file)
