### IMPORTs ###
from flask import Flask, render_template, request, jsonify


### Initializing the environment(Registers, Flags, Variables)

instructions=["mov","push","pop","xchg","add","adc","sub","sbb","cnp","inc","dec","mul","div","not","or","and","xor","call","ret","jump","jc","jnc","jz","jnz","js","jns","stc","clc"]
registers={"ax":0,"bx":0,"cx":0,"dx":0}
flags={"sign":False,"zero":False,"carry":False}
stack = []
code = dict()
counter = 0

### Defining function for addressing modes

def getVal(operand):
    if operand in registers.keys():
        return registers[operand]
    else:
        return int(operand, 16)

### Defining functions for setting Flags

def setCarry(value):
    if(value >= 65536):
        flags["carry"] = True

def setSign(value):
    if(value < 0):
        flags["sign"] = True

def setZero(value):
    if(value == 0):
        flags["zero"] = True

### Defining functions for instructions

def mov(operand1, operand2):
    registers[operand1] = getVal(operand2)

def push(operand1):
    stack.append(getVal(operand1))

def pop(operand1):
    registers[operand1] = stack[-1]
    del stack[-1]

def xchg(operand1, operand2):
    temp = registers[operand1]
    registers[operand1] = registers[operand2]
    registers[operand2] = temp

def add(operand1, operand2, operand3 = "0"):
    registers[operand1] = registers[operand1] + getVal(operand2) + getVal(operand3)
    setCarry(registers[operand1])
    setSign(registers[operand1])
    setZero(registers[operand1])

def sub(operand1, operand2, operand3 = "0"):
    registers[operand1] = registers[operand1] - getVal(operand2) - getVal(operand3)
    setCarry(registers[operand1])
    setSign(registers[operand1])
    setZero(registers[operand1])

def cmp(operand1, operand2):
    return (getVal(operand1) < getVal(operand2))

def inc(operand1):
    registers[operand1] = registers[operand1] + 1
    setCarry(registers[operand1])
    setSign(registers[operand1])
    setZero(registers[operand1])

def dec(operand1):
    registers[operand1] = registers[operand1] - 1
    setCarry(registers[operand1])
    setSign(registers[operand1])
    setZero(registers[operand1])

def mul(operand1, operand2 = "1"):
    registers["ax"] = registers["ax"] * getVal(operand1) * getVal(operand2)
    setCarry(registers["ax"])
    setSign(registers["ax"])
    setZero(registers["ax"])

def div(operand1):
    registers["ax"] = registers["ax"] / getVal(operand1)
    setCarry(registers["ax"])
    setSign(registers["ax"])
    setZero(registers["ax"])

def not1(operand1):
    registers[operand1] = ~registers[operand1]
    setCarry(registers[operand1])
    setSign(registers[operand1])
    setZero(registers[operand1])

def or2(operand1, operand2):
    registers[operand1] = getVal(operand1) | getVal(operand2)
    setCarry(registers[operand1])
    setSign(registers[operand1])
    setZero(registers[operand1])

def or3(operand1, operand2, operand3):
    registers[operand1] = or2(operand1, or2(operand2, operand3))
    setCarry(registers[operand1])
    setSign(registers[operand1])
    setZero(registers[operand1])

def and2(operand1, operand2):
    registers[operand1] = getVal(operand1) & getVal(operand2)
    setCarry(registers[operand1])
    setSign(registers[operand1])
    setZero(registers[operand1])

def and3(operand1, operand2, operand3):
    registers[operand1] = and2(operand1, and2(operand2, operand3))
    setCarry(registers[operand1])
    setSign(registers[operand1])
    setZero(registers[operand1])

def xor2(operand1, operand2):
    registers[operand1] = getVal(operand1) ^ getVal(operand2)
    setCarry(registers[operand1])
    setSign(registers[operand1])
    setZero(registers[operand1])

def jump(label):
    global counter
    counter = int(label)

def jc(label):
    global counter
    if(flags["carry"]):
        counter = int(label)
    else:
        counter = counter+1

def jnc(label):
    global counter
    if(flags["carry"]):
        counter = counter+1
    else:
        counter = int(label)

def jz(label):
    global counter
    if(flags["zero"]):
        counter = int(label)
    else:
        counter = counter+1

def jnz(label):
    global counter
    if(flags["zero"]):
        counter = counter+1
    else:
        counter = int(label)

def js(label):
    global counter
    if(flags["sign"]):
        counter = int(label)
    else:
        counter = counter+1

