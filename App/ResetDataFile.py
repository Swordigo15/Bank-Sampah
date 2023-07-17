import numpy
import pickle

from datetime import datetime

names = ["PARTO", "MARIA", "MULYADI", "SISKA", "HESTRENI",
            "ALEX", "ARI", "MURNI", "RENDI", "ATIK", 
            "DINAR", "HARTI", "HERU", "DIAH", "ASTUTIEK", 
            "MUCHTAR", "ELO"]

List = [0] * 12

data = {}

# for i in range(17):
#     data[names[i]] = List
#     print(data[names[i]])

file = open("Data.txt", "wb")
pickle.dump(data, file)
file.close()

print("")

file = open("Data.txt", "rb")
loadList = pickle.load(file)
print(loadList)
# for i in range(17):
#     print(loadList[names[i]])
file.close()

now = datetime.now()
mStr = int(now.strftime("%m"))
yStr = int(now.strftime("%Y"))

mData = {}
for i in range(12):
    mData[i+1] = List

yData = {}
yData[yStr] = mData

# print("yData[yStr][mStr] : \n", yData[yStr][mStr], "\n")
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

History = []

file = open("Riwayat.txt", "wb")
pickle.dump(History, file)
file.close()
