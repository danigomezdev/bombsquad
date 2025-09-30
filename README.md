# Bombsquad Server

Modded server scripts to host Ballistica (BombSquad) server.  
Running on **BS 1.7.41 (API 9)**  

## Requirements

- Basic knowledge of Linux  
- A VPS (e.g. [Amazon Web Services](https://aws.amazon.com/), [Google Cloud](https://cloud.google.com/), [Microsoft Azure](https://portal.azure.com/))  
- Any Linux distribution (recommended: **Ubuntu 22 or higher**)  
- Python **3.13**  
- At least **1 GB free memory** (recommended: 2 GB)  

## Installation

### Install Python 3.13  

    sudo apt install python3.13 python3.13-dev python3.13-venv python3-pip -y  

### Update installed and existing packages  

    sudo apt update && sudo apt upgrade -y  

### Start a new tmux session  

    tmux new -s server  

### Download Server Files

    git clone --depth=1 https://github.com/danigomezdev/bombsquad

#### Now edit config.yaml in root dir change server name, port, admins, playlist, team name etc.. Making the server files executable.


    chmod 777 bombsquad_server
    chmod 777 dist/bombsquad_headless
    chmod 777 dist/bombsquad_headless_aarch64

## Starting the server
 
    ./bombsquad_server.py  

<img width="503" height="694" alt="Image" src="https://github.com/user-attachments/assets/93d5fdc5-e1dd-4203-9962-896665858ec1" />

___
### More Configuration
Open `dist/ba_root/mods/setting.json` in your prefered editor and change values according to you.

[How to edit settings.json](https://github.com/imayushsaini/Bombsquad-Ballistica-Modded-Server/wiki/Server-Settings)

[Available chat commands](https://github.com/imayushsaini/Bombsquad-Ballistica-Modded-Server/wiki/Chat-commands)

___
### Adding yourself as owner
- Open `dist/ba_root/mods/playersData/roles.json` in your prefered editor.
- Add your Pb-id in owner id list.
- Restart your server

___
### Managing players
Open `dist/ba_root/mods/playersData/profiles.json` in your prefered editor.

Here you can ban players, mute them, or disable their kick votes.


## Features
- Rank System.
- [Chat commands](https://github.com/imayushsaini/Bombsquad-Ballistica-Modded-Server/wiki/Chat-commands).
- V2 Account with cloud console for server.
- check clients ping , use /ping chat command to check ping of any player._ba.get_client_ping().
- Hide player specs from cleints, chatcommand /hideid /showid .
- [Easy role management](https://github.com/imayushsaini/Bombsquad-Ballistica-Modded-Server/wiki/Chat-commands#role-management-system) , create 1000 of roles as you wish add specific chat command to the role , give tag to role ..many more.
- Rejoin cooldown.
- Leaderboard , top 3 rank players name on top right corner.
- Restrict some player to start kick vote.
- Allow server owners to join even when server is full by looking owner IP address which was used earlier(don't join by queue).
- Auto kick fake accounts (unsigned/not verified by master server).
- Auto enable/disable public queue when server is full.
- Auto night mode.
- Transparent Kickvote , can see who started kick vote for whom.
- Kickvote msg to chat/screen , can choose to show kickvote start msg either as screen message or chat message.
- Players IP Address and Device UUID tracking and banning.
- Team Chat, send msg starting with (,) comma to deliver it to team mates only.
- In game popup chat , send msg starting with (.) Dot to send in game popup msg.
- Custom Voting System , type end in chat to start end vote or sm , nv, dv.
- support for [Ballisitca-web-stats](https://github.com/imayushsaini/ballistica-web-stats).
- Integrated Discord bot to sync live stats(current players, chats , all logs) to discord.
- Execute chat command remotely from discord.
- Many New mini games and maps.
- Colourfull bomb explosion.
- Floater
- Auto stats reset after configured days .
- Auto remove afk/idle players.
- Auto check server updates.
- All settings at one place ,no coding exp. required just edit settings.json 
- Configurable Server Host name.
- Character chooser , players can choose any character while joining .
- Restrict New accounts to join or chat in server.
- Custom characters , easy to load and use characters made by character maker.
- Auto Team Balance , player shift to small team in dualteam mode.
- Integrated ElPatronPowerups.
- Auto switch to coop mode when players are less then threshold.
- Change playlist on fly with playlist code or name , i.e /playlist teams , /playlist coop , /playlist 34532
- rotate prop nodes with node.changerotation(x,y,z)
- set 2d mode with _ba.set_2d_mode(true)
- set 2d plane with _ba.set_2d_plane(z) - beta , not works with spaz.fly = true. 
- New Splitted Team in game score screen.
- New final score screen , StumbledScoreScreen.
- other small small feature improvement here there find yourself.
