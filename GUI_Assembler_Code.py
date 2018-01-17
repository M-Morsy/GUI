'''
  * assembler project
  * Author: Mohamed Morsy
  * Recognition: Bucky <3 / unknown github repo / myself <3
'''
import tkinter
import os
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
import subprocess
# global variable
Branch_Flag = 0
Current_Label = ""
instructionNumber = 0
noInstr = 0
fileReadList = []
# files variables

AssemblyFile = open("AssemblyFile.txt", 'w')
BinaryFile= open("BinaryFile.txt", 'w')
OutputFile = open("OutputFile.txt", 'w')

def get_L_value():
    global instructionNumber, noInstr, Branch_Flag, fileReadList
    Branch_offset_Number = 0
    detector = 0
    for i in range (instructionNumber +1 , noInstr):
        if (fileReadList[i].find("L:") != -1 or fileReadList[i].find("L :") != -1 or fileReadList[i].find(":") != -1 ): # FATHY >> MUST WRITE IT LIKE THIS L: or L :
            detector = i
            Branch_offset_Number = detector
            Branch_Flag = 0
            break
    return Branch_offset_Number

# register dictionary
registers = {
    "$zero": 0,
    "$at": 1,
    "$v0": 2,
    "$v1": 3,
    "$a0": 4,
    "$a1": 5,
    "$a2": 6,
    "$a3": 7,
    "$t0": 8,
    "$t1": 9,
    "$t2": 10,
    "$t3": 11,
    "$t4": 12,
    "$t5": 13,
    "$t6": 14,
    "$t7": 15,
    "$s0": 16,
    "$s1": 17,
    "$s2": 18,
    "$s3": 19,
    "$s4": 20,
    "$s5": 21,
    "$s6": 22,
    "$s7": 23,
    "$t8": 24,
    "$t9": 25,
    "$k0": 26,
    "$k1": 27,
    "$gp": 28,
    "$sp": 29,
    "$fp": 30,
    "$ra": 31
}

# converts the instruction part of a line of MIPS code
def instr_decode(instr):
    global Branch_Flag
    if instr == "add":
        func_type = "r"
        opcode = 0
        funct = 0x20
        Branch_Flag = 0

    elif instr == "addi":
        func_type = "i"
        opcode = 0x8
        funct = None
        Branch_Flag = 0
    elif instr == "addiu":
        func_type = "i"
        opcode = 0x9
        funct = None
        Branch_Flag = 0
    elif instr == "addu":
        func_type = "r"
        opcode = 0
        funct = 0x21
        Branch_Flag = 0
    elif instr == "and":
        func_type = "r"
        opcode = 0
        funct = 0x24
        Branch_Flag = 0
    elif instr == "andi":
        func_type = "i"
        opcode = 0xc
        funct = None
        Branch_Flag = 0
    elif instr == "beq":
        func_type = "i"
        opcode = 0x4
        funct = None
        Branch_Flag = 1
    elif instr == "bne":
        func_type = "i"
        opcode = 0x5
        funct = None
        Branch_Flag = 1
    elif instr == "j":
        func_type = "j"
        opcode = 0x2
        funct = None
        Branch_Flag = 0
    elif instr == "jal":
        func_type = "j"
        opcode = 0x3
        funct = None
        Branch_Flag = 0
    elif instr == "jr":
        func_type = "r"
        opcode = 0
        funct = 0x8
        Branch_Flag = 0
    elif instr == "lbu":
        func_type = "i"
        opcode = 0x24
        funct = None
        Branch_Flag = 0
    elif instr == "lhu":
        func_type = "i"
        opcode = 0x25
        funct = None
        Branch_Flag = 0
    elif instr == "ll":
        func_type = "i"
        opcode = 0x30
        funct = None
        Branch_Flag = 0
    elif instr == "lui":
        func_type = "i"
        opcode = 0xf
        funct = None
        Branch_Flag = 0
    elif instr == "lw":
        func_type = "i"
        opcode = 0x23
        funct = None
        Branch_Flag = 0
    elif instr == "nor":
        func_type = "r"
        opcode = 0
        funct = 0x27
        Branch_Flag = 0
    elif instr == "or":
        func_type = "r"
        opcode = 0
        funct = 0x25
        Branch_Flag = 0
    elif instr == "ori":
        func_type = "i"
        opcode = 0xd
        funct = None
        Branch_Flag = 0
    elif instr == "slt":
        func_type = "r"
        opcode = 0
        funct = 0x2a
        Branch_Flag = 0
    elif instr == "slti":
        func_type = "i"
        opcode = 0xa
        funct = None
        Branch_Flag = 0
    elif instr == "sltiu":
        func_type = "i"
        opcode = 0xb
        funct = None
        Branch_Flag = 0
    elif instr == "sltu":
        func_type = "r"
        opcode = 0
        funct = 0x2b
        Branch_Flag = 0
    elif instr == "sll":
        func_type = "r"
        opcode = 0
        funct = 0x00
        Branch_Flag = 0
    elif instr == "srl":
        func_type = "r"
        opcode = 0
        funct = 0x02
        Branch_Flag = 0
    elif instr == "sb":
        func_type = "i"
        opcode = 0x28
        funct = None
        Branch_Flag = 0
    elif instr == "sc":
        func_type = "i"
        opcode = 0x38
        funct = None
        Branch_Flag = 0
    elif instr == "sh":
        func_type = "i"
        opcode = 0x29
        funct = None
        Branch_Flag = 0
    elif instr == "sw":
        func_type = "i"
        opcode = 0x2b
        funct = None
        Branch_Flag = 0
    elif instr == "sub":
        func_type = "r"
        opcode = 0
        funct = 0x22
        Branch_Flag = 0
    elif instr == "subu":
        func_type = "r"
        opcode = 0
        funct = 0x23
        Branch_Flag = 0
    else:
        func_type = None
        opcode = None
        funct = None
        Branch_Flag = 0
    return [func_type, opcode, funct]
