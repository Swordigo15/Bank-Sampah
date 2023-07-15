import customtkinter
from CTkTable import *

import pickle
import os

from datetime import datetime

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

global winCounter
winCounter = [0, 0, 0]

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        #! UI #############################################################################################################################

        # configure window
        self.title("Bank Sampah")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure((1, 2), weight=1)
        self.grid_rowconfigure((3, 4), weight=1)

        # Tittle
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=5, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="BANK SAMPAH", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Menu Button
        self.InputWindowBtn = customtkinter.CTkButton(self.sidebar_frame, text="Input Sampah", command=self.InputWindow)
        self.InputWindowBtn.grid(row=1, column=0, padx=20, pady=10)
        self.InputWindowBtn.configure(state="disabled")
        self.InputHistoryBtn = customtkinter.CTkButton(self.sidebar_frame, text="Riwayat Input", command=self.InputHistoryWindow)
        self.InputHistoryBtn.grid(row=2, column=0, padx=20, pady=10)
        self.O_DatabaseBtn = customtkinter.CTkButton(self.sidebar_frame, text="Rekap Perorangan", command=self.O_DatabaseWindow)
        self.O_DatabaseBtn.grid(row=3, column=0, padx=20, pady=10)

        # Name Entry
        self.InputTittle = customtkinter.CTkLabel(self, text="INPUT SAMPAH", font=customtkinter.CTkFont(size=50, weight="bold"))
        self.InputTittle.grid(row=0, column=1, columnspan=2, padx=20, pady=20, sticky="nsew")
        self.nameEntry = customtkinter.CTkEntry(self, placeholder_text="Masukkan Nama...", font=customtkinter.CTkFont(size=30))
        self.nameEntry.grid(row=1, column=1, columnspan=2, padx=20, pady=20, sticky="new")

        # Sampah Grid
        self.gridFrame1 = customtkinter.CTkFrame(self)
        self.gridFrame1.grid(row=2, column=1, padx=(20,5), pady=(0,20), sticky="ew")
        self.gridFrame1.grid_columnconfigure(0, weight=1)

        self.trashType = ["Botol Plastik (2.000/kg)", "Gelas Plastik (2.000/kg)", "Kardus (1.200/kg)",
                        "Duplex (800/kg)", "Kertas Koran (4.000 /kg)", "Kertas HVS (2.500 /kg)",
                        "Kertas Buram (2.200 /kg)", "Galon (5.000/buah)", "Botol Kaca (100/kg)",
                        "Minyak Jenlatah (5.000 /1,5 liter)"]
        
        self.unit = ["Kg", "Buah", "Liter"]

        self.varList = [customtkinter.StringVar() for i in range(10)]
        self.S_Label_list1 = [customtkinter.CTkLabel(self.gridFrame1, font=customtkinter.CTkFont(size=15)) for i in range(5)]
        self.S_Entry_list1 = [customtkinter.CTkEntry(self.gridFrame1, textvariable=self.varList[i]) for i in range(5)]
        self.S_Label_0list1 = [customtkinter.CTkLabel(self.gridFrame1, font=customtkinter.CTkFont(size=15)) for i in range(5)]

        for i in range(5):
            self.S_Label_list1[i].configure(text=self.trashType[i])
            self.S_Label_list1[i].grid(row=i, column=0, padx=(20,0), pady=10, sticky="new")
            self.S_Entry_list1[i].grid(row=i, column=1, padx=(20,0), pady=10, sticky="new")
            self.S_Label_0list1[i].configure(text=self.unit[0])
            self.S_Label_0list1[i].grid(row=i, column=2, padx=5, pady=10, sticky="new")

        self.gridFrame2 = customtkinter.CTkFrame(self)
        self.gridFrame2.grid(row=2, column=2, padx=(5,20), pady=(0,20), sticky="ew")
        self.gridFrame2.grid_columnconfigure(0, weight=1)

        self.S_Label_list2 = [customtkinter.CTkLabel(self.gridFrame2, font=customtkinter.CTkFont(size=15)) for i in range(5)]
        self.S_Entry_list2 = [customtkinter.CTkEntry(self.gridFrame2, textvariable=self.varList[i+5]) for i in range(5)]
        self.S_Label_0list2 = [customtkinter.CTkLabel(self.gridFrame2, font=customtkinter.CTkFont(size=15)) for i in range(5)]

        for i in range(5):
            self.S_Label_list2[i].configure(text=self.trashType[i+5])
            self.S_Label_list2[i].grid(row=i, column=0, padx=(20,0), pady=10, sticky="new")
            self.S_Entry_list2[i].grid(row=i, column=1, padx=(20,0), pady=10, sticky="new")
            if i == 2:
                self.S_Label_0list2[i].configure(text=self.unit[1])
            elif i ==  4:
                self.S_Label_0list2[i].configure(text=self.unit[2])
            else:
                self.S_Label_0list2[i].configure(text=self.unit[0])
            self.S_Label_0list2[i].grid(row=i, column=2, padx=5, pady=10, sticky="new")

        for i in range(10):
            self.varList[i].trace('w', self.changeTotal)

        #! Money ##########################################################################################################################

        # Total foreach trash
        self.trashTotal = [0] * 10

        # Total money for each trash
        self.price = [2000, 2000, 1200, 800, 4000, 2500, 2200, 5000, 100, 5000]
        self.trashMoney = [0] * 10
        

        self.totalLabel = customtkinter.CTkLabel(self, text="Total : Rp. 0", font=customtkinter.CTkFont(size=30, weight="bold"))
        self.totalLabel.grid(row=3, column=1, padx=20, pady=(0,20), sticky="w")
        self.InputBtn = customtkinter.CTkButton(self, text="INPUT", font=customtkinter.CTkFont(size=30, weight="bold"), command=self.InputData)
        self.InputBtn.grid(row=4, column=2, padx=20, sticky="e")

        #! PERSON DATA #############################################################################################################################

        self.names = ["Parto", "Maria", "Mulyadi", "Siska", "Hestreni",
                    "Alex", "Ari", "Murni", "Rendi", "Atik", 
                    "Dinar", "Harti", "Heru", "Diah", "Astutiek", 
                    "Muchtar", "Elo"]

        self.P_dataList = [[0 for i in range(12)] for j in range(17)]

        self.totalPerson = 17

        for i in range(self.totalPerson):
            self.P_dataList[i][1] = self.names[i]

        # Load
        if os.stat("Data.txt").st_size != 0:
            self.file = open("Data.txt", "rb")
            self.P_dataList = pickle.load(self.file)
            self.file.close()
            print(self.P_dataList)
        else:
            self.file = open("Data.txt", "wb")
            pickle.dump(self.P_dataList, self.file)
            self.file.close()

        #! MONTH DATA ##############################################################################################################################

        # Load
        # laod year > month > data to mData
        
        self.file = open("Data Sampah.txt", "rb")
        self.DataDict = pickle.load(self.file)
        self.file.close()

        now = datetime.now()
        self.yStr = int(now.strftime("%Y"))
        self.mStr = int(now.strftime("%m"))

        self.currYData = self.DataDict[self.yStr]
        self.currMData = self.currYData[self.mStr]

    #! Input Data Func #############################################################################################################################

    def InputData(self):
        #! Person Recap
        # P_dataList = [index (0-9) trashTotal[10], index(10) totaMoney, index(11) userName]

        for i in range(self.totalPerson):
            if self.P_dataList[i][0] == self.nameEntry.get():    # if the name in data is the same as userName 
                self.P_dataList[i][1] += self.total               # Add total money to data
                for j in range(2,12):
                    self.P_dataList[i][j] += self.trashTotal[j-2]   # Add each trash data to data
                
                # self.currDataList = self.P_dataList[i] # Current Data List

        print(self.P_dataList) # Each person Data

        # Save data
        self.file = open("Data.txt", "wb")
        pickle.dump(self.P_dataList, self.file)
        self.file.close()

        #! Monthly Recap

        # each mData += each trash data
        for key in self.currMData.keys():
            self.currMData[key] += self.trashTotal[list(self.currMData.keys()).index(key)]

        # save mData > this_yData[now.month] > data[now.year] 
        self.currYData[self.mStr] = self.currMData
        self.DataDict[self.yStr] = self.currYData

        self.file = open("Data Sampah.txt", "wb")
        pickle.dump(self.DataDict, self.file)
        self.file.close()

        # History
        # self.now = datetime.now()
        # self.dateStr = self.now.strftime("%d/%m/%Y %H:%M:%S")
        # self.HistoryText = [[" - " + self.dateStr + " " + self.nameEntry.get() + " Rp. " + str(self.total) + "\n\tBP: " + str(self.trashTotal[0]) + "; GP: " + str(self.trashTotal[1]) + "; K: " + str(self.trashTotal[2]) + "; D: " + str(self.trashTotal[3]) + "; KK: " + str(self.trashTotal[4]) + "\n\tKH: " + str(self.trashTotal[5]) + "; KB: " + str(self.trashTotal[6]) + "; G: " + str(self.trashTotal[7]) + "; BK: " + str(self.trashTotal[8]) + "; MJ: " + str(self.trashTotal[9]) + "\n"]]
        
        # self.file = open("History.txt", "ab")
        # pickle.dump(self.HistoryText, self.file)
        # self.file.close()

        self.nameEntry.delete(0, customtkinter.END)
        for i in range(10):
            if i > 4:
                self.S_Entry_list2[i-5].delete(0, customtkinter.END)
            else:
                self.S_Entry_list1[i].delete(0, customtkinter.END)

    #! Change Total Label Text Func #############################################################################################################

    def changeTotal(self, *args):
        # StringVar to float
        # amount of each trash
        for i in range(10):
            self.trashTotal[i] = float(0 if self.varList[i].get() == '' else self.varList[i].get())

        # The money of each trash
        for i in range(10):
            if i == 9:
                self.trashMoney[i] = (self.trashTotal[i] / 1.5) * self.price[i]
            else:
                self.trashMoney[i] = self.trashTotal[i] * self.price[i]

        # Total money'
        self.total = 0
        for i in range(10):
            self.total += self.trashMoney[i]

        self.totalLabel.configure(text='')
        self.totalLabel.configure(text="Total : Rp. {:,.2f}".format(self.total))

    #! Button Function #############################################################################################################################

    def InputWindow(self):
        print("Input Window")

    def InputHistoryWindow(self):
        print("Input History Window")
        self.HistoryWindow = HistoryWindow(self)

    def O_DatabaseWindow(self):
        print("Orang Database Window")
        self.ODsatabaseWindow = OrangDatabaseWindow(self)

