def readAllText(filePath):
    f = open(filePath, "r", encoding="utf8")
    ret = f.read()
    f.close()
    return ret

def mapFileToLanguage(filename):
    if filename == "english.json" or filename == "english2.json":
        return "English"
    elif filename == "finnish.json":
        return "Finnish"
    elif filename == "norwegian.json" or filename == "norwegian2.json":
        return "Norwegian"
    elif filename == "polish.json":
        return "Polish"
    elif filename == "russian.json":
        return "Russian"
    elif filename == "spanish.json":
        return "Spanish"
    else:
        return filename