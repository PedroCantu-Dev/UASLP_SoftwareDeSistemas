from pathlib import Path
import os
from tkinter import *
from tkinter import messagebox
from tkinter.messagebox import *
from tkinter.filedialog import *
from tkinter.ttk import Treeview
import webbrowser
from SICXE import *


class Sicxe_GUI:

    def __thisSourceFileKeyPressed(event):
        __savedFileFlag = False

    __root = Tk()

    __savedFileFlag = True

    __sourceFileLabel = LabelFrame(__root, text="Source File")
    __thisSourceFile = Text(__sourceFileLabel, undo=True, wrap=NONE)
    __thisSourceFileScrollBar = Scrollbar(__thisSourceFile)
    __thisSourceFileScrollBarX = Scrollbar(
        __thisSourceFile, orient='horizontal')

    __file = None
    __thisSourceFile.bind('<KeyRelease>', __thisSourceFileKeyPressed)

    __InterFileLabel = LabelFrame(__root, text="Intermediate File")
    __TabSymLabel = LabelFrame(__root, text="Symbol Table")
    __ErrorsLabel = LabelFrame(__root, text="Errors File")
    __registerFileLabel = LabelFrame(__root, text="Registers")

    # El campo de los registros:
    __thisRegisterFile = Text(__registerFileLabel, wrap=NONE, state=DISABLED)
    __thisRegisterFileScrollBar = Scrollbar(__thisRegisterFile)
    __thisRegisterFileScrollBarX = Scrollbar(
        __thisRegisterFile, orient='horizontal')

    # Archivo intermedio:
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

    # Tabla de simbolos
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

    # for error lines
    # index ,sentence , type, description
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

    # forRegisters
    # columnsRegisters = ('#1', '#2', '#3', '#4', '#5')
    # __thisRegistersTree = Treeview(
    #     __RegistersLabel, columns=columnsRegisters, show='headings')

    # define headings
    # __thisRegistersTree.heading('#1', text='Type')
    # __thisRegistersTree.heading('#2', text='Name')
    # __thisRegistersTree.heading('#3', text='Direction')
    # __thisRegistersTree.heading('#4', text='Size')
    # __thisRegistersTree.heading('#5', text='Content')

    # __thisRegistersScrollBarY = Scrollbar(__thisRegistersTree)
    # __thisRegistersScrollBarX = Scrollbar(
    #     __thisRegistersTree, orient='horizontal')

    # for menu bar at the top of the window
    __thisMenuBar = Menu(__root)
    __thisFileMenu = Menu(__thisMenuBar, tearoff=0)
    __thisAssemblerMenu = Menu(__thisMenuBar, tearoff=0)
    __thisSimulationMenu = Menu(__thisMenuBar, tearoff=0)
    __thisHelpMenu = Menu(__thisMenuBar, tearoff=0)

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

        # Add controls (widget)
        self.__sourceFileLabel.place(relx=0, rely=0, relheight=1, relwidth=1/3)
        self.__InterFileLabel.place(
            relx=1/3, rely=0, relheight=1, relwidth=1/3)
        self.__TabSymLabel.place(relx=2/3, rely=0, relheight=1/3, relwidth=1/3)
        self.__ErrorsLabel.place(
            relx=2/3, rely=1/3, relheight=1/3, relwidth=1/3)
        self.__registerFileLabel.place(
            relx=2/3, rely=2/3, relheight=1/3, relwidth=1/3)

        self.__thisSourceFile.place(relx=0, rely=0, relheight=1, relwidth=1)
        self.__thisIntermediateFileTree.place(
            relx=0, rely=0, relheight=1, relwidth=1)
        self.__thisTabSymFileTree.place(
            relx=0, rely=0, relheight=1, relwidth=1)
        self.__thisErrorTableFileTree.place(
            relx=0, rely=0, relheight=1, relwidth=1)
        self.__thisRegisterFile.place(relx=0, rely=0, relheight=1, relwidth=1)

        # scroll para los registros:
        self.__thisRegisterFileScrollBar.pack(side=RIGHT, fill=Y)
        self.__thisRegisterFileScrollBar.config(
            command=self.__thisRegisterFile.yview)
        self.__thisRegisterFile.config(
            yscrollcommand=self.__thisRegisterFileScrollBar.set)

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

        ####
        # self.__thisRegistersScrollBarX.pack(side=BOTTOM, fill='x')
        # self.__thisRegistersScrollBarX.config(
        #     command=self.__thisRegistersTree.xview)
        # self.__thisRegistersTree.config(
        #     xscrollcommand=self.__thisRegistersScrollBarX.set)
        # self.__thisRegistersScrollBarY.pack(side=RIGHT, fill=Y)
        # self.__thisRegistersScrollBarY.config(
        #     command=self.__thisRegistersTree.yview)
        # self.__thisRegistersTree.config(
        #     yscrollcommand=self.__thisRegistersScrollBarY.set)

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

    def refresh(self):
        self.destroy()
        self.__init__()

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
        passTwoReturn = passTwo(self.intermediateFile, self.sections)

        # Intermediate File, plot and save
        interFile = open(self.assembledFolderPrefix +
                         self.intermediateFileName+'_pass2'+'.arc', "w+")

        index = 0
        for key in self.intermediateFile:
            codObjeto = ""
            interFile.writelines(str(key))
            interFile.writelines(" ")
            line = self.intermediateFile.get(key)
            for content in line:
                interFile.writelines(content)
                interFile.writelines(" ")
            if (key in passTwoReturn):
                codObjeto = passTwoReturn.get(key)
                interFile.writelines(codObjeto)
            self.__thisIntermediateFileTree.insert('', END, values=(
                key, line[0], line[1], line[2], line[3], line[4]))
            interFile.writelines("\n")
        index += 1
        interFile.close()