##########################################################################################################!
########################################! HISTORY WINDOW #################################################!
##########################################################################################################!

class HistoryWindow(customtkinter.CTkToplevel):
    def __init__(self, master = None):
        #! UI ############################################################################################################################# 
        super().__init__(master=master)

        # configure window
        self.title("Bank Sampah")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure((1, 2), weight=1)
        self.grid_rowconfigure((3, 4), weight=1)

        # Tittle
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=5, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="BANK SAMPAH", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Menu Button
        self.InputWindowBtn = customtkinter.CTkButton(self.sidebar_frame, text="Input Sampah", command=self.InputWindow)
        self.InputWindowBtn.grid(row=1, column=0, padx=20, pady=10)
        self.InputHistoryBtn = customtkinter.CTkButton(self.sidebar_frame, text="Riwayat Input", command=self.InputHistoryWindow)
        self.InputHistoryBtn.grid(row=2, column=0, padx=20, pady=10)
        self.InputHistoryBtn.configure(state="disabled")
        self.O_DatabaseBtn = customtkinter.CTkButton(self.sidebar_frame, text="Rekap Perorangan", command=self.O_DatabaseWindow)
        self.O_DatabaseBtn.grid(row=3, column=0, padx=20, pady=10)

        self.HistoryTittle = customtkinter.CTkLabel(self, text="RIWAYAT", font=customtkinter.CTkFont(size=50, weight="bold"))
        self.HistoryTittle.grid(row=0, column=1, columnspan=2, padx=20, pady=20, sticky="nsew")

        # self.file = open("History.txt", "rb")
        # self.HistoryTexts = [[]]
        # print(pickle.load(self.file))
        # self.file.close()

        # #! Pickle only load the first History

        # self.textbox = customtkinter.CTkTextbox(self, width=250)
        # self.textbox.grid(row=2, column=1, rowspan=3, columnspan=3, padx=20, pady=20, sticky="nsew")
        # self.textbox.configure(state="normal")
        # # self.textbox.insert("1.0", self.HistoryText)
        # self.textbox.configure(state="disabled")

        self.lift()
        self.attributes('-topmost',True)
        self.after_idle(self.attributes,'-topmost',False)

    #! Function ####################################################################################################################################

    # def updateHistory(self):
        

    #! Button Function #############################################################################################################################

    def InputWindow(self):
        print("Input Window")

    def InputHistoryWindow(self):
        print("Input History Window")

    def O_DatabaseWindow(self):
        print("Orang Database Window")
        OrangDatabaseWindow(self)

