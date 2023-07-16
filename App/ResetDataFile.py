import numpy
import pickle

from datetime import datetime

names = ["Parto", "Maria", "Mulyadi", "Siska", "Hestreni",
            "Alex", "Ari", "Murni", "Rendi", "Atik", 
            "Dinar", "Harti", "Heru", "Diah", "Astutiek", 
            "Muchtar", "Elo"]

List = [[0 for i in range(12)] for j in range(17)]

for i in range(17):
    List[i][0] = names[i]
    print(List[i])

file = open("Data.txt", "wb")
pickle.dump(List, file)
file.close()

print("")

file = open("Data.txt", "rb")
loadList = pickle.load(file)
for i in range(17):
    print(loadList[i])
file.close()

now = datetime.now()
mStr = int(now.strftime("%m"))
yStr = int(now.strftime("%Y"))

Data = {"Uang" : 0, "BP" : 0, "GP" : 0, 
        "K" : 0, "D" : 0, "KK" : 0, 
        "KH" : 0, "KB" : 0, "G" : 0, 
        "BK" : 0, "MJ" : 0}

#11x12

mData = {}
for i in range(12):
    mData[i+1] = Data

yData = {}
yData[yStr] = mData

print("yData[yStr][mStr] : \n", yData[yStr][mStr], "\n")
print("yData[yStr] : \n", yData[yStr], "\n")
print("yData : \n", yData, "\n")

# Save
file = open("Data Sampah.txt", "wb")
pickle.dump(yData, file)
file.close()

print("Load :")

# Load
file = open("Data Sampah.txt", "rb")
yData_Load = pickle.load(file)
print(yData_Load)
file.close()
