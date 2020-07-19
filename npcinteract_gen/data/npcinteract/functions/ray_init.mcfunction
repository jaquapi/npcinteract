scoreboard players set @s npcRayDist 20
summon area_effect_cloud ~ ~ ~ {Tags:["NPC_RAY"],Duration:20,Radius:0f}
function npcinteract:ray_cast
kill @e[tag=NPC_RAY,type=area_effect_cloud]
scoreboard players set @s npcTalkedTo 0
