# KIVI Clapperboard
> Part of Project KIVI (dead lol)
![image](https://github.com/KipJM/KiviClapperboard/assets/25549410/a9029601-9141-42b7-a046-4afd6f5f20d6)

## Function
This **addon for blender** helps you sync real-world video data to the Blender timeline.  
This **addon for blender** spawns a virtual clapperboard. When the blender timeline is playing, pressing the **FLASH** button will add a new marker to the current time on the timeline.

## Ok why would I want this
This was built for our movie production. Our camera is equipped with a Vive Tracker that's recording pose data into Blender keyframes through OpenVRStreamer.  
Accounting for the delay and offset between the video and tracker data is really annoying. This fixes this issue.  
This functions similarily as a physical clapperboard, it gives you a point of reference to match real-world time to Blender's timeline (or vice versa)  

## Features
- clapperboard with adjustable size
- system clock on clapperboard
- visual clap
- audio clap
- timeline marker clap

## Why this addon is absolutely terribly written
I wanted to get this thing done, and it was never really designed to be published. Oh well  
It requires you to install pygame to your blender python, it runs on another thread, it handles data REALLY dangerously, it only works on windows because of winsound, it also requires you to install a hard to find font for it to look good
oh yeah it also uses the windows emoji font. Oops

YES YOU HEARD THAT RIGHT THIS ADDON RUNS A SHAKY ADDITIONAL THREAD ON TOP OF BLENDER(UNSUPPORTED AS HELL) TO DISPLAY A PYGAME WINDOW(YES PYGAME) SO YOU CAN HAVE A SIMPLE CLAPPERBOARD THAT'S DEFINETLY NOT GOING TO CRASH BLENDER AT ANY TIME. SORRY.

# Installation
**This addon ONLY works on Windows because of the winsound API. You can easily tweak it to make it work on other OSes**
1. go to ```blender_installation_folder/version_number(example:4.0)/python/bin/```, and run a command prompt here
2. type ```./python -m pip install pygame``` to install pygame (You have to do this everytime you upgrade Blender btw)
3. (optional but really recommended) Install the font ```microgramma DOT-BolExt``` to your computer (Get this font *legally* from the Internet)
4. Install the addon normally
5. You can find it in the N-panel (right side panel) of the 3D view, under ```KIVI```.  
