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
        with open(self.pathIn,'r',encoding='utf8') as fin:
            for line in fin:
                listL = line.strip().split(":",1)

                listL = [l.strip() for l in listL]

                if self.checkName(listL):
                    self.currentNpc = len(self.npcList)-1

                elif (self.currentNpc >= 0) & self.isValid(listL):

                    if listL[0] == "color":
                        self.rawParam["color"] = listL[1]

                    elif listL[0] == "delay":
                        self.param["delay"] = listL[1]

                    elif listL[0][0] == '%':
                        self.currentState = listL[0].split('%')[1]
                        self.npcList[self.currentNpc]["texts"][self.currentState] = []   #overrides previous entries associated with 'self.currentState'

                    elif listL[0] == "text":
                        d = {"raw":{"text":listL[1]}}
                        d["raw"].update(self.rawParam)
                        d.update(self.param)
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
        self.force_mkdir("minecraft/tags/functions")
        os.chdir("minecraft/tags/functions")
        with open("ray_init.mcfunction","w",encoding="utf8") as f:
            f.write('scoreboard players set @s npcRayDist 20\nsummon area_effect_cloud ~ ~ ~ {Tags:["NPC_RAY"],Duration:20,Radius:0f}\nfunction npcinteract:ray_cast\nkill @e[tag=NPC_RAY,type=area_effect_cloud]\nscoreboard players set @s npcTalkedTo 0\n')
        with open("ray_cast.mcfunction","w",encoding="utf8") as f:
            f.write('particle minecraft:crit ~ ~ ~ 0 0 0 0 10\ntp @e[tag=NPC_RAY,type=area_effect_cloud] ~ ~ ~\nfunction npcinteract:npc_check\nscoreboard players remove @s npcRayDist 1\nexecute if score @s npcRayDist matches 1.. positioned ^ ^ ^1 run function npcinteract:ray_cast')

        #npcinteract npc specific
        with open("tick.mcfunction","w",encoding="utf8") as f:
            f.write(self.gets_tick())

        with open("load.mcfunction","w",encoding="utf8") as f:
            f.write(self.gets_load())

        with open("npc_check.mcfunction","w",encoding="utf8") as f:
            f.write(self.gets_checks())

        os.chdir("npc")
        for npc in self.npcList:
            n = self.get_varname(npc["name"])

            path = n+"_check.mcfunction"
            with open(path,"w",encoding="utf8") as f:
                f.write(self.gets_npccheck(npc["name"]))

            path = n+".mcfunction"
            with open(path,"w",encoding="utf8") as f:
                f.write(self.gets_npc(npc))


    def gets_tick(self):
        s='execute as @a[scores={npcTalkedTo=1..}] at @s anchored eyes positioned ^ ^ ^ run function npcinteract:ray_init\n'
        for npc in self.npcList:
            s+='function npcinteract:npc/'+self.get_varname(npc["name"])+'\n'
        return s

    def gets_load(self):
        s='scoreboard objectives add npcRayDist dummy\nscoreboard objectives add npcTalkedTo minecraft.custom:minecraft.talked_to_villager\n\n'
        for npc in self.npcList:
            name = self.get_varname(npc["name"])
            s+='scoreboard objectives add T_'+name+' dummy\nscoreboard players set @a T_'+name+' 0\n'
            s+='scoreboard objectives add S_'+name+' dummy\nscoreboard players set @a S_'+name+' 0\n'
            s+='scoreboard objectives add SP_'+name+' dummy\nscoreboard players set @a SP_'+name+' 0\n'
        return s

    def gets_checks(self):
        s=""
        for npc in self.npcList:
            s+='execute at @e[name="'+npc["name"]+'"] anchored eyes positioned ^ ^ ^ if entity @e[tag=NPC_RAY,distance=..1] run function npcinteract:npc/'+self.get_varname(npc["name"])+'_check\n'
        return s

    def gets_npccheck(self, name):
        n=self.get_varname(name)
        s='scoreboard players set @s npcRayDist 0\n'
        s+='scoreboard players operation @s SP_'+n+' = @s S_'+n+'\n'
        s+='scoreboard players set @s T_'+n+' 1'
        return s


    def gets_npc(self,dict):
        #Input dict of one NPC
        
        #title
        title_param={"bold":"true","color":"yellow"} #####param of name title
        title={"text":"["+dict["name"]+"] "}
        title.update(title_param)

        name=self.get_varname(dict["name"])

        s='scoreboard players add @a[scores={T_'+name+'=1..,SP_'+name+'=1..}] T_'+name+' 1\n\n'
        for state,txts in dict["texts"].items():
            totDelay=2
            for txt in txts:
                s_temp='tellraw @a[scores={T_'+name+'='+str(totDelay)+',SP_'+name+'='+state+'}] ["",'+json.dumps(title)+','+json.dumps(txt["raw"])+']\n'
                s += s_temp
                totDelay+=int(txt["delay"])
            
            s+='scoreboard players set @a[scores={T_'+name+'='+str(totDelay)+'..,SP_'+name+'='+state+'}] T_'+name+' 0\n\n'
        return s


    def get_varname(self, name):
        return name.strip().replace(" ","").replace("'","").replace("\"","").lower()[:12]

    def force_mkdir(self, dir):
        try:
            os.makedirs(dir)  
        except:
            pass

def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

if __name__ == "__main__":

    d = NpcParser("template.txt", "npc_interact_gen")
    d.pack_writer()
    pass