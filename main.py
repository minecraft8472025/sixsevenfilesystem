import sys

ekey = {}

chars = [chr(cp) for cp in range(0x110000)]  # Unicode range: U+0000 to U+10FFFF
ekey.update({item: i for i, item in enumerate(chars, start=53)})
dkey = {v: k for k, v in ekey.items()}


def encrypt(text, encoding="67"):
    output = encoding
    for ch in text:
        code = ekey[ch]
        output += "6" * ((code // 10) + 1) + "7" * ((code % 10) + 1)
    if encoding == "76":
        output = output[::-1]
    return output


def decrypt(text):
    encoding = text[:2]
    text = text[2:]
    sections = text.split("76")

    # Reconstruct the original 6/7 blocks
    for i in range(len(sections) - 2):
        sections[i + 1] = "6" + sections[i + 1] + "7"
    sections[0] = sections[0] + "7"
    sections[-1] = "6" + sections[-1]

    characters = []
    for sec in sections:
        tens = sec.count("6") - 1
        ones = sec.count("7") - 1
        characters.append((tens * 10) + ones)

    output = "".join(dkey[i] for i in characters)

    if encoding == "76":
        output = output[::-1]

    return output


if len(sys.argv) == 1:
    print("Run this code with a filename as the argument.")
    exit()

filename = sys.argv[1]

if filename.endswith(".sixseven"):
    # Decrypt
    with open(filename, "r", encoding="utf-8") as f:
        decrypted_text = decrypt(f.read())

    # Convert characters back to bytes
    data = decrypted_text.encode("latin-1", errors="strict")

    outname = filename.replace(".sixseven", "")
    with open(outname, "wb") as f:
        f.write(data)

else:
    # Encrypt
    with open(filename, "rb") as f:
        raw = f.read()

    # Convert bytes → characters (reversible)
    text = raw.decode("latin-1", errors="strict")

    encrypted = encrypt(text)

    with open(filename + ".sixseven", "w", encoding="utf-8") as f:
        f.write(encrypted)
