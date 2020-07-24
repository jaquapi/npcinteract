# Minecraft npcinteract
Generates a datapack that makes easier integration of NPC dialogs in Minecraft.
This project aims to :
- have all NPC dialogs in one file with a readable format. Which makes dialog management and translation to other languages easier.
- setup NPC states, and let the developper decide of the logical part (how/when to switch between states ...).

## Get started :
1) Open `template.txt` and write down NPC dialogs. (YML syntax highlighter works well for `template.txt`)
2) Run `python parser.py template.txt`  (Python 3+ needed)
3) Put generated datapack folder into your world's datapack folder

## How to trigger a dialog ?
Two options :
- (Automatic) Right-click the NPC (villagers only)
- (Manual) With minecraft command : 
`scoreboard players set <SELECTOR> T_<NPC> 1`

## Additionnal tricks
### Change the NPC state
- `scoreboard players set <SELECTOR> S_<NPC> <STATE_NUMBER>`

### Check end of dialog
Check for NPC state -1. For example :
- `execute if entity @a[scores={T_<NPC>=-1}] run ...` 

## Tool configuration and more
- More options in `config.json` !
- VSCode extension here : https://github.com/KReload/npc-interact-extension

## To fix
- multiple {} in one dialog line ? do something like 'text : 123456, text: 123456, raw:{azeaeazeaezae}' ?
- S / SP works only for rightclick ... Needs update more often