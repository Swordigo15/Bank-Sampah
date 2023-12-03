import pickle

file = open("Data/Admin.txt", "rb")
login = pickle.load(file)
file.close()
print(login)

input("Press Enter to continue... ")
# pyinstaller --onefile LoginReader.py