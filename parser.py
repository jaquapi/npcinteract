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

def pack_writer(dicts,out="npcinteract_gen"):
    
    #root
    force_mkdir(out)
    os.chdir(out)
    dir_root=os.getcwd()    #

    with open("pack.mcmeta","w",encoding='utf8') as f:
        json.dump({"pack": {"pack_format": 5,"description": "NPC Interact"}},f,indent=4)

    #data
    force_mkdir("data")
    os.chdir("data")
    dir_data=os.getcwd()    #

    #minecraft
    force_mkdir("minecraft/tags/functions")
    os.chdir("minecraft/tags/functions")
    with open("load.json","w",encoding="utf8") as f:
        json.dump({"replace": False,"values": ["npcinteract:load"]},f,indent=4)
    with open("tick.json","w",encoding="utf8") as f:
        json.dump({"replace": False,"values": ["npcinteract:tick"]},f,indent=4)

    #npcinteract core
    os.chdir(dir_data)
    force_mkdir("npcinteract/functions/npc")
    os.chdir("npcinteract/functions")
    with open("ray_init.mcfunction","w",encoding="utf8") as f:
        f.write('scoreboard players set @s npcRayDist 20\nsummon area_effect_cloud ~ ~ ~ {Tags:["NPC_RAY"],Duration:20,Radius:0f}\nfunction npcinteract:ray_cast\nkill @e[tag=NPC_RAY,type=area_effect_cloud]\nscoreboard players set @s npcTalkedTo 0\n')
    with open("ray_cast.mcfunction","w",encoding="utf8") as f:
        f.write('particle minecraft:crit ~ ~ ~ 0 0 0 0 10\ntp @e[tag=NPC_RAY,type=area_effect_cloud] ~ ~ ~\nfunction npcinteract:npc_check\nscoreboard players remove @s npcRayDist 1\nexecute if score @s npcRayDist matches 1.. positioned ^ ^ ^1 run function npcinteract:ray_cast')

    #npcinteract npc specific
    with open("tick.mcfunction","w",encoding="utf8") as f:
        f.write(gets_tick(dicts))

    with open("load.mcfunction","w",encoding="utf8") as f:
        f.write(gets_load(dicts))

    with open("npc_check.mcfunction","w",encoding="utf8") as f:
        f.write(gets_checks(dicts))

    os.chdir("npc")
    for npc in dicts:
        n = get_varname(npc["name"])

        path = n+"_check.mcfunction"
        with open(path,"w",encoding="utf8") as f:
            f.write(gets_npccheck(npc["name"]))

        path = n+".mcfunction"
        with open(path,"w",encoding="utf8") as f:
            f.write(gets_npc(npc))


def gets_tick(dicts):
    s='execute as @a[scores={npcTalkedTo=1..}] at @s anchored eyes positioned ^ ^ ^ run function npcinteract:ray_init\n'
    for npc in dicts:
        s+='function npcinteract:npc/'+get_varname(npc["name"])+'\n'
    return s

def gets_load(dicts):
    s='say Loaded npcinteract datapack\n\n'
    s+='scoreboard objectives add npcRayDist dummy\nscoreboard objectives add npcTalkedTo minecraft.custom:minecraft.talked_to_villager\n'
    for npc in dicts:
        name = get_varname(npc["name"])
        s+='scoreboard objectives add T_'+name+' dummy\nscoreboard players set @a T_'+name+' 0\n'
        s+='scoreboard objectives add S_'+name+' dummy\nscoreboard players set @a S_'+name+' 0\n'
        s+='scoreboard objectives add SP_'+name+' dummy\nscoreboard players set @a SP_'+name+' 0\n'
    return s

def gets_checks(dicts):
    s=""
    for npc in dicts:
        s+='execute at @e[name="'+npc["name"]+'"] anchored eyes positioned ^ ^ ^ if entity @e[tag=NPC_RAY,distance=..1] run function npcinteract:npc/'+get_varname(npc["name"])+'_check\n'
    print(s)
    return s

def gets_npccheck(name):
    n=get_varname(name)
    s='scoreboard players set @s npcRayDist 0\n'
    s+='scoreboard players operation @s SP_'+n+' = @s S_'+n+'\n'
    s+='scoreboard players set @s T_'+n+' 1'
    return s

def gets_npc(dict):
    #Input dict of one NPC
    
    #title
    title_param={"bold":"true","color":"yellow"} #param of name title
    title={"text":"["+dict["name"]+"] "}
    title.update(title_param)

    name=get_varname(dict["name"])

    s='scoreboard players add @a[scores={T_'+name+'=1..,SP_'+name+'=1..}] T_'+name+' 1\n\n'
    for state,txts in dict["texts"].items():
        totDelay=2
        for txt in txts:
            s_temp='tellraw @a[scores={T_'+name+'='+str(totDelay)+',SP_'+name+'='+state+'}] ["",'+json.dumps(title)+','+json.dumps(txt["raw"])+']\n'
            s += s_temp
            totDelay+=int(txt["delay"])
        
        s+='scoreboard players set @a[scores={T_'+name+'='+str(totDelay)+'..,SP_'+name+'='+state+'}] T_'+name+' 0\n\n'
    return s


def get_varname(name):
    return name.strip().replace(" ","").replace("'","").replace("\"","").lower()[:12]

def force_mkdir(dir):
    try:
        os.makedirs(dir)  
    except:
        pass

if __name__ == "__main__":

    d = txtParser()
    pack_writer(d)

    pass