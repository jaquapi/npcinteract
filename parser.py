import json
import os

def txtParser(pathin="template.txt",pathout="out.json"):

    #default values
    rawparam = {"color":"white"}
    param = {"delay":"40"}

    dicts=[]
    iNpc=-1 #current npc
    iState = 0  #current state

    with open(pathin,'r',encoding='utf8') as fin:
        for line in fin:
            listL = line.strip().split(":",1)

            listL = [l.strip() for l in listL]

            if checkName(listL,dicts):
                iNpc = len(dicts)-1

            elif (iNpc >= 0) & isValid(listL):

                if listL[0] == "color":
                    rawparam["color"] = listL[1]

                elif listL[0] == "delay":
                    param["delay"] = listL[1]

                elif listL[0][0] == '%':
                    iState = listL[0].split('%')[1]
                    dicts[iNpc]["texts"][iState] = []   #overrides previous entries associated with 'iState'

                elif listL[0] == "text":
                    d = {"raw":{"text":listL[1]}}
                    d["raw"].update(rawparam)
                    d.update(param)
                    dicts[iNpc]["texts"][iState].append(d)

                else :
                    print("(Invalid key/value) "+line)

    with open(pathout,'w',encoding='utf8') as fout:
        json.dump(dicts,fout,indent=3,sort_keys=True)

    return dicts
                

def checkName(listL,dicts):
    if listL[0] == "name":
        print("Got "+listL[1])
        id = len(dicts)
        dicts.append({"name":listL[1],"id":id})
        dicts[id]["texts"] = {}
        dicts[id]["texts"]["0"] = []    #initializes at iState=0
        return True

    else:
        return False

def isValid(listL):
    if not listL[0]:    #empty line
        return False
    elif listL[0][0] == '%':    #state line
        s=listL[0].split("%",1)
        if len(s) < 2:  #nothing after %
            print("(Missing state value)")
            return False
        elif is_int(s[1]): #int after %
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

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def mc_writer(dicts,out="result"):
    os.mkdir(out)
    print("ok")

if __name__ == "__main__":

    d = txtParser()
    mc_writer(d)

    pass