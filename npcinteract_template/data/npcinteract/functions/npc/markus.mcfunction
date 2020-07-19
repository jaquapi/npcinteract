scoreboard players add @a[scores={T_Markus=1..,SP_Markus=1..}] T_Markus 1

tellraw @a[scores={T_Markus=2,SP_Markus=1}] {"text":"[MARKUS] Hola !","color":"gold"}
tellraw @a[scores={T_Markus=52,SP_Markus=1}] {"text":"[MARKUS] My name is Markus.","color":"gold"}
tellraw @a[scores={T_Markus=102,SP_Markus=1}] {"text":"[MARKUS] Nice to meet you !","color":"gold"}
scoreboard players set @a[scores={T_Markus=102..,SP_Markus=1}] T_Markus 0

tellraw @a[scores={T_Markus=2,SP_Markus=2}] {"text":"[MARKUS] Bye !","color":"gold"}
tellraw @a[scores={T_Markus=52,SP_Markus=2}] {"text":"[MARKUS] See you later !","color":"gold"}
scoreboard players set @a[scores={T_Markus=52..,SP_Markus=2}] T_Markus 0

tellraw @a[scores={T_Markus=2,SP_Markus=3}] {"text":"[MARKUS] You can talk to Steve too","color":"gold"}
scoreboard players set @a[scores={T_Markus=2..,SP_Markus=3}] T_Markus 0