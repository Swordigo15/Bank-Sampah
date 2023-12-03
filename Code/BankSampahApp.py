import tkinter
from tkinter import messagebox
from tkinter import simpledialog
import customtkinter
from CTkTable import *

import pandas as pd
import openpyxl as op
from openpyxl.styles import Border, Side

import tempfile
import pickle
import math
import os

from datetime import datetime

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("green")

import ctypes
myappid = 'mycompany.myproduct.subproduct.version' 
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.hasLogin = False
        self.DatabaseWindowVar = None

        file = open("Data/Admin.txt", "rb")
        self.LoginData = pickle.load(file)
        print(self.LoginData)
        file.close()
        #! UI #############################################################################################################################
        if self.hasLogin == False:
            self.title("Login")
            self.iconbitmap("Logo.ico")

            self.nameLbl = customtkinter.CTkLabel(self, text="Nama")
            self.passLbl = customtkinter.CTkLabel(self, text="Password")
            self.nameEnt = customtkinter.CTkEntry(self)
            self.passEnt = customtkinter.CTkEntry(self)

            self.nameLbl.grid(row=0, column=0, padx=10, pady=(0,5))
            self.passLbl.grid(row=1, column=0, padx=10, pady=(0,5))
            self.nameEnt.grid(row=0, column=1, padx=10, pady=(0,5))
            self.passEnt.grid(row=1, column=1, padx=10, pady=(0,5))

            self.loginBtn = customtkinter.CTkButton(self, text="Login", command=self.Login)
            self.loginBtn.grid(row=2, column=1, pady=(0,5))

    #! Login Func #############################################################################################################################
    def Login(self):
        if self.nameEnt.get() == self.LoginData[0] and self.passEnt.get() == self.LoginData[1]:
            self.hasLogin = True
            print("Log in")

            self.nameLbl.destroy()
            self.passLbl.destroy()
            self.nameEnt.destroy()
            self.passEnt.destroy()
            self.loginBtn.destroy()

            # configure window
            width= self.winfo_screenwidth()               
            height= self.winfo_screenheight()
            self.title("SIBANKSAM")
            self.geometry(f"{width}x{height}+{-10}+{-5}")
            self.iconbitmap("Logo.ico")
            # self.state("zoomed")
            # self.attributes('-fullscreen', True)

            # configure grid layout (4x4)
            self.grid_columnconfigure((1, 2), weight=1)
            self.grid_rowconfigure((3, 4), weight=1)

            # loginW = LoginWindow(self)

            # Tittle
            self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
            self.sidebar_frame.grid(row=0, column=0, rowspan=6, sticky="nsew")
            self.sidebar_frame.grid_rowconfigure(5, weight=1)
            self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="SIBANKSAM", font=customtkinter.CTkFont(size=20, weight="bold"))
            self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

            # Menu Button
            # self.InputWindowBtn = customtkinter.CTkButton(self.sidebar_frame, text="Input Sampah", command=self.InputWindow)
            # self.InputWindowBtn.grid(row=1, column=0, padx=20, pady=10)
            # self.InputWindowBtn.configure(state="disabled")
            self.InputHistoryBtn = customtkinter.CTkButton(self.sidebar_frame, text="Riwayat Input", command=self.InputHistoryWindow)
            self.InputHistoryBtn.grid(row=1, column=0, padx=20, pady=10)
            self.O_DatabaseBtn = customtkinter.CTkButton(self.sidebar_frame, text="Rekap Data", command=self.DatabaseWindow)
            self.O_DatabaseBtn.grid(row=2, column=0, padx=20, pady=10)
            self.AdminBtn = customtkinter.CTkButton(self.sidebar_frame, text="Admin", command=self.renameAdmin)
            self.AdminBtn.grid(row=3, column=0, padx=20, pady=10)

            # Name Entry
            self.InputTittle = customtkinter.CTkLabel(self, text="INPUT SAMPAH", font=customtkinter.CTkFont(size=50, weight="bold"))
            self.InputTittle.grid(row=0, column=1, columnspan=2, padx=20, pady=20, sticky="nsew")
            self.nameEntry = customtkinter.CTkEntry(self, placeholder_text="Masukkan Nama...", font=customtkinter.CTkFont(size=30))
            self.nameEntry.grid(row=1, column=1, columnspan=2, padx=20, pady=20, sticky="new")

            file = open("Data/Tipe Sampah.txt", "rb")
            self.trashType = pickle.load(file)
            print(self.trashType)

            # Sampah Grid
            self.sf = customtkinter.CTkScrollableFrame(self)
            self.sf.grid(row=2, column=1, rowspan=2, columnspan=2, padx=20, sticky="nsew")
            self.sf.grid_columnconfigure(1, weight=1)

            self.gridFrame1 = customtkinter.CTkFrame(self.sf)
            self.gridFrame1.grid(row=0, column=0, sticky="nsew")
            self.gridFrame1.grid_columnconfigure(0, weight=1)

            self.gridFrame2 = customtkinter.CTkFrame(self.sf)
            self.gridFrame2.grid(row=0, column=1, sticky="nsew")
            self.gridFrame2.grid_columnconfigure(0, weight=1)

            self.UpdateTrashList()

            #! Money ##########################################################################################################################

            self.total = 0

            self.totalLabel = customtkinter.CTkLabel(self, text="Total : Rp. 0", font=customtkinter.CTkFont(size=30, weight="bold"))
            self.totalLabel.grid(row=4, column=1, padx=20, sticky="w")
            self.AddTrashBtn = customtkinter.CTkButton(self, text="Tambah Sampah", font=customtkinter.CTkFont(size=30, weight="bold"), command=self.AddTrash)
            self.AddTrashBtn.grid(row=5, column=1, padx=20, pady=(0,20), sticky="w")
            self.InputBtn = customtkinter.CTkButton(self, text="INPUT", font=customtkinter.CTkFont(size=30, weight="bold"), command=self.InputData)
            self.InputBtn.grid(row=5, column=2, padx=20, pady=(0,20), sticky="e")
        else:
            messagebox.showwarning("Warning", "Nama atau Password Salah!")

    def renameAdmin(self):
        self.nameLgn = simpledialog.askstring("Rename", "Masukkan nama Admin", parent=self)
        if self.nameLgn == None:
            return

        self.passLgn = simpledialog.askstring("Rename", "Masukkan password", parent=self)    
        if self.passLgn == None:
            return

        self.LoginData = [self.nameLgn, self.passLgn]
        file = open("Data/Admin.txt", "wb")
        pickle.dump(self.LoginData, file)
        file.close()

    #! Add Trash Func #############################################################################################################################
    def AddTrash(self):
        nameTrash = simpledialog.askstring("Tambah Sampah",  "Nama  : ", parent=self)
        if nameTrash == None:
            return
        
        priceTrash = simpledialog.askstring("Tambah Sampah", "Harga : ", parent=self)
        if priceTrash == None:
            return

        file = open("Data/Data.txt", "rb")
        dataP = pickle.load(file)
        file.close()

        for key in dataP.keys():
            dataP[key] += [0]

        file = open("Data/Data.txt", "wb")
        pickle.dump(dataP, file)
        file.close()

        file = open("Data/Data Sampah.txt", "rb")
        dataB = pickle.load(file)
        file.close()

        for yKey in dataB.keys():
            # for key in dataB[yKey].keys():
            dataB[yKey][1] += [0]

        file = open("Data/Data Sampah.txt", "wb")
        pickle.dump(dataB, file)
        file.close()

        self.trashType[0] += [nameTrash]
        self.trashType[1] += [priceTrash]

        print(self.trashType)
        file = open("Data/Tipe Sampah.txt", "wb")
        pickle.dump(self.trashType, file)
        file.close()

        self.UpdateTrashList()

    #! Update Trash List Func #############################################################################################################################
    def UpdateTrashList(self):
        self.gridFrame1.destroy()
        self.gridFrame2.destroy()

        self.gridFrame1 = customtkinter.CTkFrame(self.sf)
        self.gridFrame1.grid(row=0, column=0, sticky="nsew")
        self.gridFrame1.grid_columnconfigure(0, weight=1)

        self.gridFrame2 = customtkinter.CTkFrame(self.sf)
        self.gridFrame2.grid(row=0, column=1, sticky="nsew")
        self.gridFrame2.grid_columnconfigure(0, weight=1)

        self.length = len(self.trashType[0])

        # Price for each trash
        self.trashPrice = [0] * self.length
        # Total for each trash
        self.trashTotal = [0] * self.length
        # Total money for each trash
        self.trashMoney = [0] * self.length

        self.varPList = [customtkinter.StringVar() for i in range(self.length)]
        self.varAList = [customtkinter.StringVar() for i in range(self.length)]
        self.varList = [customtkinter.StringVar() for i in range(self.length)]

        midPoint = math.ceil(len(self.trashType[0]))/2
        self.S_Label_list = [customtkinter.CTkLabel(self.gridFrame1 if i < midPoint else self.gridFrame2, font=customtkinter.CTkFont(size=15)) for i in range(self.length)]
        self.S_Label2_list = [customtkinter.CTkLabel(self.gridFrame1 if i < midPoint else self.gridFrame2, text="Rp. ", font=customtkinter.CTkFont(size=15)) for i in range(self.length)]
        self.S_Price_list = [customtkinter.CTkEntry(self.gridFrame1 if i < midPoint else self.gridFrame2, textvariable=self.varPList[i], width=100) for i in range(self.length)]
        self.S_Label3_list = [customtkinter.CTkLabel(self.gridFrame1 if i < midPoint else self.gridFrame2, text="/", font=customtkinter.CTkFont(size=15)) for i in range(self.length)]
        self.S_Amount_list = [customtkinter.CTkEntry(self.gridFrame1 if i < midPoint else self.gridFrame2, textvariable=self.varAList[i], width=30) for i in range(self.length)]
        self.S_Entry_list = [customtkinter.CTkEntry(self.gridFrame1 if i < midPoint else self.gridFrame2, textvariable=self.varList[i], width=50) for i in range(self.length)]

        for i in range(self.length):
            self.S_Label_list[i].configure(text=self.trashType[0][i])
            self.S_Label_list[i].grid(row=i if i < midPoint else i-int(midPoint), column=0, padx=(20,0), pady=10, sticky="new")
            self.S_Label2_list[i].grid(row=i if i < midPoint else i-int(midPoint), column=1, padx=(20,5), pady=10, sticky="new")
            self.S_Price_list[i].insert(0, self.trashType[1][i])
            self.S_Price_list[i].grid(row=i if i < midPoint else i-int(midPoint), column=2, padx=(10,5), pady=10, sticky="new")
            self.S_Label3_list[i].grid(row=i if i < midPoint else i-int(midPoint), column=3, padx=5, pady=10, sticky="new")
            self.S_Amount_list[i].grid(row=i if i < midPoint else i-int(midPoint), column=4, padx=(5,5), pady=10, sticky="new")
            self.S_Amount_list[i].insert(0, "1" if i != 9 else "1.5")
            self.S_Entry_list[i].grid(row=i if i < midPoint else i-int(midPoint), column=5, padx=10, pady=10, sticky="new")

        for i in range(self.length):
            self.varPList[i].trace('w', self.changeTotal)
            self.varAList[i].trace('w', self.changeTotal)
            self.varList[i].trace('w', self.changeTotal)

    #! Input Data Func #############################################################################################################################

    def InputData(self):
        userName = self.nameEntry.get().upper()

        if userName != "":
            #! PERSON DATA #############################################################################################################################
            self.P_dataList = {}

            # Load
            if os.stat("Data/Data.txt").st_size != 0:
                self.file = open("Data/Data.txt", "rb")
                self.P_dataList = pickle.load(self.file)
                self.file.close()
                print(self.P_dataList)
            else:
                self.file = open("Data/Data.txt", "wb")
                pickle.dump(self.P_dataList, self.file)
                self.file.close()

            #! MONTH DATA ##############################################################################################################################

            # Load
            # laod year > month > data to mData
            self.file = open("Data/Data Sampah.txt", "rb")
            self.DataDict = pickle.load(self.file)
            self.file.close()

            now = datetime.now()
            yStr = int(now.strftime("%Y"))
            mStr = int(now.strftime("%m"))
            dStr = int(now.strftime("%d"))
            
            inputDataList = [self.total]
            inputDataList += [self.trashTotal[i] for i in range(self.length)]

            #! Person Recap Input #############################################################################################################################

            print("Person Total : ", self.total)
            if self.P_dataList.get(userName) == None:                   # if username not exist
                
                result = messagebox.askquestion("Nama Tidak Terdaftar", "Nama tidak terdaftar\nApakah anda ingin menambahkan {} Kedalam daftar?".format(userName))
                if result == "yes":
                    self.P_dataList[userName] = [0] * (self.length+1)                   # add new list to the P_dataList with username as key
                else:
                    messagebox.showinfo("Info", "Nama tidak terdaftar!")
                    return

            currDataList = [(self.P_dataList[userName][i] + inputDataList[i]) for i in range(self.length+1)]
            self.P_dataList[userName] = currDataList

            print("\nself.P_dataList :\n", self.P_dataList)

            # Save data
            self.file = open("Data/Data.txt", "wb")
            pickle.dump(self.P_dataList, self.file)
            self.file.close()
            currDataList.clear()

            #! Monthly Recap Input #############################################################################################################################

            # Add monthly data (currYear - 2022) times
            if not (yStr in self.DataDict):      
                mData = {}
                for i in range(13):
                    mData[i+1] = [0] * (self.length+1)

                print()
                print(mData)
                self.DataDict[yStr] = mData

            currDataList = [(self.DataDict[yStr][mStr][i] + inputDataList[i]) for i in range(self.length+1)]
            self.DataDict[yStr][mStr] = currDataList
            
            currYearTotal = [(self.DataDict[yStr][13][i] + inputDataList[i]) for i in range(self.length+1)]
            self.DataDict[yStr][13] = currYearTotal

            print("self.DataDict[2023] :\n", self.DataDict[2024])
            print("self.DataDict[2024] :\n", self.DataDict[2024])

            self.file = open("Data/Data Sampah.txt", "wb")
            pickle.dump(self.DataDict, self.file)
            self.file.close()

            #! History Input #############################################################################################################################
            file = open("Data/Tipe Sampah.txt", "rb")
            trashType = pickle.load(file)
            file.close()

            self.trashTypeArr = []
            self.HistoryList = []

            if os.stat("Data/Data.txt").st_size != 0:
                self.file = open("Data/Riwayat.txt", "rb")
                self.HistoryList = pickle.load(self.file)
                self.file.close()

            currHistoryText = "- {}/{}/{} {} {} ".format(dStr, mStr, yStr, userName, self.total)

            for s, i in enumerate(trashType[0]):
                if self.trashTotal[s] == 0:
                    continue

                currHistoryText += ''.join(next(zip(*i.split()))) + ": {} ".format(self.trashTotal[s])

            print("currHistoryText :\n", currHistoryText)

            self.HistoryList.append(currHistoryText)
            print("HistoryList :\n", self.HistoryList)

            self.file = open("Data/Riwayat.txt", "wb")
            pickle.dump(self.HistoryList, self.file)
            self.file.close()

            # Updating table
            if self.DatabaseWindowVar != None:
                self.DatabaseWindowVar.updateTable()

            self.nameEntry.delete(0, customtkinter.END)
            for i in range(self.length):
                self.S_Entry_list[i].delete(0, customtkinter.END)
        else :
            messagebox.showwarning("Warning", "Tolong Masukkan Nama!")

    #! Change Total Label Text Func #############################################################################################################

    def changeTotal(self, *args):
        # Total money
        self.total = 0
        # StringVar to float
        # amount of each trash
        for i in range(self.length):
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
        self.title("SIBANKSAM")
        self.geometry(f"{1100}x{580}")
        self.iconbitmap("Logo.ico")
        self.after(250, lambda: self.iconbitmap('Logo.ico'))

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.HistoryTittle = customtkinter.CTkLabel(self, text="RIWAYAT", font=customtkinter.CTkFont(size=50, weight="bold"))
        self.HistoryTittle.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")

        self.HistoryList = []

        if os.stat("Data/Data.txt").st_size != 0:
            self.file = open("Data/Riwayat.txt", "rb")
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
        self.title("SIBANKSAM")
        self.geometry(f"{1100}x{580}")
        self.iconbitmap("Logo.ico")
        self.after(250, lambda: self.iconbitmap('Logo.ico'))
        # width= self.winfo_screenwidth()               
        # height= self.winfo_screenheight()
        # self.geometry(f"{width}x{height}+{0}+{0}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.ODBTittle = customtkinter.CTkLabel(self, text="REKAP DATA", font=customtkinter.CTkFont(size=50, weight="bold"))
        self.ODBTittle.grid(row=0, column=0, columnspan=3, padx=20, pady=20, sticky="nsew")

        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=1, column=0, columnspan=3, padx=20, pady=20, sticky="nsew")
        self.tabview.add("Perorang")
        self.tabview.add("Bulanan")
        self.tabview.tab("Perorang").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Perorang").grid_rowconfigure(0, weight=1)
        self.tabview.tab("Bulanan").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Bulanan").grid_rowconfigure(0, weight=1)

        self.updateTable()

        self.RenameBtn = customtkinter.CTkButton(self, text="Rename", command=self.rename)
        self.RenameBtn.grid(row=2, column=2, padx=20, pady=20, sticky="e")
        self.PrintBBtn = customtkinter.CTkButton(self, text="Print Bulanan", command=self.print_B_Recap)
        self.PrintBBtn.grid(row=2, column=1, padx=20, pady=20, sticky="e")
        self.PrintPBtn = customtkinter.CTkButton(self, text="Print Perorang", command=self.print_P_Recap)
        self.PrintPBtn.grid(row=2, column=0, padx=20, pady=20, sticky="e")

        self.lift()
        self.attributes('-topmost', True)
        self.after_idle(self.attributes,'-topmost', False)

    #! Function ####################################################################################################################################

    def rename(self):
        if os.stat("Data/Data.txt").st_size != 0:
            self.file = open("Data/Data.txt", "rb")
            self.P_dataLoad = pickle.load(self.file)
            self.file.close()

        num = simpledialog.askinteger("Rename", "Nomor berapa yang ingin diganti?", parent=self)
        if num == None:
            return
        
        newName = simpledialog.askstring("Rename", "Masukkan nama baru : ", parent=self)
        if newName == None:
            return
        
        newName = newName.upper()
        for key in self.P_dataLoad.keys():
            i = list(self.P_dataLoad.keys()).index(key)
            if i == num-1:
                self.temp = self.P_dataLoad[key]
                self.P_dataLoad.pop(key)
                break
        
        if self.P_dataLoad.get(newName) == None:
            self.P_dataLoad[newName] = self.temp
        else:
            for i in range(11):
                self.P_dataLoad[newName][i] += self.temp[i]


        self.file = open("Data/Data.txt", "wb")
        pickle.dump(self.P_dataLoad, self.file)
        self.file.close()

        self.updateTable()

    #! Print Person Data in excel #############################################################################################################################
    def print_P_Recap(self):
        fileName = tempfile.mktemp(".xlsx")

        printData = pd.DataFrame(self.TableList_P)
        print(printData)

        printData.to_excel(fileName, index=False, header=False)

        excelFile = op.load_workbook(fileName)
        fileSheet = excelFile.active

        cellRange = "A1:{}{}".format(chr(len(self.TableList_P[0]) + 64), len(self.TableList_P))
        endColumn = chr(len(self.TableList_P[0]) + 64)
        print(cellRange)

        border = Side(border_style="thin", color="000000")
        for row in fileSheet[cellRange]:
            for cell in row:
                cell.border = Border(top=border, left=border, right=border, bottom=border)

        fileSheet.column_dimensions["A"].width = 3
        fileSheet.column_dimensions["B"].width = 11
        fileSheet.column_dimensions["C"].width = 10
        for i in self.range_char("D", endColumn):
            fileSheet.column_dimensions[i].width = 3
        excelFile.save(fileName)

        os.startfile(fileName, "print")

    #! Print Monthly Data in excel #############################################################################################################################
    def print_B_Recap(self):
        fileName = tempfile.mktemp(".xlsx")

        printData = {}
        
        data = []
        for y in list(self.TableList_B.keys()):
            data += [["", y]] + self.TableList_B[y]

        printData = pd.DataFrame(data)
        print(printData)

        printData.to_excel(fileName, index=False, header=False)

        excelFile = op.load_workbook(fileName)
        fileSheet = excelFile.active

        now = datetime.now()
        yStr = int(now.strftime("%Y"))

        cellRange = "A1:{}{}".format(chr(len(self.TableList_B[yStr][1]) + 64), (15 * len(self.TableList_B)))
        endColumn = chr(len(self.TableList_B[yStr][1]) + 64)
        print(cellRange)

        border = Side(border_style="thin", color="000000")
        for row in fileSheet[cellRange]:
            for cell in row:
                cell.border = Border(top=border, left=border, right=border, bottom=border)

        fileSheet.column_dimensions["A"].width = 3
        fileSheet.column_dimensions["B"].width = 11
        fileSheet.column_dimensions["C"].width = 10
        for i in self.range_char("D", endColumn):
            fileSheet.column_dimensions[i].width = 3
        excelFile.save(fileName)

        os.startfile(fileName, "print")

    def updateTable(self):
        #! Table Data #############################################################################################################################
        # Load
        # Load person Data
        file = open("Data/Tipe Sampah.txt", "rb")
        trashType = pickle.load(file)
        file.close()

        self.trashTypeArr = []

        for s in trashType[0]:
            self.trashTypeArr += [''.join(next(zip(*s.split())))]
        
        self.ListP = ["No.", "Nama", "Tabungan"]
        self.ListP += self.trashTypeArr
        self.ListM = ["No.", "Bulan", "Tabungan"]
        self.ListM += self.trashTypeArr

        if os.stat("Data/Data.txt").st_size != 0:
            self.file = open("Data/Data.txt", "rb")
            self.P_dataLoad = pickle.load(self.file)
            self.file.close()

        # Load month Data
        if os.stat("Data/Data Sampah.txt").st_size != 0:
            self.file = open("Data/Data Sampah.txt", "rb")
            self.B_dataLoad = pickle.load(self.file)
            print("Recap Monthly :\n", self.B_dataLoad)
            self.file.close()

        self.names = list(self.P_dataLoad.keys())

        #! 14 = no + nama + total + sampah[11]

        self.totalPerson = len(self.names)
        self.TableList_P = [self.ListP]
        self.TableList_P += [[0]*len(self.ListP)]*self.totalPerson
        print("self.TableList_P : \n", self.TableList_P)

        for key in self.P_dataLoad.keys():
            i = list(self.P_dataLoad.keys()).index(key)
            l = [i+1, self.names[i]]
            l += self.P_dataLoad[key]
            l[2] = "{:,.2f}".format(l[2])
            self.TableList_P[i+1] = l

        print("Person Table List : \n\n", self.TableList_P)

        # create table monthly data
        self.Month = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", 
                        "Agustus", "September", "Oktober", "November", "Desember", "Total"]

        self.TableList_B = {}

        print()
        print(self.B_dataLoad)

        for i in list(self.B_dataLoad.keys()): # i = 2023, 2024, ... Year
            # for j in list(self.B_dataLoad[i].keys()): j = 1, 2, ..., 12 Month
            self.TableList_B[i] = [self.ListM]
            self.TableList_B[i] += [(["" if j == 13 else j, self.Month[j-1]] + self.B_dataLoad[i][j]) for j in list(self.B_dataLoad[i].keys())]

        print("Month Table List :\n\n", self.TableList_B)


        #! create table UI #############################################################################################################################

        #! Tabel Perorangan
        self.tableFrameP = customtkinter.CTkScrollableFrame(self.tabview.tab("Perorang"))
        self.tableFrameP.grid(row=0, column=0, sticky="news")

        self.tableP = CTkTable(self.tableFrameP, row=self.totalPerson+1, column=len(self.ListP), values=self.TableList_P, corner_radius=0)
        self.tableP.grid(row=0, column=0)

        for i in range(len(self.ListP)):
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
        self.tableB = [CTkTable(self.yFrame[i], row=14, column=len(self.ListM), values=self.TableList_B[year[i]], corner_radius=0) for i in range(len(self.B_dataLoad))]

        for i in range(len(year)):
            self.yFrame[i].grid(row=i, column=0)
            self.yLabel[i].grid(row=0, column=0)
            self.tableB[i].grid(row=1, column=0)
            for j in range(len(self.ListM)):
                if j == 0:
                    self.tableB[i].edit_column(0, width=20)
                elif j == 1 or j == 2:
                    continue
                else:
                    self.tableB[i].edit_column(j, width=30)

    def range_char(self, start, stop):
        return (chr(n) for n in range(ord(start), ord(stop) + 1))

if __name__ == "__main__":
    app = App()
    app.mainloop()

# Build command for customTkinter
# pyinstaller -F -i "Logo.ico" BankSampahApp.py --collect-all customtkinter -w
