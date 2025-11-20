import sys

ekey = {}

chars = [chr(cp) for cp in range(0x110000)]  # Unicode range: U+0000 to U+10FFFF

ekey.update({item: i for i, item in enumerate(chars, start=53)})

dkey = {v: k for k, v in ekey.items()}

def encrypt(text,encoding="67"):
    output = encoding
    characters = list(text)
    for i in range(len(characters)):
        characters[i] = ekey[characters[i]]
        output += "6"*((characters[i] // 10)+1) + "7"*((characters[i] % 10)+1)
    if encoding == "76":
        output = output[::-1]
    return output

def decrypt(text):
    encoding = text[:2]
    text = text[2:]
    characters = []
    output = ""
    sections = text.split("76")
    for i in range(len(sections)-2):
        sections[i+1] = "6"+sections[i+1]+"7"
    sections[0] = sections[0] + "7"
    sections[-1] = "6" + sections[-1]
    for i in range(len(sections)):
        tens = sections[i].count("6")-1
        ones = sections[i].count("7")-1
        characters.append((tens*10)+ones)
    for i in characters:
        output += dkey[i]
    if encoding == "76":
        output = output[::-1]
    return output

if len(sys.argv) == 1:
    print("Run this code with a filename as the argument.")
    exit()

with open(sys.argv[1],"r") as file:
    if sys.argv[1].split(".")[-1] == "sixseven":
        data = decrypt(file.read())
        with open(sys.argv[1].replace(".sixseven",""),"w") as outputfile:
            outputfile.write(data)
    else:
        data = encrypt(file.read())
        with open(sys.argv[1]+".sixseven","w") as outputfile:
            outputfile.write(data)
        