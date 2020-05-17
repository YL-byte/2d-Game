from tkinter import *
from objects import Character, Ground, Item
from gui import App
from threadingController import *


app = App()
app.gameMap.createGround(0, app.gameMap.width, app.gameMap.height, app.gameMap.height)  # Create the ground
app.gameMap.createGround(0, 150, app.gameMap.height - 100, app.gameMap.height - 100)  # Create the ground
app.gameMap.createGround(150, 300, app.gameMap.height - 200, app.gameMap.height - 200)  # Create the ground
app.gameMap.createGround(300, 450, app.gameMap.height - 300, app.gameMap.height - 300)  # Create the ground
app.gameMap.createGround(450, 600, app.gameMap.height - 400, app.gameMap.height - 400)  # Create the ground


mainCharacter = Character(type="Character", name="myCharacter", x=50, y=500, mapObject=app.gameMap, objectAnimationDir="character_1/", standard_vel_x = 6)
app.controlledObject = mainCharacter
createObjectInGame(mainCharacter, app.gameMap)

monster1 = Character(type="Monster", name="monster1", x=500, y=500, mapObject=app.gameMap, characters_path="assets/monsters/", objectAnimationDir="monster_1/")
createObjectInGame(monster1, app.gameMap, isMoving=True, isInteractive=True, isAggressive=True)

monster2 = Character(type="Monster", name="monster2", x=1000, y=700, mapObject=app.gameMap, characters_path="assets/monsters/", objectAnimationDir="monster_1/")
createObjectInGame(monster2, app.gameMap, isMoving=True, isInteractive=True, isAggressive=True)

monster3 = Character(type="Monster", name="monster3", x=1300, y=700, mapObject=app.gameMap, characters_path="assets/monsters/", objectAnimationDir="monster_1/")
createObjectInGame(monster3, app.gameMap, isInteractive=True, isMoving=True, isAggressive=True)

app.controlledObject = mainCharacter
app.bindKeyPress()
app.mainloop()