def jns(label):
    global counter
    if(flags["sign"]):
        counter = counter+1
    else:
        counter = int(label)

def stc():
    flags["carry"] = True

def clc():
    flags["carry"] = False


### Executing a line of code

def executeCodeLine(line):
    global counter
    opcode = line.split()[0]
    operands = [operand.strip() for operand in line.split(" ",1)[1].split(",")]
    if(opcode == "mov"):
        mov(operands[0], operands[1])
        counter = counter + 1
    elif(opcode == "push"):
        push(operands[0])
        counter = counter + 1
    elif(opcode == "pop"):
        pop(operands[0])
        counter = counter + 1
    elif(opcode == "xchg"):
        xchg(operands[0], operands[1])
        counter = counter + 1
    elif(opcode == "add"):
        if(len(operands) == 2):
            add(operands[0], operands[1])
            counter = counter + 1
        elif(len(operands) == 3):
            add(operands[0], operands[1], operands[2])
            counter = counter + 1
    elif(opcode == "sub"):
        if(len(operands) == 2):
            sub(operands[0], operands[1])
            counter = counter + 1
        elif(len(operands) == 3):
            sub(operands[0], operands[1], operands[2])
            counter = counter + 1
    elif(opcode == "cmp"):
        cmp(operands[0], operands[1])
        counter = counter + 1
    elif(opcode == "inc"):
        inc(operands[0])
        counter = counter + 1
    elif(opcode == "dec"):
        dec(operands[0])
        counter = counter + 1
    elif(opcode == "mul"):
        if(len(operands) == 1):
            mul(operands[0])
            counter = counter + 1
        elif(len(operands) == 2):
            mul(operands[0], operands[1])
            counter = counter + 1
    elif(opcode == "div"):
        div(operands[0])
        counter = counter + 1
    elif(opcode == "not"):
        not1(operands[0])
        counter = counter + 1
    elif(opcode == "or"):
        if(len(operands) == 2):
            or2(operands[0], operands[1])
            counter = counter + 1
        elif(len(operands) == 3):
            or3(operands[0], operands[1], operands[2])
            counter = counter + 1
    elif(opcode == "and"):
        if(len(operands) == 2):
            and2(operands[0], operands[1])
            counter = counter + 1
        elif(len(operands) == 3):
            and3(operands[0], operands[1], operands[2])
            counter = counter + 1
    elif(opcode == "xor"):
        xor2(operands[0], operands[1])
        counter = counter + 1
    elif(opcode == "jump"):
        jump(operands[0])
    elif(opcode == "jc"):
        jc(operands[0])
    elif(opcode == "jnc"):
        jnc(operands[0])
    elif(opcode == "jz"):
        jz(operands[0])
    elif(opcode == "jnz"):
        jnz(operands[0])
    elif(opcode == "js"):
        js(operands[0])
    elif(opcode == "jns"):
        jns(operands[0])

### Setting up the Flask Environment
app = Flask(__name__)

### Sending the webpage
@app.route('/')
def index():
    return render_template('index.html')

### Adding code line to dictionary

@app.route('/enter')
def addLine():
    global code
    line = request.args.get('line', 0).lower()
    if(line.split()[0] in instructions):
        code[len(code)] = line
    codeTable =[]
    for i in range(len(code)):
        temp = dict()
        temp["label"] = i
        temp["code"] = code[i]
        codeTable.append(temp)
    return jsonify(codeTable)

### Executing the program

@app.route('/halt')
def run():
    global code
    while counter < len(code):
        executeCodeLine(code[counter])
    resultTable = []
    for register in registers.keys():
        rTemp = dict()
        rTemp["label"] = register
        rTemp["value"] = hex(registers[register])
        resultTable.append(rTemp)
    for flag in flags.keys():
        fTemp = dict()
        fTemp["label"] = flag
        fTemp["value"] = flags[flag]
        resultTable.append(fTemp)
    return jsonify(resultTable)

@app.route('/documentation')
def docs():
    return render_template('documentation.html')

@app.route('/reset')
def reset():
    global registers
    global flags
    global stack
    global code
    global counter
    registers={"ax":0,"bx":0,"cx":0,"dx":0}
    flags={"sign":False,"zero":False,"carry":False}
    stack = []
    code = dict()
    counter = 0
    return render_template('index.html')

#code[0] = "mov ax, fff"
#code[1] = "mov bx, 444"
#code[2] = "sub ax, bx"
#code[3] = "jns 2"
#code[4] = "add ax"

if __name__ == "__main__":
    app.run()

#print(run(code))
#print(flags)