#
def reg_decode(func_type, instr, regs):
    # execution for r-type functions
    #print(regs, "\n")
    if func_type == "r":

        # special case for MIPS shifts
        if (instr == "sll"):
            try:
                # return[rs,        rt,               rd,             shamt]
                return [0, registers[regs[1]], registers[regs[0]], int(regs[2])]
            except:
                #print("BUSTED2")
                return None

                # special case for MIPS jr
        try:
            # return[      rs,                 rt,               rd,          shamt]
            #print(regs[0])
            return [registers[regs[1]], registers[regs[2]], registers[regs[0]], 0]

        except:
            #print("BUSTED1")
            return None


    # execution for i-type functions
    elif func_type == "i":

        # special case for lw,sw
        if (instr == "lw") or (instr == "sw"):
            try:
                if len(regs[1]) > 1 and regs[1][1] == "x":
                    imm = int(regs[1], base=16)
                else:
                    imm = int(regs[1])

                # return[       rs,                rt        ,  immediate  ]
                return [registers[regs[2]], registers[regs[0]], imm]
            except:
                return None

        # standard i-type MIPS instructions
        ''' This supports only the beq in our case but we need to enter the immediate value directly, not C or L ... etc. '''
        try:
            if len(regs[2]) > 1 and regs[2][1] == "x":
                imm = int(regs[2], base=16)
            elif (regs[2] == 'L'):
                imm = int(get_L_value())
            else:
                imm = int(regs[2])
            #print ("imm try =", imm)
            # return[        rs                 rt              immediate ]
            return  [registers[regs[1]], registers[regs[0]],     imm]
        except:
            #print (get_L_value())
            #print ("REGS =",regs[0],regs[1], regs[2])
            #print ("BUSTED !!")
            return None


    else:
        return None

