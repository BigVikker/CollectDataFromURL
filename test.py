
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

for i in readder:
    obj_splitted = i.split()
    for item1 in obj_splitted:
        for item in range(0, len(list)):
            if list[item].name == item1:
                list[item].number += 1
                break
            if item == len(list) - 1:
                obj = Complex(item1, 1)
                list.append(obj)

max = 0
for item in list:
    if item.number > max:
        max = item.number
        obj_save = item
print(obj_save.name , obj_save.number)



