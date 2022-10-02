from pathlib import Path
import tkinter
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
    __RegistersLabel = LabelFrame(__root, text="Registers")

    # for intermediate file
    columnsInter = ('#1', '#2', '#3', '#4', '#5', '#6')
    __thisIntermediateFileTree = Treeview(
        __InterFileLabel, columns=columnsInter, show='headings')
    # define headings

    __thisIntermediateFileTree.column('#1', anchor=CENTER, width=70)
    __thisIntermediateFileTree.heading('#1', text='Line Index')
    __thisIntermediateFileTree.column('#2', anchor=CENTER, width=60)
    __thisIntermediateFileTree.heading('#2', text='PC')
    __thisIntermediateFileTree.column('#3', anchor=CENTER, width=100)
    # __thisIntermediateFileTree.tag_config(background="black",
    #   foreground="red")
    __thisIntermediateFileTree.heading('#3', text='Label')
    __thisIntermediateFileTree.column('#4', anchor=CENTER, width=100)
    __thisIntermediateFileTree.heading('#4', text='Mnemonic')
    __thisIntermediateFileTree.column('#5', anchor=CENTER, width=360)
    __thisIntermediateFileTree.heading('#5', text='Operand')
    __thisIntermediateFileTree.column('#6', anchor=CENTER, width=360)
    __thisIntermediateFileTree.heading('#6', text='Obj Code')

    __thisIntermediateFileScrollBarY = Scrollbar(__thisIntermediateFileTree)
    __thisIntermediateFileScrollBarX = Scrollbar(
        __thisIntermediateFileTree, orient='horizontal')

    # for symbol table
    columnsTabSym = ('#1', '#2')
    __thisTabSymFileTree = Treeview(
        __TabSymLabel, columns=columnsTabSym, show='headings')
    # define headings
    # __thisTabSymFileTree.column('#1', anchor=CENTER, width=80)
    # __thisTabSymFileTree.heading('#1', text='Sym-Index')
    __thisTabSymFileTree.column('#1', anchor=CENTER, width=50)
    __thisTabSymFileTree.heading('#1', text='Symbol')
    __thisTabSymFileTree.column('#2', anchor=CENTER, width=50)
    __thisTabSymFileTree.heading('#2', text='Address')

    __thisTabSymFileScrollBarY = Scrollbar(__thisTabSymFileTree)
    __thisTabSymFileScrollBarX = Scrollbar(
        __thisTabSymFileTree, orient='horizontal')

    # for error lines
    # index ,sentence , type, description
    columnsErrorTable = ('#1', '#2', '#3', '#4')
    __thisErrorTableFileTree = Treeview(
        __ErrorsLabel, columns=columnsErrorTable, show='headings')
    # define headings
    __thisErrorTableFileTree.column('#1', anchor=CENTER, width=80)
    __thisErrorTableFileTree.heading('#1', text='Line index')
    __thisErrorTableFileTree.column('#2', anchor=CENTER, width=200)
    __thisErrorTableFileTree.heading('#2', text='sentence')
    __thisErrorTableFileTree.column('#3', anchor=CENTER, width=200)
    __thisErrorTableFileTree.heading('#3', text='type')
    __thisErrorTableFileTree.column('#4', anchor=CENTER, width=450)
    __thisErrorTableFileTree.heading('#4', text='description')

    __thisErrorTableFileScrollBarY = Scrollbar(__thisErrorTableFileTree)
    __thisErrorTableFileScrollBarX = Scrollbar(
        __thisErrorTableFileTree, orient='horizontal')

    # forRegisters
    columnsRegisters = ('#1', '#2', '#3', '#4', '#5')
    __thisRegistersTree = Treeview(
        __RegistersLabel, columns=columnsRegisters, show='headings')
    # define headings
    __thisRegistersTree.heading('#1', text='Type')
    __thisRegistersTree.heading('#2', text='Name')
    __thisRegistersTree.heading('#3', text='Direction')
    __thisRegistersTree.heading('#4', text='Size')
    __thisRegistersTree.heading('#5', text='Content')

    __thisRegistersScrollBarY = Scrollbar(__thisRegistersTree)
    __thisRegistersScrollBarX = Scrollbar(
        __thisRegistersTree, orient='horizontal')

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
        self.__RegistersLabel.place(
            relx=2/3, rely=2/3, relheight=1/3, relwidth=1/3)

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

        self.__thisRegistersScrollBarX.pack(side=BOTTOM, fill='x')
        self.__thisRegistersScrollBarX.config(
            command=self.__thisRegistersTree.xview)
        self.__thisRegistersTree.config(
            xscrollcommand=self.__thisRegistersScrollBarX.set)
        self.__thisRegistersScrollBarY.pack(side=RIGHT, fill=Y)
        self.__thisRegistersScrollBarY.config(
            command=self.__thisRegistersTree.yview)
        self.__thisRegistersTree.config(
            yscrollcommand=self.__thisRegistersScrollBarY.set)

        self.__thisSourceFile.place(relx=0, rely=0, relheight=1, relwidth=1)
        self.__thisIntermediateFileTree.place(
            relx=0, rely=0, relheight=1, relwidth=1)
        self.__thisTabSymFileTree.place(
            relx=0, rely=0, relheight=1, relwidth=1)
        self.__thisErrorTableFileTree.place(
            relx=0, rely=0, relheight=1, relwidth=1)
        self.__thisRegistersTree.place(relx=0, rely=0, relheight=1, relwidth=1)

        # Scrollbar will adjust automatically according to the content
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
            if(save == True):
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

    def __assemble(self):
        # self.__thisTextArea.event_generate("<<Cut>>")
        # self.__thisTextArea.event_generate("<<Paste>>")

        pass1Array = []
        pass2Array = []

    intermediateFile = None
    tabSym = None

    def cleanWhenPass2(self):
        {}

    def cleanWhenPass1(self):
        self.intermediateFile = None
        for i in self.__thisIntermediateFileTree.get_children():
            self.__thisIntermediateFileTree.delete(i)
        for i in self.__thisTabSymFileTree.get_children():
            self.__thisTabSymFileTree.delete(i)
        for i in self.__thisErrorTableFileTree.get_children():
            self.__thisErrorTableFileTree.delete(i)
        self.tableSym = None
        # self.refresh()

    def refresh(self):
        self.destroy()
        self.__init__()

    def __pass1(self):
        # llama al metodo para generar una lista de lineas apartir del archivo|
        # call readLines method for generating
        self.cleanWhenPass1()
        lines = self.__thisSourceFile.get("1.0", "end")
        if(lines and lines != '\n'):
            # lines = open(file).readlines()
            # llama al paso 1 |
            # call step one
            lines = lines.split("\n")
            passOneReturn = passOne(lines)
            self.intermediateFile = passOneReturn[0]
            self.tableSym = passOneReturn[1]
            size = passOneReturn[2]
            errors = passOneReturn[3]
            # print("file name(just name) :  " + Path(__file__).name)
            # print("Directory name :  " + os.path.dirname(__file__))

            intermediateFileName = list(self.intermediateFile.values())[0][1]
            assembledFolderPrefix = os.path.dirname(
                __file__)+"/assembled/" + intermediateFileName + "/"

            # for assembled folder creation
            if not os.path.exists(assembledFolderPrefix):
                os.makedirs(assembledFolderPrefix)

            # Intermediate File, plot and save
            interFile = open(assembledFolderPrefix +
                             intermediateFileName+'.arc', "w+")
            index = 0
            for key in self.intermediateFile:
                interFile.writelines(str(key))
                interFile.writelines(" ")
                line = self.intermediateFile.get(key)
                for any in line:
                    interFile.writelines(any)
                    interFile.writelines(" ")
                self.__thisIntermediateFileTree.insert(
                    '', END, values=(index, line[0], line[1], line[2], line[3], line[4]))
                interFile.writelines("\n")
                index += 1
            interFile.close()

            # symbol table
            tabSymFile = open(assembledFolderPrefix +
                              intermediateFileName+'.tab', "w+")
            for key in self.tableSym:
                tabSymFile.writelines(key)
                tabSymFile.writelines(" ")
                line = self.tableSym.get(key)
                tabSymFile.writelines(line)
                tabSymFile.writelines("\n")
                self.__thisTabSymFileTree.insert('', END, values=(key, line))
            tabSymFile.writelines("Tam del programa:" + str(size))
            tabSymFile.close()

            # error table
            errorFile = open(assembledFolderPrefix +
                             intermediateFileName+'.err', "w+")
            for key in errors:
                errorFile.writelines(str(key))
                errorFile.writelines(" ")
                line = errors.get(key)

                for lin in line:
                    errorFile.writelines(str(lin))
                    errorFile.writelines(" ")
                errorFile.writelines("\n")
                msgError = line[5].split(',')
                self.__thisErrorTableFileTree.insert(
                    '', END, values=(str(key) + ' | ('+line[1]+')', msgError[0] + '-->   ' + line[2] + ' ' + line[3] + ' ' + line[4], msgError[1], msgError[2]))
            errorFile.close()

    def __pass2(self):
        if(self.intermediateFile and self.tableSym):
            passTwoReturn = passTwo(self.intermediateFile, self.tableSym)
            lines = self.__thisSourceFile.get("1.0", "end")
            if(lines):
                # lines = open(file).readlines()
                # llama al paso 1 |
                # call step one
                lines = lines.split("\n")
                passOneReturn = passOne(lines)
                intermediateFile = passOneReturn[0]
                tableSym = passOneReturn[1]
                size = passOneReturn[2]
                errors = passOneReturn[3]

    def run(self):
        # Run main application
        self.__root.mainloop()


# Run main application
assemblyGUI = Sicxe_GUI(width=600, height=400)
assemblyGUI.run()
