from tkinter import messagebox
from tkinter import simpledialog
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

        self.DatabaseWindowVar = None
        #! UI #############################################################################################################################

        # configure window
        width= self.winfo_screenwidth()               
        height= self.winfo_screenheight()
        self.title("Bank Sampah")
        self.geometry(f"{width}x{height}+{-10}+{-5}")
        # self.state("zoomed")
        # self.attributes('-fullscreen', True)

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
        self.O_DatabaseBtn = customtkinter.CTkButton(self.sidebar_frame, text="Rekap Perorangan", command=self.DatabaseWindow)
        self.O_DatabaseBtn.grid(row=3, column=0, padx=20, pady=10)

        # Name Entry
        self.InputTittle = customtkinter.CTkLabel(self, text="INPUT SAMPAH", font=customtkinter.CTkFont(size=50, weight="bold"))
        self.InputTittle.grid(row=0, column=1, columnspan=2, padx=20, pady=20, sticky="nsew")
        self.nameEntry = customtkinter.CTkEntry(self, placeholder_text="Masukkan Nama...", font=customtkinter.CTkFont(size=30))
        self.nameEntry.grid(row=1, column=1, columnspan=2, padx=20, pady=20, sticky="new")

        self.trashType = ["Botol Plastik", "Gelas Plastik", "Kardus",
                        "Duplex", "Kertas Koran", "Kertas HVS",
                        "Kertas Buram", "Galon", "Botol Kaca",
                        "Minyak Jenlatah", "Lainnya"]

        self.prices = [2000, 2000, 1200, 800, 4000, 2500, 2200, 5000, 100, 5000, 2000]

        # Sampah Grid
        self.gridFrame1 = customtkinter.CTkFrame(self)
        self.gridFrame1.grid(row=2, column=1, padx=(20,5), pady=(0,20), sticky="ew")
        self.gridFrame1.grid_columnconfigure(0, weight=1)

        self.gridFrame2 = customtkinter.CTkFrame(self)
        self.gridFrame2.grid(row=2, column=2, padx=(5,20), pady=(0,20), sticky="ew")
        self.gridFrame2.grid_columnconfigure(0, weight=1)

        self.varPList = [customtkinter.StringVar() for i in range(11)]
        self.varAList = [customtkinter.StringVar() for i in range(11)]
        self.varList = [customtkinter.StringVar() for i in range(11)]

        self.S_Label_list = [customtkinter.CTkLabel(self.gridFrame1 if i < 5 else self.gridFrame2, font=customtkinter.CTkFont(size=15)) for i in range(11)]
        self.S_Label2_list = [customtkinter.CTkLabel(self.gridFrame1 if i < 5 else self.gridFrame2, text="Rp. ", font=customtkinter.CTkFont(size=15)) for i in range(11)]
        self.S_Price_list = [customtkinter.CTkEntry(self.gridFrame1 if i < 5 else self.gridFrame2, textvariable=self.varPList[i], width=100) for i in range(11)]
        self.S_Label3_list = [customtkinter.CTkLabel(self.gridFrame1 if i < 5 else self.gridFrame2, text="/", font=customtkinter.CTkFont(size=15)) for i in range(11)]
        self.S_Amount_list = [customtkinter.CTkEntry(self.gridFrame1 if i < 5 else self.gridFrame2, textvariable=self.varAList[i], width=30) for i in range(11)]
        self.S_Entry_list = [customtkinter.CTkEntry(self.gridFrame1 if i < 5 else self.gridFrame2, textvariable=self.varList[i], width=50) for i in range(11)]

        for i in range(11):
            self.S_Label_list[i].configure(text=self.trashType[i])
            self.S_Label_list[i].grid(row=i if i < 5 else i-5, column=0, padx=(20,0), pady=10, sticky="new")
            self.S_Label2_list[i].grid(row=i if i < 5 else i-5, column=1, padx=(20,5), pady=10, sticky="new")
            self.S_Price_list[i].insert(0, self.prices[i])
            self.S_Price_list[i].grid(row=i if i < 5 else i-5, column=2, padx=(10,5), pady=10, sticky="new")
            self.S_Label3_list[i].grid(row=i if i < 5 else i-5, column=3, padx=5, pady=10, sticky="new")
            self.S_Amount_list[i].grid(row=i if i < 5 else i-5, column=4, padx=(5,5), pady=10, sticky="new")
            self.S_Amount_list[i].insert(0, "1")
            self.S_Entry_list[i].grid(row=i if i < 5 else i-5, column=5, padx=10, pady=10, sticky="new")

        for i in range(11):
            self.varPList[i].trace('w', self.changeTotal)
            self.varAList[i].trace('w', self.changeTotal)
            self.varList[i].trace('w', self.changeTotal)

        #! Money ##########################################################################################################################

        # Price for each trash
        self.trashPrice = [0] * 11
        # Total for each trash
        self.trashTotal = [0] * 11
        # Total money for each trash
        self.trashMoney = [0] * 11
        # Total money
        self.total = 0

        self.totalLabel = customtkinter.CTkLabel(self, text="Total : Rp. 0", font=customtkinter.CTkFont(size=30, weight="bold"))
        self.totalLabel.grid(row=3, column=1, padx=20, pady=(0,20), sticky="w")
        self.InputBtn = customtkinter.CTkButton(self, text="INPUT", font=customtkinter.CTkFont(size=30, weight="bold"), command=self.InputData)
        self.InputBtn.grid(row=4, column=2, padx=20, sticky="e")


    #! Input Data Func #############################################################################################################################

    def InputData(self):
        userName = self.nameEntry.get().upper()
        if userName != "":
            #! PERSON DATA #############################################################################################################################
            self.P_dataList = {}

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
            yStr = int(now.strftime("%Y"))
            mStr = int(now.strftime("%m"))
            dStr = int(now.strftime("%d"))
            
            inputDataList = [self.total]
            inputDataList += [self.trashTotal[i] for i in range(11)]

            #! Person Recap Input #############################################################################################################################

            print("Person Total : ", self.total)
            if self.P_dataList.get(userName) == None:                   # if username not exist
                
                result = messagebox.askquestion("Nama Tidak Terdaftar", "Nama tidak terdaftar\nApakah anda ingin menambahkan {} Kedalam daftar?".format(userName))
                if result == "yes":
                    self.P_dataList[userName] = [0] * 12                    # add new list to the P_dataList with username as key

                    currDataList = [(self.P_dataList[userName][i] + inputDataList[i]) for i in range(12)]
                    self.P_dataList[userName] = currDataList

                    print("\nself.P_dataList :\n", self.P_dataList)

                    # Save data
                    self.file = open("Data.txt", "wb")
                    pickle.dump(self.P_dataList, self.file)
                    self.file.close()
                    currDataList.clear()

                    #! Monthly Recap Input #############################################################################################################################

                    currDataList = [(self.DataDict[yStr][mStr][i] + inputDataList[i]) for i in range(12)]
                    self.DataDict[yStr][mStr] = currDataList

                    print("self.DataDict :\n", self.DataDict)

                    self.file = open("Data Sampah.txt", "wb")
                    pickle.dump(self.DataDict, self.file)
                    self.file.close()

                    #! History Input #############################################################################################################################
                    
                    self.HistoryList = []

                    if os.stat("Data.txt").st_size != 0:
                        self.file = open("Riwayat.txt", "rb")
                        self.HistoryList = pickle.load(self.file)
                        self.file.close()

                    currHistoryText = "- {}/{}/{} {} {} BP:{}, GP:{}, K:{}, D:{}, KK:{}, KH:{}, KB:{}, G:{}, BK:{}, MJ:{}, L:{}".format(
                    dStr, mStr, yStr, userName, self.total, self.trashTotal[0], self.trashTotal[1], self.trashTotal[2], self.trashTotal[3],
                                                    self.trashTotal[4], self.trashTotal[5], self.trashTotal[6], self.trashTotal[7],
                                                    self.trashTotal[8], self.trashTotal[9], self.trashTotal[10])
                    print("currHistoryText :\n", currHistoryText)

                    self.HistoryList.append(currHistoryText)
                    print("HistoryList :\n", self.HistoryList)

                    self.file = open("Riwayat.txt", "wb")
                    pickle.dump(self.HistoryList, self.file)
                    self.file.close()

                    # Updating table
                    if self.DatabaseWindowVar != None:
                        self.DatabaseWindowVar.updateTable()

                    self.nameEntry.delete(0, customtkinter.END)
                    for i in range(11):
                        self.S_Entry_list[i].delete(0, customtkinter.END)
                else:
                    messagebox.showinfo("Info", "Nama tidak terdaftar!")
        else :
            messagebox.showwarning("Warning", "Tolong Masukkan Nama!")

    #! Change Total Label Text Func #############################################################################################################

    def changeTotal(self, *args):
        # StringVar to float
        # amount of each trash
        for i in range(11):
            self.trashPrice[i] = float(0 if self.varPList[i].get() == '' else self.varPList[i].get()) / float(0 if self.varAList[i].get() == '' else self.varAList[i].get())
            self.trashTotal[i] = float(0 if self.varList[i].get() == '' else self.varList[i].get())

            # The money of each trash
            self.trashMoney[i] = self.trashTotal[i] * self.trashPrice[i]

            # Total money'
            self.total += self.trashMoney[i]

        self.totalLabel.configure(text='')
        self.totalLabel.configure(text="Total : Rp. {:,.2f}".format(self.total))

    #! Button Function #############################################################################################################################

    def InputWindow(self):
        print("Input Window")

    def InputHistoryWindow(self):
        print("Input History Window")
        self.HistoryWindow = HistoryWindow(self)

    def DatabaseWindow(self):
        print("Orang Database Window")
        self.DatabaseWindow = OrangDatabaseWindow(self)

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

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.HistoryTittle = customtkinter.CTkLabel(self, text="RIWAYAT", font=customtkinter.CTkFont(size=50, weight="bold"))
        self.HistoryTittle.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")

        self.HistoryList = []

        if os.stat("Data.txt").st_size != 0:
            self.file = open("Riwayat.txt", "rb")
            self.HistoryList = pickle.load(self.file)
            self.file.close()

        print(self.HistoryList)

        self.HistoryFrame = customtkinter.CTkTextbox(self)
        for i in range(len(self.HistoryList)) :
            self.HistoryFrame.insert("0.0", text=self.HistoryList[i] + "\n")
        self.HistoryFrame.grid(row=1, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")

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
        # width= self.winfo_screenwidth()               
        # height= self.winfo_screenheight()
        # self.geometry(f"{width}x{height}+{0}+{0}")

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
        self.tabview.tab("Perorang").grid_rowconfigure(0, weight=1)
        self.tabview.tab("Bulanan").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Bulanan").grid_rowconfigure(0, weight=1)

        self.updateTable()

        self.RenameBtn = customtkinter.CTkButton(self, text="Rename", command=self.rename)
        self.RenameBtn.grid(row=2, column=0, padx=20, pady=20, sticky="e")

        self.lift()
        self.attributes('-topmost', True)
        self.after_idle(self.attributes,'-topmost', False)

    #! Function ####################################################################################################################################

    def rename(self):
        if os.stat("Data.txt").st_size != 0:
            self.file = open("Data.txt", "rb")
            self.P_dataLoad = pickle.load(self.file)
            self.file.close()

        num = simpledialog.askinteger("Rename", "Nomor berapa yang ingin diganti?", parent=self)
        newName = simpledialog.askstring("Rename", "Masukkan nama baru : ", parent=self)
        for key in self.P_dataLoad.keys():
            i = list(self.P_dataLoad.keys()).index(key)
            if i == num-1:
                self.temp = self.P_dataLoad[key]
                self.P_dataLoad.pop(key)
                break
        
        self.P_dataLoad[newName] = self.temp

        self.file = open("Data.txt", "wb")
        pickle.dump(self.P_dataLoad, self.file)
        self.file.close()

        self.updateTable()

    def updateTable(self):
        #! Table Data #############################################################################################################################
        # Load
        # Load person Data
        self.names = ["PARTO", "MARIA", "MULYADI", "SISKA", "HESTRENI",
                "ALEX", "ARI", "MURNI", "RENDI", "ATIK", 
                "DINAR", "HARTI", "HERU", "DIAH", "ASTUTIEK", 
                "MUCHTAR", "ELO"]
        
        self.ListP = ["No.", "Nama", "Tabungan", 
                        "BP", "GP", "K", "D",
                        "KK", "KH", "KB", "G", 
                        "BK", "MJ", "L"]
        self.ListM = ["No.", "Bulan", "Tabungan", 
                        "BP", "GP", "K", "D",
                        "KK", "KH", "KB", "G", 
                        "BK", "MJ", "L"]

        if os.stat("Data.txt").st_size != 0:
            self.file = open("Data.txt", "rb")
            self.P_dataLoad = pickle.load(self.file)
            self.file.close()

        # Load month Data
        if os.stat("Data Sampah.txt").st_size != 0:
            self.file = open("Data Sampah.txt", "rb")
            self.B_dataLoad = pickle.load(self.file)
            print("Recap Monthly :\n", self.B_dataLoad)
            self.file.close()

        self.names = list(self.P_dataLoad.keys())

        #! 14 = no + nama + total + sampah[11]

        self.totalPerson = len(self.names)
        self.TableList_P = [self.ListP]
        self.TableList_P += [[0]*14]*self.totalPerson

        for key in self.P_dataLoad.keys():
            i = list(self.P_dataLoad.keys()).index(key)
            l = [i+1, self.names[i]]
            l += self.P_dataLoad[key]
            l[2] = "Rp. {:,.2f}".format(l[2])
            self.TableList_P[i+1] = l

        print("Person Table List : \n\n", self.TableList_P)

        # create table monthly data
        self.Month = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", 
                        "Agustus", "September", "Oktober", "November", "Desember"]

        self.TableList_B = [self.ListM]
        self.TableList_B += [[0]*14]*12

        now = datetime.now()
        self.yStr = int(now.strftime("%Y"))
        self.mStr = int(now.strftime("%m"))

        self.curr_B_Data = self.B_dataLoad[self.yStr]
        print(list(self.curr_B_Data.keys()))
        for i in self.curr_B_Data.keys():
            l = [i, self.Month[i-1]]
            l += self.curr_B_Data[i]
            l[2] = "Rp. {:,.2f}".format(l[2])
            self.TableList_B[i] = l

        print("Month Table List : \n\n", self.TableList_B)
        #! create table UI #############################################################################################################################
        #! Tabel Perorangan
        self.tableFrameP = customtkinter.CTkScrollableFrame(self.tabview.tab("Perorang"))
        self.tableFrameP.grid(row=0, column=0, sticky="news")

        self.tableP = CTkTable(self.tableFrameP, row=self.totalPerson+1, column=14, values=self.TableList_P, corner_radius=0)
        self.tableP.grid(row=0, column=0)

        for i in range(14):
            if i == 0:
                self.tableP.edit_column(0, width=20)
            elif i == 1 or i == 2:
                continue
            else:
                self.tableP.edit_column(i, width=30)

        #! Tabel Bulanan
        self.tableFrameB = customtkinter.CTkScrollableFrame(self.tabview.tab("Bulanan"))
        self.tableFrameB.grid(row=0, column=0, sticky="news")

        year = list(self.B_dataLoad.keys())
        self.yFrame = [customtkinter.CTkFrame(self.tableFrameB) for i in range(len(self.B_dataLoad))]
        self.yLabel = [customtkinter.CTkLabel(self.yFrame[i], text=year[i], font=customtkinter.CTkFont(size=30, weight="bold")) for i in range(len(self.B_dataLoad))]
        self.tableB = [CTkTable(self.yFrame[i], row=13, column=14, values=self.TableList_B, corner_radius=0) for i in range(len(self.B_dataLoad))]

        for i in range(len(self.B_dataLoad)):
            self.yFrame[i].grid(row=i, column=0)
            self.yLabel[i].grid(row=0, column=0)
            self.tableB[i].grid(row=1, column=0)
            for j in range(14):
                if j == 0:
                    self.tableB[i].edit_column(0, width=20)
                elif j == 1 or j == 2:
                    continue
                else:
                    self.tableB[i].edit_column(j, width=30)


if __name__ == "__main__":
    app = App()
    app.mainloop()

# Build command for customTkinter
# pyinstaller -F BooyooToDo.py --collect-all customtkinter -w
