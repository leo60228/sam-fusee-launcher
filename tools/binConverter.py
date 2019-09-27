from textwrap import wrap
import sys
import binascii
import os

def printProgressBar(progress):
    i = int(progress * 20)
    sys.stdout.write('\r')
    sys.stdout.write("[%-20s] %d%%" % ('='*i, 5*i))
    sys.stdout.flush()

def readChunks(filename, chunkSize = 128000):
    readBytes = 0
    with open(filename, "rb") as f:
        while True:
            chunk = f.read(chunkSize)
            if chunk:
                yield chunk
            else:
                break

def makeArray(filename):
    stringBuffer = "    "
    print("reading file: " + filename)

    parts = []

    length = 0

    for chunk in readChunks(filename):
        length += len(chunk)
        parts.append(", ".join(["0x" + s for s in wrap(chunk.hex(), 2)]))

    stringBuffer += "".join(parts)
    stringBuffer = "#include <Arduino.h>\n\n#define FUSEE_BIN_SIZE " + str(length) + "\nconst byte fuseeBin[FUSEE_BIN_SIZE] = {\n" + stringBuffer + "\n};"

    return stringBuffer

if(len(sys.argv) is not 2):
    sys.exit('usage: binConverter.py "pathToFile/fileName.bin"')

filename = sys.argv[1]

base = os.path.splitext(filename)[0]
fileOut = base + ".h"

stringBuffer = makeArray(filename)

print("\nwriting file: " + fileOut)
text_file = open(fileOut, "w")
text_file.write(stringBuffer)
text_file.close()

print("finished")
