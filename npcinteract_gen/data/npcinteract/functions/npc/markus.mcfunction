scoreboard players add @a[scores={T_markus=1..,SP_markus=1..}] T_markus 1

scoreboard players set @a[scores={T_markus=2..,SP_markus=0}] T_markus 0

tellraw @a[scores={T_markus=2,SP_markus=1}] ["",{"text": "[Markus] ", "bold": "true", "color": "yellow"},{"text": "Hola !", "color": "white"}]
tellraw @a[scores={T_markus=52,SP_markus=1}] ["",{"text": "[Markus] ", "bold": "true", "color": "yellow"},{"text": "My name is \"Markus\".", "color": "white"}]
tellraw @a[scores={T_markus=102,SP_markus=1}] ["",{"text": "[Markus] ", "bold": "true", "color": "yellow"},{"text": "Nice to meet you !", "color": "white"}]
scoreboard players set @a[scores={T_markus=152..,SP_markus=1}] T_markus 0

tellraw @a[scores={T_markus=2,SP_markus=2}] ["",{"text": "[Markus] ", "bold": "true", "color": "yellow"},{"text": "Bye !", "color": "white"}]
tellraw @a[scores={T_markus=52,SP_markus=2}] ["",{"text": "[Markus] ", "bold": "true", "color": "yellow"},{"text": "See you later !", "color": "white"}]
scoreboard players set @a[scores={T_markus=102..,SP_markus=2}] T_markus 0

tellraw @a[scores={T_markus=2,SP_markus=3}] ["",{"text": "[Markus] ", "bold": "true", "color": "yellow"},{"text": "You can talk to Steve too.", "color": "white"}]
tellraw @a[scores={T_markus=52,SP_markus=3}] ["",{"text": "[Markus] ", "bold": "true", "color": "yellow"},{"text": "Let's go find him ...", "color": "white"}]
scoreboard players set @a[scores={T_markus=102..,SP_markus=3}] T_markus 0

