
class Complex:
  def __init__(self, realpart, imagpart):
     self.name = realpart
     self.number = imagpart

readder = []
file = open("recordFileResult.txt.txt", "r")
dataFromFile = file.readline()
while dataFromFile:
    readder.append(dataFromFile.strip().lower())
    dataFromFile = file.readline()
file.close()

list = []
firstInsertToList = readder[0].split()
for i in firstInsertToList:
    if len(list) == 0:
        obj = Complex(i, 1)
        list.append(obj)
        continue

    for item in range(0,len(list)):
        if list[item].name == i:
            list[item].number += 1
            break
        if item == len(list) - 1:
            obj = Complex(i,1)
            list.append(obj)
for i in range(1,len(readder)):
    obj_splitted = readder[i].split()
    for item1 in obj_splitted:
        for item in range(0, len(list)):
            if list[item].name == item1:
                list[item].number += 1
                break
            if item == len(list) - 1:
                obj = Complex(item1, 1)
                list.append(obj)

list.sort(key=lambda x: x.number, reverse=True)
list[:10]

for i in range(0,10):
    print(list[i].name,list[i].number)



