scoreboard players add @a[scores={T_steve=1..,SP_steve=1..}] T_steve 1

scoreboard players set @a[scores={T_steve=2..,SP_steve=0}] T_steve 0

tellraw @a[scores={T_steve=2,SP_steve=1}] ["",{"text": "[Steve] ", "bold": "true", "color": "yellow"},{"text": "Hello !", "color": "white"}]
tellraw @a[scores={T_steve=42,SP_steve=1}] ["",{"text": "[Steve] ", "bold": "true", "color": "yellow"},{"text": "I'm Steve.", "color": "white"}]
tellraw @a[scores={T_steve=82,SP_steve=1}] ["",{"text": "[Steve] ", "bold": "true", "color": "yellow"},{"text": "Nice to meet you !", "color": "white"}]
scoreboard players set @a[scores={T_steve=122..,SP_steve=1}] T_steve 0