##########################################################################################################!
####################################! ORANG DATABASE WINDOW ##############################################!
##########################################################################################################!

class OrangDatabaseWindow(customtkinter.CTkToplevel):
    def __init__(self, master=None):
        #! UI #############################################################################################################################
        super().__init__(master=master)

        # configure window
        self.title("Bank Sampah")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.ODBTittle = customtkinter.CTkLabel(self, text="REKAP PERORANGAN", font=customtkinter.CTkFont(size=50, weight="bold"))
        self.ODBTittle.grid(row=0, column=0, columnspan=3, padx=20, pady=20, sticky="nsew")

        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        self.tabview.add("Perorang")
        self.tabview.add("Bulanan")
        self.tabview.tab("Perorang").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Bulanan").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Perorang").grid_rowconfigure(0, weight=1)
        self.tabview.tab("Bulanan").grid_rowconfigure(0, weight=1)
        

        self.tableFrameP = customtkinter.CTkScrollableFrame(self.tabview.tab("Perorang"))
        self.tableFrameP.grid(row=0, column=0, sticky="news")

        self.tableFrameB = customtkinter.CTkScrollableFrame(self.tabview.tab("Bulanan"))
        self.tableFrameB.grid(row=0, column=0, sticky="news")

        self.names = ["Parto", "Maria", "Mulyadi", "Siska", "Hestreni",
                    "Alex", "Ari", "Murni", "Rendi", "Atik", 
                    "Dinar", "Harti", "Heru", "Diah", "Astutiek", 
                    "Muchtar", "Elo"]

        # Load
        # Load person Data
        self.P_dataList = [[0 for i in range(12)] for j in range(17)]
        for i in range(17):
            self.P_dataList[i][1] = self.names[i]

        if os.stat("Data.txt").st_size != 0:
            self.file = open("Data.txt", "rb")
            self.P_dataList = pickle.load(self.file)
            self.file.close()

        # Load month Data
        if os.stat("Data Sampah.txt").st_size != 0:
            self.file = open("Data Sampah.txt", "rb")
            self.file.close()

        #Create table data
        totalRows = 12
        totalCols = 17
        self.List = [["No.", "Nama", "Tabungan", "BP", "GP", 
                        "K", "D", "KK", "KH",
                        "KB", "G", "BK", "MJ"]]
        self.data = [[0 for i in range(totalRows+1)] for j in range(totalCols)]

        self.List = self.List + self.data
        for i in range(17): self.List[i+1][0] = i+1

        for i in range(17):
            for j in range(12):
                self.List[i+1][j+1] = self.P_dataList[i][j]

        #! Tabel Perorangan
        # create table
        self.tableP = CTkTable(self.tableFrameP, row=totalCols+1, column=totalRows+1, values=self.List, corner_radius=0)
        self.tableP.grid(row=0, column=0)

        #! Tabel Bulanan
        self.tableB = CTkTable(self.tableFrameB, row=totalCols+1, column=totalRows+1, values=self.List, corner_radius=0)
        self.tableB.grid(row=0, column=0)

        self.lift()
        self.attributes('-topmost',True)
        self.after_idle(self.attributes,'-topmost',False)

    #! Button Function #############################################################################################################################

    def InputWindow(self):
        print("Input Window")

    def InputHistoryWindow(self):
        print("Input History Window")
        HistoryWindow(self)

    def O_DatabaseWindow(self):
        print("Orang Database Window")

if __name__ == "__main__":
    app = App()
    app.mainloop()