# convert one instruction into binary & write in file
def convertANDwrite(code):
    global instructionNumber
    code = code.replace("(", " ")
    code = code.replace(")", "")
    code = code.replace(",", " ")
    code = code.replace("  ", " ")
    code = code.replace("L:","")
    code = code.replace("L :", "")
    #print (code)
    args = code.split(" ")
    instruction = args[0]

    codes = instr_decode(instruction)
    func_type = codes[0]
    if (args[0] == ""): #to handle beq effect after removing L:
        reg_values = reg_decode(func_type, instruction, args[2:])  # get the numeric values of the registers
        #print ("args = ",args)
    else:
        reg_values = reg_decode(func_type, instruction, args[1:])  # get the numeric values of the registers
    #print ("reg values are:", reg_values)
    # the following if statement below prints an error if needed
    if reg_values == None:
        #print ("BUSTED!!")
        print("Not a valid MIPS statement")
        return

    # execution for r-type functions
    if func_type == "r":
        opcode = '{0:06b}'.format(codes[1])
        rs = '{0:05b}'.format(reg_values[0])
        rt = '{0:05b}'.format(reg_values[1])
        rd = '{0:05b}'.format(reg_values[2])
        shamt = '{0:05b}'.format(reg_values[3])
        funct = '{0:06b}'.format(codes[2])                                                                              # codes is the return of instr_decode [func_type, opcode, funct]

        #BinaryFile = open('BinaryFile.txt', 'w')
        BinaryFile = open('BinaryFile.txt', 'a')                                                                                        # needs to be 'a' to append
        #file.write(opcode +"|" + rs +"|" + rt +"|" + rd +"|"+ shamt +"|" + funct)
        BinaryFile.write(opcode +rs + rt + rd + shamt + funct)
        BinaryFile.write(" //          ")
        BinaryFile.write(str(instructionNumber))
        BinaryFile.write(" ")
        BinaryFile.write(opcode +"|"+ rs+"|"+ rt+"|"+ rd + "|" + shamt + "|" + funct)
        BinaryFile.write("\n")

    # execution for i-type functions
    elif func_type == "i":
        opcode = '{0:06b}'.format(codes[1])
        rs = '{0:05b}'.format(reg_values[0])
        rt = '{0:05b}'.format(reg_values[1])
        imm = '{0:016b}'.format(reg_values[2])
        #BinaryFile = open('BinaryFile.txt', 'w')
        BinaryFile = open('BinaryFile.txt', 'a')                                                                                        # needs to be 'a' to append
        #file.write(opcode+"|"+rs+"|"+rt+"|"+imm)
        BinaryFile.write(opcode +"|"+ rs+"|" + rt+"|" + imm)
        BinaryFile.write(" //          ")
        BinaryFile.write(str(instructionNumber))
        BinaryFile.write(" ")
        BinaryFile.write(opcode + rs + rt + imm)
        BinaryFile.write("\n")
    else:
        print("Not a valid MIPS statement")
        return

    return


def AssemblerFunction ():
    global instructionNumber, noInstr, fileReadList
    AssemblyFile = open('AssemblyFile.txt', 'r')  # file written
    text = AssemblyFile.read()
    #print(text)
    AssemblyFile.close()
    fileReadList = text.split("\n")  # list with one instruction per element
    noInstr = len(fileReadList)  # number of instructions entered in the file
    BinaryFile = open('BinaryFile.txt', 'w')  # must be 'w' to override in the file, not to append

    for i in range(noInstr):
        instructionNumber = i
        convertANDwrite(fileReadList[i])  # send one instruction & write it in the file

    BinaryFile.close()


