def readAllText(filePath):
    f = open(filePath, "r", encoding="utf8")
    ret = f.read()
    f.close()
    return ret