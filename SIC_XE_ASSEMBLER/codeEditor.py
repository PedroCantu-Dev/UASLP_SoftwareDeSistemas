from pathlib import Path
import os
from tkinter import *
from tkinter import messagebox
from tkinter.messagebox import *
from tkinter.filedialog import *
from tkinter.ttk import Treeview
import memory as mem
import webbrowser
from SICXE import *


class Sicxe_GUI:

    def __thisSourceFileKeyPressed(event):
        __savedFileFlag = False
    __root = Tk()

    __savedFileFlag = True
    __file = None

    ###############
    # Menu de opciones:
    ##############
    # for menu bar at the top of the window
    __thisMenuBar = Menu(__root)
    __thisFileMenu = Menu(__thisMenuBar, tearoff=0)
    __thisAssemblerMenu = Menu(__thisMenuBar, tearoff=0)
    __thisSimulationMenu = Menu(__thisMenuBar, tearoff=0)
    __thisHelpMenu = Menu(__thisMenuBar, tearoff=0)

    ######################
    # Archivo fuente SICXE:
    ####################
    __sourceFileLabel = LabelFrame(__root, text="Source File")
    __thisSourceFile = Text(__sourceFileLabel, undo=True, wrap=NONE)
    __thisSourceFileScrollBar = Scrollbar(__thisSourceFile)
    __thisSourceFileScrollBarX = Scrollbar(
        __thisSourceFile, orient='horizontal')
    __thisSourceFile.bind('<KeyRelease>', __thisSourceFileKeyPressed)

    ######################
    # Archivo intermedio
    ####################
    __InterFileLabel = LabelFrame(__root, text="Intermediate File")
    columnsInter = ('#1', '#2', '#3', '#4', '#5', '#6', '#7',  '#8')
    __thisIntermediateFileTree = Treeview(
        __InterFileLabel, columns=columnsInter, show='headings')
    # define headings
    # [blockName, actualCounterLoc, label, mnemonic, operands, '.'])
    __thisIntermediateFileTree.column('#1', anchor=CENTER, width=50)
    __thisIntermediateFileTree.heading('#1', text='Index')
    __thisIntermediateFileTree.column('#2', anchor=CENTER, width=100)
    __thisIntermediateFileTree.heading('#2', text='Sección')
    __thisIntermediateFileTree.column('#3', anchor=CENTER, width=100)
    __thisIntermediateFileTree.heading('#3', text='Bloque')
    __thisIntermediateFileTree.column('#4', anchor=CENTER, width=75)
    __thisIntermediateFileTree.heading('#4', text='PC')
    __thisIntermediateFileTree.column('#5', anchor=CENTER, width=100)
    __thisIntermediateFileTree.heading('#5', text='Label')
    __thisIntermediateFileTree.column('#6', anchor=CENTER, width=100)
    __thisIntermediateFileTree.heading('#6', text='Mnemonico')
    __thisIntermediateFileTree.column('#7', anchor=CENTER, width=360)
    __thisIntermediateFileTree.heading('#7', text='Operando')
    __thisIntermediateFileTree.column('#8', anchor=CENTER, width=360)
    __thisIntermediateFileTree.heading('#8', text='Obj/Error')
    # __thisIntermediateFileTree.tag_config(background="black",
    #   foreground="red")
    # definiendo los scroll bars:
    __thisIntermediateFileScrollBarY = Scrollbar(__thisIntermediateFileTree)
    __thisIntermediateFileScrollBarX = Scrollbar(
        __thisIntermediateFileTree, orient='horizontal')

    ######################
    # Tabla de memoria:
    ####################
    __thisMemoryTabLabel = LabelFrame(__root, text="Memory")
    # la tabla de bloques
    columnsInter = ('#0', '#1', '#2', '#3', '#4', '#5', '#6', '#7',
                    '#8', '#9', '#10', '#11', '#12', '#13', '#14', '#15')
    __thisMemoryTabTree = Treeview(
        __thisMemoryTabLabel, columns=columnsInter, show='headings')
    # define headings
    # [blockName, actualCounterLoc, label, mnemonic, operands, '.'])
    __thisMemoryTabTree.column('#1', anchor=CENTER, width=150)
    __thisMemoryTabTree.heading('#1', text='Dir')
    __thisMemoryTabTree.column('#2', anchor=CENTER, width=50)
    __thisMemoryTabTree.heading('#2', text='0')
    __thisMemoryTabTree.column('#3', anchor=CENTER, width=50)
    __thisMemoryTabTree.heading('#3', text='1')
    __thisMemoryTabTree.column('#4', anchor=CENTER, width=50)
    __thisMemoryTabTree.heading('#4', text='2')
    __thisMemoryTabTree.column('#5', anchor=CENTER, width=50)
    __thisMemoryTabTree.heading('#5', text='3')
    __thisMemoryTabTree.column('#6', anchor=CENTER, width=50)
    __thisMemoryTabTree.heading('#6', text='4')
    __thisMemoryTabTree.column('#7', anchor=CENTER, width=50)
    __thisMemoryTabTree.heading('#7', text='5')
    __thisMemoryTabTree.column('#8', anchor=CENTER, width=50)
    __thisMemoryTabTree.heading('#8', text='6')
    __thisMemoryTabTree.column('#9', anchor=CENTER, width=50)
    __thisMemoryTabTree.heading('#9', text='8')
    __thisMemoryTabTree.column('#10', anchor=CENTER, width=50)
    __thisMemoryTabTree.heading('#10', text='9')
    __thisMemoryTabTree.column('#11', anchor=CENTER, width=50)
    __thisMemoryTabTree.heading('#11', text='A')
    __thisMemoryTabTree.column('#12', anchor=CENTER, width=50)
    __thisMemoryTabTree.heading('#12', text='B')
    __thisMemoryTabTree.column('#13', anchor=CENTER, width=50)
    __thisMemoryTabTree.heading('#13', text='C')
    __thisMemoryTabTree.column('#14', anchor=CENTER, width=50)
    __thisMemoryTabTree.heading('#14', text='D')
    __thisMemoryTabTree.column('#15', anchor=CENTER, width=50)
    __thisMemoryTabTree.heading('#15', text='E')
    __thisMemoryTabTree.column('#16', anchor=CENTER, width=65)
    __thisMemoryTabTree.heading('#16', text='F')
    # definiendo los scroll bars:
    __thisMemoryTabScrollBarY = Scrollbar(__thisMemoryTabTree)
    __thisMemoryTabScrollBarX = Scrollbar(
        __thisMemoryTabTree, orient='horizontal')

    ######################
    # Tabla de symbolos
    ####################
    __TabSymLabel = LabelFrame(__root, text="Symbol Table")
    columnsTabSym = ('#1', '#2', '#3', '#4', '#5', '#6')
    __thisTabSymFileTree = Treeview(
        __TabSymLabel, columns=columnsTabSym, show='headings')
    # define headings
    __thisTabSymFileTree.column('#1', anchor=CENTER, width=150)
    __thisTabSymFileTree.heading('#1', text='Symbol')
    __thisTabSymFileTree.column('#2', anchor=CENTER, width=150)
    __thisTabSymFileTree.heading('#2', text='dir/val')
    __thisTabSymFileTree.column('#3', anchor=CENTER, width=50)
    __thisTabSymFileTree.heading('#3', text='type')
    __thisTabSymFileTree.column('#4', anchor=CENTER, width=150)
    __thisTabSymFileTree.heading('#4', text='Seccion')
    __thisTabSymFileTree.column('#5', anchor=CENTER, width=100)
    __thisTabSymFileTree.heading('#5', text='Bloque')
    __thisTabSymFileTree.column('#6', anchor=CENTER, width=100)
    __thisTabSymFileTree.heading('#6', text='symExt')

    __thisTabSymFileScrollBarY = Scrollbar(__thisTabSymFileTree)
    __thisTabSymFileScrollBarX = Scrollbar(
        __thisTabSymFileTree, orient='horizontal')

    ######################
    # Tabla de bloques
    ####################
    __TabBlocksLabel = LabelFrame(__root, text="Blocks Table")
    columnsTabBlocks = ('#1', '#2', '#3', '#4')
    __thisTabBlocksFileTree = Treeview(
        __TabBlocksLabel, columns=columnsTabBlocks, show='headings')
    # define headings
    __thisTabBlocksFileTree.column('#1', anchor=CENTER, width=150)
    __thisTabBlocksFileTree.heading('#1', text='Section')
    __thisTabBlocksFileTree.column('#2', anchor=CENTER, width=150)
    __thisTabBlocksFileTree.heading('#2', text='Block Name')
    __thisTabBlocksFileTree.column('#3', anchor=CENTER, width=100)
    __thisTabBlocksFileTree.heading('#3', text='Dir Init')
    __thisTabBlocksFileTree.column('#4', anchor=CENTER, width=150)
    __thisTabBlocksFileTree.heading('#4', text='Size')

    __thisTabBlocksFileScrollBarY = Scrollbar(__thisTabBlocksFileTree)
    __thisTabBlocksFileScrollBarX = Scrollbar(
        __thisTabBlocksFileTree, orient='horizontal')

    ######################
    # Errors File
    ####################
    # index ,sentence , type, description
    __ErrorsLabel = LabelFrame(__root, text="Errors File")
    columnsErrorTable = ('#1', '#2', '#3', '#4', '#5')
    __thisErrorTableFileTree = Treeview(
        __ErrorsLabel, columns=columnsErrorTable, show='headings')
    # define headings
    __thisErrorTableFileTree.column('#1', anchor=CENTER, width=80)
    __thisErrorTableFileTree.heading('#1', text='Line index')
    __thisErrorTableFileTree.column('#2', anchor=CENTER, width=200)
    __thisErrorTableFileTree.heading('#2', text='CP')
    __thisErrorTableFileTree.column('#3', anchor=CENTER, width=200)
    __thisErrorTableFileTree.heading('#3', text='sentence')
    __thisErrorTableFileTree.column('#4', anchor=CENTER, width=200)
    __thisErrorTableFileTree.heading('#4', text='type')
    __thisErrorTableFileTree.column('#5', anchor=CENTER, width=450)
    __thisErrorTableFileTree.heading('#5', text='description')

    __thisErrorTableFileScrollBarY = Scrollbar(__thisErrorTableFileTree)
    __thisErrorTableFileScrollBarX = Scrollbar(
        __thisErrorTableFileTree, orient='horizontal')

    ######################
    # El campo de los registros:
    ####################
    __registerFileLabel = LabelFrame(__root, text="Registers")
    __thisRegisterFile = Text(__registerFileLabel, wrap=NONE, state=DISABLED)
    __thisRegisterFileScrollBar = Scrollbar(__thisRegisterFile)
    __thisRegisterFileScrollBarX = Scrollbar(
        __thisRegisterFile, orient='horizontal')

    def __init__(self, **kwargs):
        # Set icon
        try:
            self.__root.wm_iconbitmap("Notepad.ico")
        except:
            pass
        try:
            self.__thisWidth = kwargs['width']
        except KeyError:
            pass
        try:
            self.__thisHeight = kwargs['height']
        except KeyError:
            pass

        # Set the window text
        self.__root.title("SicXe assembly")

        # For top and bottom
        self.__root.geometry('1080x720')

        ###############
        # Menu de opciones:
        ##############

        ######################
        # Archivo fuente SICXE:
        ####################
        self.__sourceFileLabel.place(relx=0, rely=0, relheight=1, relwidth=1/3)
        self.__thisSourceFile.place(relx=0, rely=0, relheight=1, relwidth=1)
        # scroll para el archivo fuente
        self.__thisSourceFileScrollBarX.pack(side=BOTTOM, fill='x')
        self.__thisSourceFileScrollBarX.config(
            command=self.__thisSourceFile.xview)
        self.__thisSourceFile.config(
            xscrollcommand=self.__thisSourceFileScrollBarX.set)

        self.__thisSourceFileScrollBar.pack(side=RIGHT, fill=Y)
        self.__thisSourceFileScrollBar.config(
            command=self.__thisSourceFile.yview)
        self.__thisSourceFile.config(
            yscrollcommand=self.__thisSourceFileScrollBar.set)

        ######################
        # Archivo intermedio
        ####################
        self.__InterFileLabel.place(
            relx=1/3, rely=0, relheight=1/2, relwidth=1/3)
        self.__thisIntermediateFileTree.place(
            relx=0, rely=0, relheight=1, relwidth=1)
        # scroll para el archivo intermedio:
        self.__thisIntermediateFileScrollBarX.pack(side=BOTTOM, fill='x')
        self.__thisIntermediateFileScrollBarX.config(
            command=self.__thisIntermediateFileTree.xview)
        self.__thisIntermediateFileTree.config(
            xscrollcommand=self.__thisIntermediateFileScrollBarX.set)

        self.__thisIntermediateFileScrollBarY.pack(side=RIGHT, fill=Y)
        self.__thisIntermediateFileScrollBarY.config(
            command=self.__thisIntermediateFileTree.yview)
        self.__thisIntermediateFileTree.config(
            yscrollcommand=self.__thisIntermediateFileScrollBarY.set)

        ######################
        # Tabla de memoria:
        ####################
        self.__thisMemoryTabLabel.place(
            relx=1/3, rely=1/2, relheight=1/2, relwidth=1/3)
        self.__thisMemoryTabTree.place(
            relx=0, rely=0, relheight=1, relwidth=1)
        # scroll para la tabla de simbolos
        self.__thisMemoryTabScrollBarX.pack(side=BOTTOM, fill='x')
        self.__thisMemoryTabScrollBarX.config(
            command=self.__thisMemoryTabTree.xview)
        self.__thisMemoryTabTree.config(
            xscrollcommand=self.__thisMemoryTabScrollBarX.set)

        self.__thisMemoryTabScrollBarY.pack(side=RIGHT, fill=Y)
        self.__thisMemoryTabScrollBarY.config(
            command=self.__thisMemoryTabTree.yview)
        self.__thisMemoryTabTree.config(
            yscrollcommand=self.__thisMemoryTabScrollBarY.set)

        ######################
        # Tabla de symbolos
        ####################
        self.__TabSymLabel.place(relx=2/3, rely=0, relheight=1/4, relwidth=1/3)
        self.__thisTabSymFileTree.place(
            relx=0, rely=0, relheight=1, relwidth=1)
        # scroll para la tabla de simbolos
        self.__thisTabSymFileScrollBarX.pack(side=BOTTOM, fill='x')
        self.__thisTabSymFileScrollBarX.config(
            command=self.__thisTabSymFileTree.xview)
        self.__thisTabSymFileTree.config(
            xscrollcommand=self.__thisTabSymFileScrollBarX.set)

        self.__thisTabSymFileScrollBarY.pack(side=RIGHT, fill=Y)
        self.__thisTabSymFileScrollBarY.config(
            command=self.__thisTabSymFileTree.yview)
        self.__thisTabSymFileTree.config(
            yscrollcommand=self.__thisTabSymFileScrollBarY.set)

        ######################
        # Tabla de bloques
        ####################
        self.__TabBlocksLabel.place(
            relx=2/3, rely=1/4, relheight=1/4, relwidth=1/3)
        self.__thisTabBlocksFileTree.place(
            relx=0, rely=0, relheight=1, relwidth=1)
        # scroll para la tabla de errores:
        self.__thisTabBlocksFileScrollBarX.pack(side=BOTTOM, fill='x')
        self.__thisTabBlocksFileScrollBarX.config(
            command=self.__thisTabBlocksFileTree.xview)
        self.__thisTabBlocksFileTree.config(
            xscrollcommand=self.__thisTabBlocksFileScrollBarX.set)

        self.__thisTabBlocksFileScrollBarY.pack(side=RIGHT, fill=Y)
        self.__thisTabBlocksFileScrollBarY.config(
            command=self.__thisTabBlocksFileTree.yview)
        self.__thisTabBlocksFileTree.config(
            yscrollcommand=self.__thisTabBlocksFileScrollBarY.set)

        ######################
        # Errors File
        ####################
        self.__ErrorsLabel.place(
            relx=2/3, rely=2/4, relheight=1/4, relwidth=1/3)
        self.__thisErrorTableFileTree.place(
            relx=0, rely=0, relheight=1, relwidth=1)
        # scroll para la tabla de errores:
        self.__thisErrorTableFileScrollBarX.pack(side=BOTTOM, fill='x')
        self.__thisErrorTableFileScrollBarX.config(
            command=self.__thisErrorTableFileTree.xview)
        self.__thisErrorTableFileTree.config(
            xscrollcommand=self.__thisErrorTableFileScrollBarX.set)

        self.__thisErrorTableFileScrollBarY.pack(side=RIGHT, fill=Y)
        self.__thisErrorTableFileScrollBarY.config(
            command=self.__thisErrorTableFileTree.yview)
        self.__thisErrorTableFileTree.config(
            yscrollcommand=self.__thisErrorTableFileScrollBarY.set)

        ######################
        # El campo de los registros:
        ####################
        self.__registerFileLabel.place(
            relx=2/3, rely=3/4, relheight=1/4, relwidth=1/3)
        self.__thisRegisterFile.place(relx=0, rely=0, relheight=1, relwidth=1)
        # scroll para los registros:
        # Scrollbar will adjust automatically according to the content
        self.__thisRegisterFileScrollBarX.pack(side=BOTTOM, fill='x')
        self.__thisRegisterFileScrollBarX.config(
            command=self.__thisRegisterFile.xview)
        self.__thisRegisterFile.config(
            xscrollcommand=self.__thisRegisterFileScrollBarX.set)

        self.__thisRegisterFileScrollBar.pack(side=RIGHT, fill=Y)
        self.__thisRegisterFileScrollBar.config(
            command=self.__thisRegisterFile.yview)
        self.__thisRegisterFile.config(
            yscrollcommand=self.__thisRegisterFileScrollBar.set)

        # To open new file
        self.__thisFileMenu.add_command(label="New",
                                        command=self.__newFile)

        # To open a already existing file
        self.__thisFileMenu.add_command(label="Open",
                                        command=self.__openFile)

        # To save current file
        self.__thisFileMenu.add_command(label="Save",
                                        command=self.__saveFile)

        # To saveas current file
        self.__thisFileMenu.add_command(label="SaveAs",
                                        command=self.__saveAsFile)

        # To create a line in the dialog
        self.__thisFileMenu.add_separator()
        self.__thisFileMenu.add_command(label="Exit",
                                        command=self.__quitApplication)
        self.__thisMenuBar.add_cascade(label="File",
                                       menu=self.__thisFileMenu)

        # To give a feature of cut
        self.__thisAssemblerMenu.add_command(label="Assemble",
                                             command=self.__assemble)

        # to give a feature of copy
        self.__thisAssemblerMenu.add_command(label="Pass1",
                                             command=self.__pass1)

        # To give a feature of paste
        self.__thisAssemblerMenu.add_command(label="Pass2",
                                             command=self.__pass2)

        # To give a feature of assembrer
        self.__thisMenuBar.add_cascade(label="Assembler",
                                       menu=self.__thisAssemblerMenu)

        self.__thisMenuBar.add_command(label="Simulation",
                                       command=self.__thisSimulationMenu)

        # To create a feature of description of the notepad
        self.__thisHelpMenu.add_command(label="About the project",
                                        command=self.__showAbout)

        self.__thisMenuBar.add_cascade(label="Help",
                                       menu=self.__thisHelpMenu)

        self.__root.config(menu=self.__thisMenuBar)

    def __quitApplication(self):
        self.__root.destroy()
        # exit()

    def __showAbout(self):
        MsgBox_SI = messagebox.askquestion(
            'Documentation', 'Are you sure you want to open documentation on the browser?', icon='question')
        if MsgBox_SI == 'yes':
            webbrowser.open(
                "https://github.com/Pedejeca135/SoftwareDeSistemas_UASLP")
        # else:
        #     messagebox.showinfo('Return','You will now return to the application screen')

    def __openFile(self):
        if self.__savedFileFlag == False:
            save = self.__showSaveChanges(self)
            if (save == True):
                self.__saveFile(self)

        self.__file = askopenfilename(initialdir=os.getcwd(
        )+"\\"+"SIC-XE_Programs", filetypes=[("SIC-XE Files", "*.xe")])

        if self.__file == "":

            # no file to open
            self.__file = None
        else:
            # Try to open the file
            # set the window title
            self.__root.title(os.path.basename(
                self.__file) + " - SicXe Assembly")
            self.__thisSourceFile.delete(1.0, END)

            file = open(self.__file, "r")

            self.__thisSourceFile.insert(1.0, file.read())
            # textColored = "un texto X"
            # textColored.tag_config("start", background="black",
            #                        foreground="red")
            file.close()
            __savedFileFlag = True

    def __newFile(self):
        self.__root.title("Untitled - SicXe Assembly")
        self.__file = None
        self.__thisSourceFile.delete(1.0, END)
        __savedFileFlag = True
        self.cleanOpenNewFile()

    def __showSaveChanges(self):
        MsgBox_SI = messagebox.askquestion(
            'Save File', 'Save changes?', icon='question')
        if MsgBox_SI == 'yes':
            return True
        else:
            return False

    def __saveFile(self):
        if self.__file == None:
            # Save as new file
            self.__file = asksaveasfilename(initialfile='Untitled.xe',
                                            defaultextension=".xe",
                                            filetypes=[("All Files", "*.*"),
                                                       ("Text Documents", "*.txt"),
                                                       ("SIC-XE Files", "*.xe")
                                                       ])
            if self.__file == "":
                self.__file = None
            else:
                # Try to save the file
                file = open(self.__file, "w")
                file.write(self.__thisSourceFile.get(1.0, END))
                file.close()
                __savedFileFlag = True
                # Change the window title
                self.__root.title(os.path.basename(
                    self.__file) + " - SicXe Assembly")
        else:
            file = open(self.__file, "w")
            file.write(self.__thisSourceFile.get(1.0, END))
            file.close()

    def __saveAsFile(self):
        self.__file = asksaveasfilename(initialfile='Untitled.xe',
                                        defaultextension=".xe",
                                        filetypes=[("All Files", "*.*"),
                                                   ("Text Documents", "*.txt"),
                                                   ("SIC-XE Files", "*.xe")
                                                   ])
        if self.__file == "":
            self.__file = None
        else:
            # Try to save the file
            file = open(self.__file, "w")
            file.write(self.__thisSourceFile.get(1.0, END))
            file.close()
            __savedFileFlag = True
            # Change the window title
            self.__root.title(os.path.basename(
                self.__file) + " - SicXe Assembly")

    intermediateFile = None
    tabSym = None

    def cleanWhenPass1(self):
        self.intermediateFile = None
        for i in self.__thisIntermediateFileTree.get_children():
            self.__thisIntermediateFileTree.delete(i)
        for i in self.__thisTabSymFileTree.get_children():
            self.__thisTabSymFileTree.delete(i)
        for i in self.__thisErrorTableFileTree.get_children():
            self.__thisErrorTableFileTree.delete(i)
        self.tableSym = None

    def cleanWhenPass2(self):
        for i in self.__thisIntermediateFileTree.get_children():
            self.__thisIntermediateFileTree.delete(i)
        calc.setEND()
        calc.setBASES(self.sections)

    def refresh(self):
        self.destroy()
        self.__init__()

    def getCleanMemory():
        memory = {}
        dirCounter = 0
        for i in range((2**20)/15):
            memoryRow = []
            for j in range(16):
                memoryRow.append('FF')
            memory[calc.SIC_HEX(dirCounter)] = memoryRow
            dirCounter + 16

    def __getAssembledFolderPrefix(self, fileName):
        assembledFolderPrefix = os.path.dirname(
            __file__)+"/assembled/" + fileName + "/"
        # for assembled folder creation
        if not os.path.exists(assembledFolderPrefix):
            os.makedirs(assembledFolderPrefix)
        return assembledFolderPrefix

    assembledFolderPrefix = ""
    intermediateFileName = ""

    def __pass1(self):
        # llama al metodo para generar una lista de lineas apartir del archivo|
        # call readLines method for generating
        self.cleanWhenPass1()
        lines = self.__thisSourceFile.get("1.0", "end")
        if (lines and lines != '\n'):
            # lines = open(file).readlines()
            # llama al paso 1 |
            # call step one
            lines = lines.split("\n")
            passOneReturn = passOne(lines)

            # asignando los valores con lo que retorna el paso 1
            self.intermediateFile = passOneReturn['interFile']
            self.errors = passOneReturn['errorsFile']
            self.intermediateFileName = passOneReturn['nameSTART']
            self.assembledFolderPrefix = self.__getAssembledFolderPrefix(
                self.intermediateFileName)
            self.sections = passOneReturn['secciones']

            # Intermediate File, plot and save
            interFile = open(self.assembledFolderPrefix +
                             self.intermediateFileName+'_pass1'+'.arc', "w+")

            for line in self.intermediateFile:
                if (line != '.'):
                    for field in line:
                        if (field != '.'):
                            interFile.writelines(str(field))
                            interFile.writelines("|")
                    self.__thisIntermediateFileTree.insert(
                        '', END, values=(line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7]))
                    interFile.writelines("\n")

            interFile.close()

            # archivo de errores , plot y save
            # error table
            if (len(self.errors) > 0):
                errorFile = open(self.assembledFolderPrefix +
                                 self.intermediateFileName+'.err', "w+")
                for errorLine in self.errors:
                    errorFile.writelines(
                        str(errorLine[0]) + "|" + errorLine[1]+"|" + errorLine[2]+"|" + errorLine[3]+"|")
                    errorFile.writelines(" ")
                    codeLine = errorLine[4] + " " + \
                        errorLine[5] + " " + errorLine[6]
                    errorFile.writelines(codeLine)
                    errorFile.writelines(" ")
                    errorFile.writelines("|")
                    errorFile.writelines(errorLine[7])
                    errorFile.writelines("\n")

                    errDescription = errorLine[7].split(":")
                    errType = errDescription[2]
                    errDescription = errDescription[3]

                    self.__thisErrorTableFileTree.insert('', END, values=(
                        errorLine[0], errorLine[1]+"/"+errorLine[2]+"/CP:"+errorLine[3], codeLine, errType, errDescription))
                errorFile.close()

            # para los archivos que se generan en cada seccion:
            for indexSection, seccionName in enumerate(self.sections):
                # haciendo los archivos de la tabla de bloques:
                blockFile = open(self.assembledFolderPrefix +
                                 self.intermediateFileName+"_"+seccionName+'.blq', "w+")
                tabBlocks = self.sections[seccionName]['tabblock']
                for indexBlock, blockName in enumerate(tabBlocks):
                    blockRow = tabBlocks[blockName]

                    blockFile.writelines(blockName)
                    blockFile.writelines("|")
                    blockFile.writelines(blockRow['dirIniRel'])
                    blockFile.writelines("|")
                    blockFile.writelines(blockRow['len'])
                    blockFile.writelines("\n")
                    self.__thisTabBlocksFileTree.insert('', END, values=(seccionName,
                                                                         blockName, blockRow['dirIniRel'], blockRow['len']))
                blockFile.close()

                # haciendo los archivos de la tabla de sibolos:
                tabFile = open(self.assembledFolderPrefix +
                               self.intermediateFileName+"_"+seccionName+'.tab', "w+")
                tabSym = self.sections[seccionName]['tabsym']
                for indexSym, symName in enumerate(tabSym):
                    symRow = tabSym[symName]

                    tabFile.writelines(symName)
                    tabFile.writelines("|")
                    tabFile.writelines(symRow['dirVal'])
                    tabFile.writelines("|")
                    tabFile.writelines(symRow['type'])
                    tabFile.writelines("|")
                    tabFile.writelines(symRow['block'])
                    tabFile.writelines("|")
                    tabFile.writelines(str(symRow['symExt']))
                    tabFile.writelines("\n")
                    self.__thisTabSymFileTree.insert('', END, values=(symName,
                                                                      symRow['dirVal'], symRow['type'], seccionName, symRow['block'], str(symRow['symExt'])))
                tabFile.close()

    def makeHexString(self, vari):
        if (type(vari) is int):
            return self.makeHexString(hex(vari))
        try:
            int(vari, 16)
            return vari.replace('0x', '')
        except:
            return '0'

    def __pass2(self):
        if (not self.intermediateFile or not self.sections):
            self.__pass1()
        self.cleanWhenPass2()
        self.passTwoReturn = passTwo(self.intermediateFile, self.sections)

        # Intermediate File, plot and save
        interFile = open(self.assembledFolderPrefix +
                         self.intermediateFileName+'_pass2'+'.arc', "w+")

        # Intermediate File, plot and save
        for line in self.intermediateFile:
            if (line != '.'):
                for field in line:
                    if (field != '.'):
                        interFile.writelines(str(field))
                        interFile.writelines("|")
                interFile.writelines("\n")
                self.__thisIntermediateFileTree.insert(
                    '', END, values=(line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7]))
        interFile.close()

        registers = self.passTwoReturn['registers']

        objFileLines = ''
        for indexSection, seccionName in enumerate(self.sections):
            # creando el archivo de los registros
            registerFile = open(self.assembledFolderPrefix +
                                self.intermediateFileName+"_"+seccionName+'.obj', "w+")

            # registro H
            tabBlocks = self.sections[seccionName]['tabblock']
            initialDir = list(tabBlocks.values())[0]['dirIniRel']
            dirIniFinal = calc.getIntBy_SicXe_HexOrInt(
                list(tabBlocks.values())[-1]['dirIniRel'], True)
            tamFinal = calc.getIntBy_SicXe_HexOrInt(
                list(tabBlocks.values())[-1]['len'], True)
            length = calc.SIC_HEX(dirIniFinal + tamFinal)

            HRegLine = "H" + calc.fillOrCutL(seccionName) + calc.fillOrCutR(
                initialDir) + calc.fillOrCutR(length)+'\n'

            regInsertion = HRegLine+registers[seccionName]['registers']
            registerFile.writelines(regInsertion)
            registerFile.close()
            objFileLines += regInsertion+'\n\n'

        self.__thisRegisterFile.config(state=NORMAL)
        self.__thisRegisterFile.insert(1.0, objFileLines)
        self.__thisRegisterFile.config(state=DISABLED)

        # self.makeRegisters()
