from time import sleep
from threading import Thread
from objects import Spell
from threadingController import *

#If key is pressed it will be True, else it will be False
keysPressed = {'a': False, 'b': False, 'c': False, 'd': False, 'e': False, 'f': False, 'g': False, 'h': False, 'i': False,
'j': False, 'k': False, 'l': False, 'm': False, 'n': False, 'o': False, 'p': False, 'q': False, 'r': False, 's': False,
't': False, 'u': False, 'v': False, 'w': False, 'x': False, 'y': False, 'z': False
}

def keyUp(e, object):
    map = object.mapObject
    print ('up', e.char)
    object.stopWalkingAnimation()
    if e.char == "s" or e.char == 'S':
        keysPressed['s'] = False
        object.stopDuckAnimation()

    elif e.char == "d" or e.char == 'D' or e.char == "a" or e.char == 'A':
        keysPressed[e.char] = False
        if object.canControlActions:
            object.x_vel = 0

    else:
        keysPressed[e.char] = False

def keyDown(e, object):
    map = object.mapObject
    objectwidth = object.stand.width()
    object_height = object.stand.height()
    map_width = int(map["width"])
    map_height = int(map["height"])
    object_x_pos_on_canvas = object.x
    object_y_pos_on_canvas = map_height - object.y

    #Movement Keys
    if (e.char == "d" or e.char == "D") and object.canControlActions:
        keysPressed[e.char] = True
        object.x_vel = object.standard_vel_x
        object.walkRight()

    elif (e.char == "a" or e.char == "A") and object.canControlActions:
        keysPressed[e.char] = True
        object.walkLeft()

    elif (e.char == "w" or e.char == "W") and object.canControlActions:
        keysPressed[e.char] = True
        object.canControlActions = False
        object.currentImage = object.jump
        map.itemconfig(object.canvasObject, image=object.currentImage)
        object.y_vel = -1 * object.standard_vel_y
        object.y += 1
        print ("Jump", "X Vel", object.x_vel, "Y Vel", object.y_vel)
        map.coords(object.canvasObject, (object_x_pos_on_canvas, object_y_pos_on_canvas))  # change coordinates
        sleep(0.01)

    elif (e.char == "s" or e.char == "S") and object.canControlActions:
        keysPressed[e.char] = True
        object.duckAnimation()

    #Action Keys

    #ICE SPELL
    elif (e.char == "c" or e.char == "C") and keysPressed[e.char] == False and object.x_vel == 0 and object.y_vel == 0 and object.canControlActions:
        keysPressed[e.char] = True
        print ("Ice Spell")
        #Set object's image as casting image
        object.currentImage = object.spell
        map.itemconfig(object.canvasObject, image=object.currentImage)

        #If object is facing right, spell will happen to the object's right; else, to his left
        if object.isLookingRight:
            spell_x_location = object.x + 100
        else:
            spell_x_location = object.x - 100

        spell_y_location = object.y + 50
        #Create spell object
        spellObject = Spell(
            damage=2, damage_radius=50,
            castingObject=object, specificAnimationPath="iceSpell",
            x=spell_x_location, y=spell_y_location, acc_y=-1,
            mapObject=map
        )

        #Start spell sequence
        Thread(target=iceSpellThread, args=[object, spellObject]).start()

    elif (e.char == 'z' or e.char == 'Z') and object.x_vel == 0 and object.y_vel == 0 and object.canControlActions:
        keysPressed[e.char] = True
        print (object.name, "Attacked")
        object.simpleAttack()

    else:
        print ('down', e.char)
        keysPressed[e.char] = True

def mouseClick(e):
    print("X:", e.x, "Y:", e.y)

def objectClick(e, object):
    print (object.name, "Clicked at", e.x, e.y)
    print ("OBJECT HEIGHT", object.y)