# self.__thisTextArea.event_generate("<<Cut>>")
        # self.__thisTextArea.event_generate("<<Paste>>")

    def __assemble(self):
        self.__pass2()
        self.makeRegisters()

    def deleteStringAfterChar(self, ch, strValue):
        # The Regex pattern to match al characters on and after '-'
        pattern = ch + ".*"
        # Remove all characters after the character '-' from string
        return re.sub(pattern, '', strValue)

    # funcion para generar los archivos de texto

    def makeRegisters(self):
        registros = open(self.assembledFolderPrefix +
                         self.intermediateFileName+'.obj', "w+")
        nombre = self.intermediateFileName
        primeraInstruccion = ""

        # registro H
        objFileLines = "H" + fillOrCutL(nombre) + fillOrCutR(self.makeHexString(
            self.initial)) + fillOrCutR(self.makeHexString(self.size))

        objFileLines += "\n"
        registrosM = []

        primeraDireccionRegistroAux = ""
        registroTAux = ""

        lastCodObj = ""
        lastDireccion = ""
        # registro T
        for item in self.intermediateFile:
            line = self.intermediateFile[item][4]
            instru = self.intermediateFile[item][2]
            fullLine = self.intermediateFile[item]

            if (len(registroTAux) >= 60):
                # cortan el archivo de texto
                if (len(registroTAux) > 60):
                    primeraDireccionRegistroAux = lastDireccion
                    if (len(registroTAux) % 2 == 0):
                        objFileLines += "T " + cleanHexForCodObj(primeraDireccionRegistroAux, 6) + " "+cleanHexForCodObj(
                            hex(int(len(registroTAux)/2)), 2) + " " + registroTAux[:-len(lastCodObj)]
                        registroTAux = registroTAux[-len(lastCodObj):]
                    else:
                        objFileLines += "T " + cleanHexForCodObj(primeraDireccionRegistroAux, 6) + " "+cleanHexForCodObj(hex(int((len(registroTAux)+1)/2)), 2) + \
                            " " + registroTAux[:-len(lastCodObj)]
                        registroTAux = registroTAux[-len(lastCodObj):]
                    lastDireccion = ""
                else:
                    objFileLines += "T " + cleanHexForCodObj(primeraDireccionRegistroAux, 6) + fillOrCutR(hex(len(registroTAux)), 2) + \
                        " " + registroTAux

                registroTAux = ""
                primeraDireccionRegistroAux = ""
                lastCodObj = ""
                objFileLines += "\n"  # cortando el archivo de texto
            elif (instru == 'RESW' or instru == 'RESB' or instru == 'ORG' or instru == 'USE'):
                # cortan el archivo de texto
                if (registroTAux):
                    objFileLines += "T " + cleanHexForCodObj(primeraDireccionRegistroAux, 6) + " "+cleanHexForCodObj(hex(int(len(registroTAux)/2)), 2) + \
                        " " + registroTAux
                registroTAux = ""
                lastCodObj = ""
                primeraDireccionRegistroAux = ""
                objFileLines += "\n"  # cortando el archivo de texto
            elif (instru == 'END'):
                if (registroTAux):
                    objFileLines += "T " + cleanHexForCodObj(primeraDireccionRegistroAux, 6) + " "+cleanHexForCodObj(hex(int(len(registroTAux)/2)), 2) + \
                        " " + registroTAux
                if (fullLine[3]):  # buscará en la tabla de simbolos
                    primeraInstruccion = "YEah"
            elif (line == "----"):
                continue

            else:
                lastDireccion = fullLine[0]
                # objFileLines += "T"
                # si aun no se sabe la primera instruccion se guarda en la variable
                if (not primeraInstruccion):
                    # si en efecto se trata de una instruccion se asigna el valor
                    if (SICXE_Dictionary[baseMnemonic(instru)][0] == 'I'):
                        primeraInstruccion = fillOrCutR(fullLine[0])
                if (not primeraDireccionRegistroAux):
                    primeraDireccionRegistroAux = fullLine[0]
                if ('*' in line):
                    lastCodObj = self.deleteStringAfterChar(
                        ':', str(line).replace('*', ''))
                    # se genera un registro m
                    if (instru == 'WORD'):  # si el relocalizable es por un WORD
                        pass
                    elif (baseMnemonic(instru) in SICXE_Dictionary.keys()):
                        # la relocalizacion se hará un byte despues
                        registroM = "\nM"
                        registroM += fillOrCutR(
                            cleanHexForCodObj(hex(int(fullLine[0], 16)+1)))
                        registroM += "05"
                        if (True):  # aqui  cambiará segun se avance en la arquitectura
                            registroM += "+"
                        else:
                            pass  # los casos para saber cuando es con signo -
                        registroM += nombre+"\n"
                        registrosM.append(registroM)
                    elif (True):
                        # los casos que faltan por ver como relocalizables.
                        pass
                else:
                    lastCodObj = self.deleteStringAfterChar(':', str(line))
                registroTAux += lastCodObj
        for itemss in registrosM:
            objFileLines += itemss
        # registro E
        objFileLines += "E"
        objFileLines += cleanHexForCodObj(primeraInstruccion)

        self.__thisRegisterFile.config(state=NORMAL)
        self.__thisRegisterFile.insert(1.0, objFileLines)
        self.__thisRegisterFile.config(state=DISABLED)
        registros.writelines(objFileLines)
        registros.close()

    def run(self):
        # Run main application
        self.__root.mainloop()


# Run main application
assemblyGUI = Sicxe_GUI(width=600, height=400)
assemblyGUI.run()
