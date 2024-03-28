HELLO USER,

To run the game, run the "game.py" file.

If that doesn't work, three things could be going wrong:
    1. You are not running the game.py py from the correct folder.
    (SOLUTION) To fix this, open the survive folder in Visual Studio Code (Or your preffered code editor) and run "game.py" from there
    2. You haven't installed python
    (Solution) Install python from https://www.python.org/downloads/
    3. (MOST COMMON) You have not installed the python module "arcade"
    (Solution)
        Step 1: Due to the arcade module needing MS Build Tools (which is very difficult to get working), install anaconda from https://www.anaconda.com/download if you haven't already 
        Step 2: Select anaconda as you python interpreter in your code editor
        Step 3: Install arcade using pip (NOT conda) with anaconda as your selected interpreter by typing this in your code editor's terminal: pip install arcade (conda doesn't work as it doesnt have arcade pre-installed on the default channels))
        Step 4: If pip doesn't work, you might need to install by visiting: https://pip.pypa.io/en/stable/installation (too see if you have installed pip, type: pip help (doesn't matter which terminal this is in))
        Step 4: If pip still doesn't work after installation, use this instead: python -m pip install arcade (Do this IN your code editor's terminal)
        INFO:
            Q: What is anaconda?
            A: Anaconda is a distribution of the Python programming language that aims to simplify package management and deployment. This helps us as it has MS Build Tools pre-installed

            Q: Why do I have to use pip to install arcade and not conda which I just installed?
            A: Anaconda doesn't have arcade pre-installed, so we need to get arcade with pip, but to get arcade we need MS Build Tools, which anaconda has, and that is why we need to select anaconda as our python interpreter

** CREDITS **

MUSIC
Fesliyan Studios: https://www.fesliyanstudios.com/

ITEM IMAGES
Link: https://opengameart.org/content/roguelikerpg-items
Twitter: https://twitter.com/joecreates

TREE IMAGE
https://opengameart.org/content/pine-tree-tiles

ROCK IMAGES
https://opengameart.org/content/various-stones-and-oregem-veins-16x16

ENEMY SPRITES
https://monopixelart.itch.io/skeletons-pack