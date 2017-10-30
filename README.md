BOMBERMAN GAME:

How to run the game:
	You can run the game by using python3 command on 'bomberman.py' file i.e. on running the command 'python3 bomberman.py' , the game will start.

Controls : 

	Move left	: a
	Move right	: d
	Move up		: w
	Move down	: s
	Drop bomb 	: b
	Quit game 	: q

Specifications Of The Game:

# Game consists of the 1 Bomberman and many Enemies. 
# Bomberman has to kill all the enemies on a level to complete a given level.
# Enemies or Bomberman are killed if they are caught up in an explosion.
# Bomberman also loses his life if he collides with the enemy.
# Only one bomb can be placed at a given time.
# Bomberman gets a score of +100 on killing an enemy and a score of +20 on breaking a brick by a bomb.
# Bomberman has 3 lives to play.
# The game is terminated if the bomberman loses his three lives or the user presses the key 'q'
# There are 3 levels in the game and the bomberman is upgraded to the next level if he kills all his enemies in that level.
# The difficulty of the game increases with each level.

Symbols for the game :
	Walls 			: X
	Bricks 			: /
	Bomberman 		: B
	Enemy 			: E
	Explosion 		: e

Features implemented :
# INHERITANCE : There is good use of inheritance. Enemy as well as the bomberman inherit their movement functions from the person class.

# POLYMORPHISM : The use of polymorphism has been done to print board according to current state of the game.

# MODULARITY : The entire game has been build in a modular fashion. Most of the activites have their own dedicated functions which make the code modular and easy to understand.

# ENCAPSULATION : Encapsulation has been used to present many methods in various classes which are integral to the functioning of the game.

