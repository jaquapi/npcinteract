# Minecraft npcinteract
Generates a datapack that makes easier integration of NPC dialogs in Minecraft.
This project aims to :
- have all NPC dialogs in one file with a readable format. Which makes dialog management and translation to other languages easier.
- setup NPC states, and let the developper decide of the logical part (how/when to switch between states ...).

## Get started :
1) Open `template.txt` and write down NPC dialogs. (YML syntax highlighter works well for `template.txt`)
2) Run `python parser.py template.txt`  (Python 3+ needed)
3) Put generated datapack folder into your world's datapack folder

## How to use the datapack ?
### Trigger dialog
Two options :
- (Automatic) Right-click the NPC (villagers only)
- (Manual) Set NPC timer value to 1 : 
    - `scoreboard players set <SELECTOR> T_<NPC> 1`

### Change NPC state
Change NPC state value :
- `scoreboard players set <SELECTOR> S_<NPC> <STATE_VALUE>`

### Change NPC state and trigger dialog
For example :
- `execute as <SELECTOR> store success score @s T_<NPC> run scoreboard players set @s S_<NPC> <STATE_VALUE>`

### Check start of dialog
Check for NPC timer value 2. For example :
- `execute if entity @a[scores={T_<NPC>=2}] run ...` 

### Check end of dialog
Check for NPC timer value -1. For example :
- `execute if entity @a[scores={T_<NPC>=-1}] run ...` 

## Tool configuration and more
- More options in `config.json` !
- VSCode extension here : https://github.com/KReload/npc-interact-extension

## To fix
- does not support anything other than {"text":"123"}