class Printing:
    root2 = Tk()
    OutputWidthPrim = 700
    OutputHeightPrim = 700
    root2.title("Output Printed")
    screenWidth = root2.winfo_screenwidth()
    screenHeight = root2.winfo_screenheight()
    Outputleft = (screenWidth / 2) + (OutputWidthPrim / 3)  # starting point on left
    Outputtop = (screenHeight / 2) - (OutputHeightPrim / 3)
    tempText = Label (root2, text="No Output yet :D \n"
                                  "Please press Run Code from Run Menu :D ")

    tempText.pack()
    root2.geometry('%dx%d+%d+%d' % (OutputWidthPrim, OutputHeightPrim, Outputleft, Outputtop))
    # variables




    def __init__(self, **kwargs):
        self.tempText.destroy()

        try:
            self.OutputWidth = kwargs['width']
        except KeyError:
            pass

        try:
            self.OutputHeight = kwargs['height']
        except KeyError:
            pass
        # Title
        self.root2.title("Output Printed")
        # position
        OutputWidth = 600
        OutputHeight = 600
        self.root2.title("Output Printed")
        screenWidth = self.root2.winfo_screenwidth()
        screenHeight = self.root2.winfo_screenheight()
        Outputleft = (screenWidth / 2) + (OutputWidth / 3)  # starting point on left
        Outputtop = (screenHeight / 2) - (OutputHeight / 3)

        self.root2.geometry('%dx%d+%d+%d' % (OutputWidth, OutputHeight, Outputleft, Outputtop))

        # to print assembly file
        OutputFrameThree = LabelFrame(self.root2, text="   Assembly File ", padx=10, pady=10)
        AssemblyFileName = 'AssemblyFile.txt'
        AssemblyFile = open(AssemblyFileName, 'r')
        text = AssemblyFile.read()
        AssemblyFile.close()
        AssemblyFilePrint = Label(OutputFrameThree, text=text)

        # to print binary file
        OutputFrameOne = LabelFrame(self.root2, text="   Binary File ", padx=10, pady=10)
        BinaryFileName = 'BinaryFile.txt'
        BinaryFile = open(BinaryFileName, 'r')
        text = BinaryFile.read()
        BinaryFile.close()
        BinaryFilePrint = Label(OutputFrameOne, text=text)

        # to print output file
        OutputFrameTwo = LabelFrame(self.root2, text="   Output File ", padx=10, pady=10)
        OutputFileName = 'OutputFile.txt'
        OutputFile = open(OutputFileName, 'r')
        text = OutputFile.read()
        OutputFile.close()
        OutputFilePrint = Label(OutputFrameTwo, text=text)


        # layout
        OutputFrameOne.grid(row=0, column=2)
        OutputFrameTwo.grid(row=1, column=1, columnspan=2)
        OutputFrameThree.grid(row=0, column=0)
        BinaryFilePrint.grid()
        OutputFilePrint.grid()
        AssemblyFilePrint.grid()


    def Outputrun(self):
        self.root2.mainloop()

