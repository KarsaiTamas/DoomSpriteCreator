# DoomSpriteCreator
For those who don't use github. To download it click code and click download zip. The python file is inside if blender can't recognize it with the zip file.

WIP
This is a blender addon to make sprites easier from your blender models for doom.

This will have more options, just this is the first mostly properly working version 
and just want to save it to github, for good mesure.

To remove shadows from render combine the Principled BSDF with Emission shader
The emission shader should get it's color from the texture colors aka diffuse

I did managed to set the background to be transparent for the sprite renders.

Still missing setting for the start sprite frame aka the 5th letter so it always start with A for now, 
but I will change that soonTM :D  

Use case: 

Position your camera where you want your camera to render your sprites. 
HIT the set data for cam position button

Set object to rotate, to be your character/object, 
if your character don't want to rotate for the renders 
than parent it under an empty and set that to be the object to rotate.

Don't leave render location to be empty, so just simply copy paste a path into it, where you want to save your sprites.

You can select different animations, so anything under that is for the selected animation.

Camera position is where your cam gonna make the renders.

Angle count is the number of angles you want for your character. options are 1,4,5,8.

Frames: They go from left to right. Set the values to be NOT -1 for them to render that frame of your animation. 
-1 values are skipped.

If you set up everything than just hit, make sprites for the selected animation button, 
than it will start rendering your sprites.

