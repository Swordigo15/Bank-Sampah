import numpy
import pickle

from datetime import datetime

Login = ["Admin", "123"]
file = open("Data/Admin.txt", "wb")
pickle.dump(Login, file)
file.close()

file = open("Data/Admin.txt", "rb")
print(pickle.load(file))
file.close()

trashType = ["Botol Plastik", "Gelas Plastik", "Kardus",
                        "Duplex", "Kertas Koran", "Kertas HVS",
                        "Kertas Buram", "Galon", "Botol Kaca",
                        "Minyak Jelantah", "Lainnya"]

prices = [2000, 2000, 1200, 800, 4000, 2500, 2200, 5000, 100, 5000, 2000]

sampah = [trashType, prices]

file = open("Data/Tipe Sampah.txt", "wb")
pickle.dump(sampah, file)
file.close()

print("")

file = open("Data/Tipe Sampah.txt", "rb")
sampahLoad = pickle.load(file)
print("sampah : ", sampahLoad)
file.close()

names = ["PARTO", "MARIA", "MULYADI", "SISKA", "HESTRENI",
            "ALEX", "ARI", "MURNI", "RENDI", "ATIK", 
            "DINAR", "HARTI", "HERU", "DIAH", "ASTUTIEK", 
            "MUCHTAR", "ELO"]

List = [0] * (len(trashType)+1)

data = {}

# for i in range(17):
#     data[names[i]] = List
#     print(data[names[i]])

file = open("Data/Data.txt", "wb")
pickle.dump(data, file)
file.close()

print("")

file = open("Data/Data.txt", "rb")
loadList = pickle.load(file)
print(loadList)
# for i in range(17):
#     print(loadList[names[i]])
file.close()

now = datetime.now()
mStr = int(now.strftime("%m"))
yStr = int(now.strftime("%Y"))

mData = {}
for i in range(13):
    mData[i+1] = List

yData = {}
yData[yStr] = mData

# print("yData[yStr][mStr] : \n", yData[yStr][mStr], "\n")
print("yData[yStr] : \n", yData[yStr], "\n")
print("yData : \n", yData, "\n")

# Save
file = open("Data/Data Sampah.txt", "wb")
pickle.dump(yData, file)
file.close()

print("Load :")

# Load
file = open("Data/Data Sampah.txt", "rb")
yData_Load = pickle.load(file)
print(yData_Load)
file.close()

History = []

file = open("Data/Riwayat.txt", "wb")
pickle.dump(History, file)
file.close()

# pyinstaller --onefile ResetDataFile.py
# - Nambah Jenis sampah manual
# - Login
# - Bisa print history dan rekap