# self.__thisTextArea.event_generate("<<Cut>>")
        # self.__thisTextArea.event_generate("<<Paste>>")

    def __assemble(self):
        self.__pass2()
        self.cleanMemory()
        self.assemblePassOne()
        self.assemblePassTwo()

    def assemblePassOne(self):
        self.dirprog = 12309
        # self.dirprog = 16
        dirsc = self.dirprog

        self.tabse = {}
        errorFlag = False

        for entry in self.passTwoReturn['registers']:
            if (errorFlag):
                break
            if (entry in self.tabse.keys()):
                errorFlag = True
            else:
                sectionRegSplited = self.passTwoReturn['registers'][entry]['registers'].split(
                    '\n')
                hreg = sectionRegSplited[0]
                lonsc = hreg[len(hreg)-6:]
                lonsc = calc.getIntBy_SicXe_HexOrInt(lonsc, True)
                # tabBlocks = self.sections[entry]['tabblock']
                # dirIniFinal = calc.getIntBy_SicXe_HexOrInt(
                #     list(tabBlocks.values())[-1]['dirIniRel'], True)
                # tamFinal = calc.getIntBy_SicXe_HexOrInt(
                #     list(tabBlocks.values())[-1]['len'], True)
                # lonsc = dirIniFinal + tamFinal

                self.tabse[entry] = {'dir': calc.SIC_HEX(dirsc),
                                     'len': calc.SIC_HEX(lonsc), 'sym': {}}

                for reg in sectionRegSplited:
                    if (reg[0] == 'E'):
                        break
                    if (reg[0] == 'D'):
                        index = 1
                        while (True):
                            try:
                                name = reg[index:index+6]
                                index += 6
                                dir = reg[index:index+6]
                                index += 6
                                if (index and name):
                                    if (name in self.tabse[entry]['sym'].keys()):
                                        errorFlag = True
                                        break
                                    else:
                                        self.tabse[entry]['sym'][name] = {}
                                        dire = calc.SIC_HEX(
                                            dirsc + calc.getIntBy_SicXe_HexOrInt(dir, True))
                                        self.tabse[entry]['sym'][name]['dir'] = dire
                                else:
                                    break
                            except:
                                break
                dirsc += dirsc + lonsc
        return not errorFlag

    def assemblePassTwo(self):
        dirsc = self.dirprog
        direj = self.dirprog
        errorFlag = False
        for entry in self.passTwoReturn['registers']:
            if (errorFlag):
                break
            sectionRegSplited = self.passTwoReturn['registers'][entry]['registers'].split(
                '\n')
            for reg in sectionRegSplited:
                if (reg[0] == 'E'):
                    break
                if (reg[0] == 'T'):
                    dir = reg[1:7]
                    content = reg[10:]
                    rowCounter = mem.writeAllocation(content, dir, dirsc)
                    self.updateAllocationView(dir, rowCounter, dirsc)
                if (reg[0] == 'M'):
                    dir = reg[1:7]
                    numBytes = reg[7:9]
                    numBytes = calc.getIntBy_SicXe_HexOrInt(numBytes)
                    dirFromTabse = self.getDirFromTabse()
                    if (dirFromTabse != False):
                        dir = reg[1:7]
                        dirsc
                        mem.readAllocation(dir, dirsc,)
                    else:
                        errorFlag = True
                        break

        return not errorFlag

    def updateAllocationView(self, allocation, rowCounter, dirsc):
        i = 0
        allocation = calc.getIntBy_SicXe_HexOrInt(allocation, True)
        while (i < rowCounter):
            index = int(calc.getIntBy_SicXe_HexOrInt(allocation, True)/16)
            memRow = mem.getAllocationRow(allocation, dirsc)
            self.__thisMemoryTabTree.insert('', index, values=(
                calc.SIC_HEX(allocation), memRow[0], memRow[1], memRow[2], memRow[3], memRow[4], memRow[5], memRow[6], memRow[7], memRow[8], memRow[9], memRow[10], memRow[11], memRow[12], memRow[13], memRow[14], memRow[15]))
            allocation += 16
            i += 1

    def cleanMemory(self):
        mem.cleanMemory()
        for allocation in mem.memory:
            allocationRow = mem.memory[allocation]
            self.__thisMemoryTabTree.insert('', END, values=(
                allocation,  allocationRow[0], allocationRow[1], allocationRow[2], allocationRow[3], allocationRow[4], allocationRow[5], allocationRow[6], allocationRow[7], allocationRow[8], allocationRow[9], allocationRow[10], allocationRow[11], allocationRow[12], allocationRow[13], allocationRow[14], allocationRow[15]))
        self.__thisMemoryTabTree.insert('', END, values=(
            'empty',  ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',))

    def getDirFromTabse(self, label):
        tabseKeys = self.tabse.keys()
        if (label in tabseKeys):
            return self.tabse[label]['dir']
        else:
            for tabseKey in tabseKeys:
                if label in self.tabse[tabseKey]['sym'].keys():
                    return self.tabse[tabseKey]['sym'][label]['dir']
        return False

    def deleteStringAfterChar(self, ch, strValue):
        # The Regex pattern to match al characters on and after '-'
        pattern = ch + ".*"
        # Remove all characters after the character '-' from string
        return re.sub(pattern, '', strValue)

    def run(self):
        # Run main application
        self.__root.mainloop()


# Run main application
assemblyGUI = Sicxe_GUI(width=600, height=400)
assemblyGUI.run()
