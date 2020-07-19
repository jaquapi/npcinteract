
#raycast
execute as @a[scores={npcTalkedTo=1..}] at @s anchored eyes positioned ^ ^ ^ run function npcinteract:ray_init

#npc speak
function npcinteract:npc/steve
function npcinteract:npc/markus