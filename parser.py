import json
import os

class NpcParser:
    def __init__(self, inputPath, outputPath):
        self.npcList = []
        self.currentNpc = -1
        self.currentState = 0
        self.rawParam = {"color":"white"}
        self.param = {"delay":"40"}
        self.pathIn = inputPath
        self.pathOut = outputPath

    def parse(self):

        #default values
        rawparam = {"color":"white"}
        param = {"delay":"40"}

        with open(self.pathIn,'r',encoding='utf8') as fin:
            for line in fin:
                listL = line.strip().split(":",1)

                listL = [l.strip() for l in listL]

                if self.checkName(listL):
                    self.currentNpc = len(self.npcList)-1

                elif (self.currentNpc >= 0) & self.isValid(listL):

                    if listL[0] == "color":
                        rawparam["color"] = listL[1]

                    elif listL[0] == "delay":
                        param["delay"] = listL[1]

                    elif listL[0][0] == '%':
                        self.currentState = listL[0].split('%')[1]
                        self.npcList[self.currentNpc]["texts"][self.currentState] = []   #overrides previous entries associated with 'self.currentState'

                    elif listL[0] == "text":
                        d = {"raw":{"text":listL[1]}}
                        d["raw"].update(rawparam)
                        d.update(param)
                        self.npcList[self.currentNpc]["texts"][self.currentState].append(d)

                    else :
                        print("(Invalid key/value) "+line)

        with open("out.json",'w',encoding='utf8') as fout:
            json.dump(self.npcList,fout,indent=3,sort_keys=True)

        self.npcList = self.npcList             

    def checkName(self, listL):
        if listL[0] == "name":
            print("Got "+listL[1])
            id = len(self.npcList)
            self.npcList.append({"name":listL[1],"id":id})
            self.npcList[id]["texts"] = {}
            self.npcList[id]["texts"]["0"] = []    #initializes at self.currentState=0
            return True

        else:
            return False

    def isValid(self, listL):
        if not listL[0]:    #empty line
            return False
        elif listL[0][0] == '%':    #state line
            s=listL[0].split("%",1)
            if len(s) < 2:  #nothing after %
                print("(Missing state value)")
                return False
            elif isInt(s[1]): #int after %
                return True
            print("(Invalid state value) "+s[1])
            return False
        elif listL[0][0] == "#":    #comment line
            return False
        elif len(listL) < 2:    #missing key/value format
            print("(Missing value) "+listL)
            return False
        else:   #valid line
            return True
    
    def printFile(self):
        os.mkdir(self.pathOut)
        print("ok")


def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


if __name__ == "__main__":

    parser = NpcParser("template.txt","result")
    parser.parse()
    parser.printFile()

    pass