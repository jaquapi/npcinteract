#Execute when NPC is triggered

#stop ray
scoreboard players set @s npcRayDist 0

#update internal state
scoreboard players operation @s SP_Markus = @s S_Markus

#restart dialog timer
scoreboard players set @s T_Markus 1

# scoreboard players set @s[scores={T_Markus=0}] T_Markus 1
# scoreboard players set @s[scores={SP_Markus=0}] T_Markus 0