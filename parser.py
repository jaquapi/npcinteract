import os, sys
import json
import re

class NpcParser:
    def __init__(self, inputPath="template.txt", outputPath="npcinteract_gen"):
        self.npcList = []
        self.currentNpc = -1
        self.currentState = 0
        self.cfg = {}
        self.mcdefault_cfg = self.load_mcdefault_config()
        self.pathIn = inputPath
        self.pathOut = outputPath

    def _save_config(self,path):
        #TEMP
        d = {}

        d["nameDisplay"] = {}
        d["nameDisplay"]["bold"] = "true"
        d["nameDisplay"]["color"] = "yellow"
        d["nameDisplay"]["separator"]="[]"
        d["nameDisplay"]["italic"]= "false"
        d["nameDisplay"]["underlined"]= "false"      

        d["text"] = {}        
        d["text"]["color"]="yellow"
        d["text"]["bold"]= "false"
        d["text"]["italic"]= "false"
        d["text"]["underlined"]= "false"

        d["dialog"] = {}
        d["dialog"]["delay"] = "40"
        d["dialog"]["npcSpam"] = "false"

        d["raycast"] = {}
        d["raycast"]["hideParticle"] = "false"
        d["raycast"]["particle"] = "minecraft:crit"

        with open(path,"w",encoding="utf8") as f:
            json.dump(d,f,indent=4)
        
    def load_config(self,path):
        with open(path,"r",encoding="utf8") as f:
            self.cfg = json.load(f)

    def load_mcdefault_config(self):
        #for later default values removing

        d = {}
        d["text"] = {}

        d["text"]["color"]="white"
        d["text"]["bold"]="false"
        d["text"]["italic"]="false"
        d["text"]["underlined"]="false"

        d["nameDisplay"] = {}
        d["nameDisplay"]["bold"] = "false"
        d["nameDisplay"]["italic"]= "false"
        d["nameDisplay"]["underlined"]= "false"   
        d["nameDisplay"]["color"] = "white"

        return d

    def parse(self):
        with open(self.pathIn,'r',encoding='utf8') as fin:
            for line in fin:
                listL = line.strip().split(":",1)

                listL = [l.strip() for l in listL]

                if self.check_name(listL):
                    self.currentNpc = len(self.npcList)-1

                elif (self.currentNpc >= 0) & self.is_valid(listL):
                    
                    if listL[0] in list(self.cfg["text"].keys()):
                        self.cfg["text"][listL[0]] = listL[1]

                    # if listL[0] == "color":
                    #     self.rawParam["color"] = listL[1]

                    elif listL[0] == "delay":
                        self.cfg["dialog"]["delay"] = listL[1]

                    elif listL[0][0] == '%':
                        self.currentState = listL[0].split('%')[1]
                        self.npcList[self.currentNpc]["texts"][self.currentState] = []   #overrides previous entries associated with 'self.currentState'

                    elif listL[0] == "text":
                        d = {"raw":{"text":listL[1]}}
                        d["raw"].update( remove_duplicate(self.cfg["text"],self.mcdefault_cfg["text"]) )
                        d.update({key:self.cfg["dialog"][key] for key in ["delay"]})
                        self.npcList[self.currentNpc]["texts"][self.currentState].append(d)

                    else :
                        print("(Invalid key/value) "+line)

        with open("out.json",'w',encoding='utf8') as fout:
            json.dump(self.npcList,fout,indent=3,sort_keys=True)
          

    def check_name(self, listL):
        if listL[0] == "name":
            print("Got "+listL[1])
            id = len(self.npcList)
            self.npcList.append({"name":listL[1],"nickname":listL[1],"varname":listL[1],"id":id})
            self.npcList[id]["texts"] = {}
            self.npcList[id]["texts"]["0"] = []    #initializes at self.currentState=0
            return True
        
        elif listL[0] == "nickname":
            print("\talias "+listL[1])
            self.npcList[len(self.npcList)-1]["nickname"] = listL[1]
            return True

        elif listL[0] == "varname":
            print("\tstored as "+listL[1])
            self.npcList[len(self.npcList)-1]["varname"] = listL[1]
            return True

        else:
            return False

    def is_valid(self, listL):
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
            print("(Only one value) "+str(listL))
            return False
        else:   #valid line
            return True
    
    def printFile(self):
        os.mkdir(self.pathOut)
        print("ok")


    def pack_writer(self):
        
        #root
        self.force_mkdir(self.pathOut)
        os.chdir(self.pathOut)

        with open("pack.mcmeta","w",encoding='utf8') as f:
            json.dump({"pack": {"pack_format": 5,"description": "NPC Interact"}},f,indent=4)

        #data
        self.force_mkdir("data")
        os.chdir("data")
        dir_data=os.getcwd()    #

        #minecraft
        self.force_mkdir("minecraft/tags/functions")
        os.chdir("minecraft/tags/functions")
        with open("load.json","w",encoding="utf8") as f:
            json.dump({"replace": False,"values": ["npcinteract:load"]},f,indent=4)
        with open("tick.json","w",encoding="utf8") as f:
            json.dump({"replace": False,"values": ["npcinteract:tick"]},f,indent=4)

        #npcinteract core
        os.chdir(dir_data)
        self.force_mkdir("npcinteract/functions/npc")
        os.chdir("npcinteract/functions")
        with open("ray_init.mcfunction","w",encoding="utf8") as f:
            f.write('scoreboard players set @s npcRayDist '+self.cfg["raycast"]["distance"]+'\nsummon area_effect_cloud ~ ~ ~ {Tags:["NPC_RAY"],Duration:'+self.cfg["raycast"]["distance"]+',Radius:0f}\nfunction npcinteract:ray_cast\nkill @e[tag=NPC_RAY,type=area_effect_cloud]\nscoreboard players set @s npcTalkedTo 0\n')
        with open("ray_cast.mcfunction","w",encoding="utf8") as f:
            if self.cfg["raycast"]["hideParticle"] == "false" :
                f.write('particle '+self.cfg["raycast"]["particle"]+' ~ ~ ~ 0 0 0 0 10\n')
            f.write('tp @e[tag=NPC_RAY,type=area_effect_cloud] ~ ~ ~\nfunction npcinteract:npc_check\nscoreboard players remove @s npcRayDist 1\nexecute if score @s npcRayDist matches 1.. positioned ^ ^ ^1 run function npcinteract:ray_cast')

        #npcinteract npc specific
        with open("tick.mcfunction","w",encoding="utf8") as f:
            f.write(self.gets_tick())

        with open("load.mcfunction","w",encoding="utf8") as f:
            f.write(self.gets_load())

        with open("reset.mcfunction","w",encoding="utf8") as f:
            f.write(self.gets_reset())

        with open("npc_check.mcfunction","w",encoding="utf8") as f:
            f.write(self.gets_checks())

        os.chdir("npc")
        for npc in self.npcList:
            n = self.get_varname(npc["varname"])

            path = n+"_check.mcfunction"
            with open(path,"w",encoding="utf8") as f:
                f.write(self.gets_npccheck(npc["varname"]))

            path = n+".mcfunction"
            with open(path,"w",encoding="utf8") as f:
                f.write(self.gets_npc(npc))

        print("Datapack " + self.pathOut + " written !")


    def gets_tick(self):
        s='execute as @a[scores={npcTalkedTo=1..}] at @s anchored eyes positioned ^ ^ ^ run function npcinteract:ray_init\n'
        for npc in self.npcList:
            name = self.get_varname(npc["varname"])
            # s+='execute as @a[scores={T_'+name+'=0}] run scoreboard players operation @s SP_'+name+' = @s S_'+name+'\n' #synchro SP and S
            s+='execute as @a if score @s T_'+name+' matches -1.. unless score @s T_'+name+' matches 0 run function npcinteract:npc/'+name+'\n'
            # s+='execute as @a[scores={T_'+name+'=1..}] run function npcinteract:npc/'+name+'\n'
        return s

    def gets_load(self):
  
        s='scoreboard objectives add npcRayDist dummy\nscoreboard objectives add npcTalkedTo minecraft.custom:minecraft.talked_to_villager\n\n'
        s+='scoreboard objectives add npcinteract_once dummy\n'
        s+='execute unless score fakeplayer npcinteract_once matches 42 run function npcinteract:reset\n'
        s+='tell @a[gamemode=creative] (npcinteract) LOADED\n'
        return s

    def gets_reset(self):

        s="scoreboard players set fakeplayer npcinteract_once 42\n\n"

        for npc in self.npcList:
            name = self.get_varname(npc["varname"])
            s+='scoreboard objectives add T_'+name+' dummy\nscoreboard players set @a T_'+name+' 0\n'
            s+='scoreboard objectives add S_'+name+' dummy\nscoreboard players set @a S_'+name+' 0\n'
            s+='scoreboard objectives add SP_'+name+' dummy\nscoreboard players set @a SP_'+name+' 0\n'

        s+='tell @a[gamemode=creative] (npcinteract) RESET\n'

        return s

    def gets_checks(self):
        s=""
        for npc in self.npcList:
            s+='execute at @e[name="'+npc["name"]+'"] anchored eyes positioned ^ ^ ^ if entity @e[tag=NPC_RAY,distance=..1] run function npcinteract:npc/'+self.get_varname(npc["varname"])+'_check\n'
        return s

    def gets_npccheck(self, name):
        n=self.get_varname(name)
        s='scoreboard players set @s npcRayDist 0\n'

        if self.cfg["dialog"]["rightClickSpam"] == "false":
            s+='scoreboard players operation @s[scores={T_'+n+'=0}] SP_'+n+' = @s S_'+n+'\n'
            s+='scoreboard players set @s[scores={T_'+n+'=0}] T_'+n+' 1'
        else:
            s+='scoreboard players operation @s SP_'+n+' = @s S_'+n+'\n'
            s+='scoreboard players set @s T_'+n+' 1'            
        return s


    def gets_npc(self,dict):
        #Input dict of one NPC
        
        #title
        title={"text":self.cfg["nameDisplay"]["separator"][0]+dict["nickname"]+self.cfg["nameDisplay"]["separator"][1]+" "}
        title.update( remove_duplicate(self.cfg["nameDisplay"],self.mcdefault_cfg["nameDisplay"]) )

        name=self.get_varname(dict["varname"])

        maxDelay = 0
        s='scoreboard players add @s T_'+name+' 1\n\n'
        s+='scoreboard players operation @s[scores={T_'+name+'=3}] SP_'+name+' = @s S_'+name+'\n\n' #synchro SP and S at T=3
        for state,txts in dict["texts"].items():
            curDelay=0
            totDelay=3  #Begin dialog at T=3
            for txt in txts:
                s_temp='tellraw @s[scores={T_'+name+'='+str(totDelay)+',SP_'+name+'='+state+'}] ["",'+json.dumps(title)+','+json.dumps(txt["raw"])+']\n'
                s += s_temp
                curDelay=int(txt["delay"])
                totDelay+=curDelay
            
            totDelay -= (curDelay-1)
            if maxDelay < totDelay :
                maxDelay = totDelay
            s+='scoreboard players set @s[scores={T_'+name+'='+str(totDelay)+'..,SP_'+name+'='+state+'}] T_'+name+' -1\n\n' #Go to T=-1 upon finish

        s+='scoreboard players set @s[scores={T_'+name+'='+str(maxDelay)+'..}] T_'+name+' -1\n\n' #timeout 

        return s


    def get_varname(self, name):
        return re.sub('[^A-Za-z0-9]+', '', name).lower()[:12]

    def force_mkdir(self, dir):
        try:
            os.makedirs(dir)  
        except:
            pass

def remove_duplicate(d,dref):
    return {k:d[k] for k in d if k in dref if (d[k] != dref[k]) }

def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

if __name__ == "__main__":
    if len(sys.argv) == 2:
        d = NpcParser(inputPath=sys.argv[1])
    else:
       d = NpcParser() 
    # d._save_config("config.json")
    d.load_config("config.json")
    d.parse()
    d.pack_writer()
