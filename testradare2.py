import r2pipe

#Here,we used rasm2 to decompiling hexadecimal message to CL instruction
def radare2_Decompile_Tool(str,flag):
    cpu_Structure = "x86"
    cpu_Register_bit = "64"
    if(flag == 1):
        return r2.syscmd("rasm2 -a " + cpu_Structure + " -b " + cpu_Register_bit + " -d " + str)
    if (flag == 2):
        return r2.syscmd("rasm2 -a " + cpu_Structure + " -b " + cpu_Register_bit + " " + str)


path="./test.out"
flags = ["-w"]
r2=r2pipe.open(path,flags )
str=r2.cmd("pdV")
print(radare2_Decompile_Tool("0x75fe",1))


#print str
# print("----------------------------------------")
print(r2.cmd("s 0x0040068a"))
print(r2.cmd("px 20"))
r2.cmd("wx 75")
print(r2.cmd("px 20"))
#https://radare.gitbooks.io/radare2book/content/scripting/r2pipe.html