class Notepad:

    root = Tk()

    # default window width and height
    thisWidth = 300
    thisHeight = 300
    thisTextArea = Text(root)
    thisMenuBar = Menu(root)
    thisFileMenu = Menu(thisMenuBar, tearoff=0)
    thisEditMenu = Menu(thisMenuBar, tearoff=0)
    thisHelpMenu = Menu(thisMenuBar, tearoff=0)
    thisRunMenu = Menu (thisMenuBar, tearoff=0)
    thisScrollBar = Scrollbar(thisTextArea)
    #thisRunButton = Button(root,text="Run Code" ,bg="Green",width=thisWidth)
    file = None
    #constructor function
    def __init__(self, **kwargs):
        # initialization

        # set window size (the default is 300x300)

        try:
            self.thisWidth = kwargs['width']
        except KeyError:
            pass

        try:
            self.thisHeight = kwargs['height']
        except KeyError:
            pass
        # try different window

        # set the GUI place on screen
        self.root.title("GUI_CO_Project")

        # Adjust window place
        screenWidth = self.root.winfo_screenwidth()
        screenHeight = self.root.winfo_screenheight()
        
        left = (screenWidth / 2) - (self.thisWidth / 2)                                                                 #starting point on left
        top = (screenHeight / 2) - (self.thisHeight / 2)                                                                #starting point on top

        self.root.geometry('%dx%d+%d+%d' % (self.thisWidth, self.thisHeight, left, top))                                #DONT REMEMBER WHY dx?

        # to make the text area auto resizable
        self.root.grid_rowconfigure(0, weight=1)                                                                        #CHECK PARAMETER
        self.root.grid_columnconfigure(0, weight=1)

        # add controls (widget)

        self.thisTextArea.grid(sticky=N + E + W + S)                                                                    # To show text area all over the place
        # File Menu
        self.thisFileMenu.add_command(label="New", command=self.newFile)
        self.thisFileMenu.add_command(label="Open", command=self.openFile)
        self.thisFileMenu.add_command(label="Save", command=self.saveFile)
        self.thisFileMenu.add_separator()
        self.thisFileMenu.add_command(label="Exit", command=self.quitApplication)
        self.thisMenuBar.add_cascade(label="File", menu=self.thisFileMenu)
        #Edit menu
        self.thisEditMenu.add_command(label="Cut", command=self.cut)
        self.thisEditMenu.add_command(label="Copy", command=self.copy)
        self.thisEditMenu.add_command(label="Paste", command=self.paste)
        self.thisMenuBar.add_cascade(label="Edit", menu=self.thisEditMenu)
        #Help menu
        self.thisHelpMenu.add_command(label="About Notepad", command=self.showAbout)
        self.thisMenuBar.add_cascade(label="Help", menu=self.thisHelpMenu)
        # Run bar
        self.thisRunMenu.add_command(label="Run Code", command=self.runCode)
        self.thisMenuBar.add_cascade(label="Run", menu=self.thisRunMenu)

        #Bar gathering all menus
        self.root.config(menu=self.thisMenuBar)
        #scroll bar
        self.thisScrollBar.pack(side=RIGHT, fill=Y)
        # to attach scroll bar to text area & vice versa
        self.thisScrollBar.config(command=self.thisTextArea.yview)                                                      #When you scroll, text area gets up & down with you
        self.thisTextArea.config(yscrollcommand=self.thisScrollBar.set)                                                 #When you write, the bar is scrolling with you @ need
        #Run button
        #self.thisRunButton.grid()

    def quitApplication(self):
        self.root.destroy()
        # exit()

    def showAbout(self):
        showinfo("""
  assembler project \n
  Author: Mohamed Morsy & Awesome Team \n
  Recognition: Bucky <3
""")

    def openFile(self):

        self.file = askopenfilename(defaultextension=".txt",
                                      filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])

        if self.file == "":
            # no file to open
            self.file = None
        else:
            # try to open the file
            # set the window title
            self.root.title(os.path.basename(self.file) + " - Notepad")                                                 # Get the file name
            self.thisTextArea.delete(1.0, END)                                                                          # to delete the contents of what you wrote in the text area

            file = open(self.file, "r")

            self.thisTextArea.insert(1.0, file.read())

            file.close()

    def newFile(self):
        self.root.title("Untitled - Notepad")
        self.file = None
        self.thisTextArea.delete(1.0, END)

    def saveFile(self, name="Untitled"):

        if self.file == None:
            # save as new file
            self.file = asksaveasfilename(initialfile=name, defaultextension=".txt",
                                            filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])

            if self.file == "":
                self.file = None
            else:
                # try to save the file
                file = open(self.file, "w")
                file.write(self.thisTextArea.get(1.0, END))
                file.close()
                # change the window title
                self.root.title(os.path.basename(self.file))


        else:
            file = open(self.file, "w")
            file.write(self.thisTextArea.get(1.0, END))
            file.close()
    #no real value for the next operations
    def cut(self):
        self.thisTextArea.event_generate("<<Cut>>")

    def copy(self):
        self.thisTextArea.event_generate("<<Copy>>")

    def paste(self):
        self.thisTextArea.event_generate("<<Paste>>")
    #to access the class from outside it
    def run(self):

        # run main application
        self.root.mainloop()

    def runCode(self):
        # Save code file
        self.saveFile(name="AssemblyFile.txt")
        # Run assembler code on file >> # create binary file
        AssemblerFunction()
        # compilation code
        #subprocess.call('start', shell=True)
        subprocess.call('iverilog hello.v', shell=True)                                                                 # compile verilog file
        subprocess.call('vvp a.out', shell=True)                                                                        # run verilog file

        # open results file in the program in new window >> with the old one exists
        OutputPrint = Printing(width=600,height=600)
        OutputPrint.Outputrun()


    #thisRunButton.bind("<Button -1>", dummy)                                                                           # Button code didn't work for some reason


# run main application

notepad = Notepad(width=600, height=400)
notepad.run()
