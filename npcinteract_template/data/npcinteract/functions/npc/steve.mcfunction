scoreboard players add @a[scores={T_Steve=1..}] T_Steve 1

tellraw @a[scores={T_Steve=2}] {"text":"[STEVE] Hello !","color":"gold"}
tellraw @a[scores={T_Steve=52}] {"text":"[STEVE] I'm Steve.","color":"gold"}
tellraw @a[scores={T_Steve=102}] {"text":"[STEVE] Nice to meet you !","color":"gold"}
scoreboard players set @a[scores={T_Steve=103..}] T_Steve 0