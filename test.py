readder = []
file = open("recordFile.txt", "r")
dataFromFile = file.readline()
for i in range(0,10):
    print(dataFromFile.strip())
    print(dataFromFile.strip().lower())
    file.w
    dataFromFile = file.readline()