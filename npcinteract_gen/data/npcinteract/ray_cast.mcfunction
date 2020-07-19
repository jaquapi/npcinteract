particle minecraft:crit ~ ~ ~ 0 0 0 0 10
tp @e[tag=NPC_RAY,type=area_effect_cloud] ~ ~ ~
function npcinteract:npc_check
scoreboard players remove @s npcRayDist 1
execute if score @s npcRayDist matches 1.. positioned ^ ^ ^1 run function npcinteract:ray_cast