<h1 align=”center”>
Black Widow Python
</h1>

Black Widow is a project I created using the Python programming language with the use of the Pygame set of Python modules. This application is a loose reimagining of the 1982 Atari arcade game Black Widow.

## How To Play
Black Widow has the player taking control of a Black Widow that can fire a projectile in four directions. Enemy bugs will begin to swarm the screen which leaves the player with the goal to eliminate the enemies and collect the grub they drop. Enemies come in a variety of types with unique behaviors so be careful. Every 60 seconds that pass in the game, the game becomes faster causing the challenge to increase as time passes. The goal of the game is to see how much grub (how many points) the player can collect before being defeated. The player’s high score is saved so they can try and beat their previous record in that instance. The game uses a mix of 2D assets and 3D models created from the OpenGL Python module with textures applied to many. The exe file to launch the game can be found in the main folder. 

## Controls
**WASD Keys** - Move Up, Down, Left, and Right.

**Arrow Keys** - Fire the Projectile in said direction.

**R Key** - Restarts the game.

**Enter/Return Key** - Pauses the game.

**Escape Key** - Exits the game.


## HUD Display
**Score** - Displays how many points the player has collected from enemies.

**High Score** - Displays the highest number of points collected in a round.

**Wave** - Displays the number of times the speed of the game has increased.

**Time** - Displays the current time of the 60-second timer. 

**Controls** - Listed out at the bottom of the screen.

## Enemy Types
- Mosquito - This enemy always targets the player and chases them with a health of 1.

- Beetle - This enemy is slow and only chases after grub left on the web. If a Beetle gets to a grub it will eat it causing the player to lose out on points. A Beetle has a health of 3. 

- Grenade Bug - This enemy moves in a straight line horizontally. Once it reaches the edge of the web it will move to the next row to move in whether it is up or down. The Grenade bug has a health of 1 and when shot, creates an explosion. This explosion has a radius for a brief moment and if any player or enemy is caught in this explosion they will be defeated. Enemies will drop grub when caught in an explosion while players will receive a game over. 

- Rocket Bug - This enemy can move in unpredictable patterns and is the fastest enemy out of all of them. The player should watch out for their sides to make sure not to get caught off guard by one.  

## Credits
- Programming and everything else done by me. 

- Textures for the bounding box, player, and enemies are all from the 1982 Atari arcade title Black Widow.

- Music is the Boss Theme from SEGA’S 1996 House of the Dead arcade title.
Credit to Cirno thanks for uploading the ripped audio to YouTube
https://www.youtube.com/watch?v=cqRwsw0K084

- Projectile SFX is the shooting sound from Konami’s 1987 NES port of Contra.
Credit to J-sinn on TheVGResource for ripping the audio 
https://www.sounds-resource.com/nes/contra/sound/3625/ 

- Collection SFX is the Wumpa Fruit sound from Naughty Dog’s 1996 PlayStation title Crash Bandicoot. 
Credit to RealRustyWalrus on YouTube for uploading the ripped audio.
https://www.youtube.com/watch?v=85MNpd2k1sU 
