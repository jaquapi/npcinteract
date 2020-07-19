say Loaded npcinteract datapack

# Core
scoreboard objectives add npcRayDist dummy
scoreboard objectives add npcTalkedTo minecraft.custom:minecraft.talked_to_villager

# NPCs
scoreboard objectives add T_Steve dummy
scoreboard objectives add S_Steve dummy
scoreboard objectives add SP_Steve dummy
scoreboard objectives add T_Markus dummy
scoreboard objectives add S_Markus dummy
scoreboard objectives add SP_Markus dummy


scoreboard players set @a T_Markus 0
scoreboard players set @a S_Markus 0
scoreboard players set @a SP_Markus 0
scoreboard players set @a T_Steve 0
scoreboard players set @a S_Steve 0
scoreboard players set @a SP_Steve 0