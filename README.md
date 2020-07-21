# Minecraft npcinteract
Generates a datapack that makes easier integration of NPC dialogs in Minecraft.
This project aims to :
- have all NPC dialogs in one file with a readable format. Which makes dialog management and traduction to other languages easier.
- setup NPC states, and let the developper decide of the logical part (how/when to switch between states ...).

## Get started :
1) Open `template.txt` and write down NPC dialogs. 
2) Run `python parser.py template.txt`  (Python 3+ needed)
3) Put generated datapack folder into your world's datapack folder

## How to change an NPC state ?
- With minecraft command :
`scoreboard players set <SELECTOR> S_<NPC> <STATE_NUMBER>`

## How to trigger a dialog ?
Two options :
- (Automatic) Right-click the NPC (villagers only)
- (Manual) With minecraft command : 
`scoreboard players set <SELECTOR> T_<NPC> 1`

## Tool configuration and more
- More options in `config.json` !
- YML syntax highlighter works well for `template.txt`
- VSCode extension here : https://github.com/KReload/npc-interact-extension
