from threading import Thread
from time import sleep, perf_counter
import random

def createObjectInGame(object, map, isMoving=False, isInteractive=False, isAggressive=False):
    map.setObjectOnTheMap(object)
    blinkingThread = Thread(target=blinking, args=[object]).start()
    gravityThread = Thread(target=gravity, args=[object]).start()
    afterDamageThread = Thread(target=returnToNormalAfterDamage, args=[object]).start()
    if isMoving or isInteractive or isAggressive:
        randmonMovement = Thread(target=randomMovement, args=[object,isMoving, isInteractive, isAggressive]).start()

def blinking(object):
    map = object.mapObject
    blinkingCounter = 0
    while object.hitPoints > 0:
        if blinkingCounter > 0 and blinkingCounter % object.blinkInterval == 0 and object.currentImage == object.stand:
            # print (object.name, "blinked")
            object.currentImage = object.blink
            map.itemconfig(object.canvasObject, image=object.currentImage) #Change Image
            sleep(0.2)
            object.currentImage = object.stand
            map.itemconfig(object.canvasObject, image=object.currentImage)
            object.blinkInterval = random.randint(5, 7)
            blinkingCounter = 0
        else:
            blinkingCounter += 1
        sleep(0.5)

def gravity(object):
    map = object.mapObject
    while object.hitPoints > 0:
        map_height = int(map["height"])
        if [object.x, map_height - object.y] not in map.groundPoints: #"map_height - object.y" is used because the top of the map is 0
            object.canControlActions = False  # Object is falling
            if object.y_vel < 0:
                object.currentImage = object.jump
                map.itemconfig(object.canvasObject, image=object.currentImage)
            else:
                object.currentImage = object.fall
                map.itemconfig(object.canvasObject, image=object.currentImage)
            object.isFalling = True
            map = object.mapObject
            object_x_pos_on_canvas = object.x
            object_y_pos_on_canvas = map_height - object.y
            no_match_found = True
            object.walkInWidthBoundry()
            object.y_vel += map.gravity
            for check_y in range(object.y - object.y_vel, object.y):
                if [object.x, map_height - check_y] in map.groundPoints:
                    no_match_found = False
                    object.y_vel = 0
                    object.y = check_y
                    object_y_pos_on_canvas = map_height - object.y
                    map.coords(object.canvasObject, (object_x_pos_on_canvas, object_y_pos_on_canvas))  # change coordinates
                map.coords(object.canvasObject, (object_x_pos_on_canvas, object_y_pos_on_canvas))  # change coordinates

            if no_match_found:
                # object.y_vel += map.gravity
                object.y -= object.y_vel
                map.coords(object.canvasObject, (object_x_pos_on_canvas, object_y_pos_on_canvas))  # change coordinates

        elif object.isFalling: #This sequence runs just when object stops falling
            object_y_pos_on_canvas = map_height - object.y
            map.coords(object.canvasObject, (object_x_pos_on_canvas, object_y_pos_on_canvas))  # change coordinates
            object.isFalling = False #Stooped Falling
            object.canControlActions = True  # Stopped Falling
            object.y_vel = 0 #Stopped moving in the Y Direction
            object.x_vel = 0 #Stopped moving in the X Direction
            if object.y < 0:
                object.y = 0
            object.currentImage = object.stand
            map.itemconfig(object.canvasObject, image=object.currentImage)

        sleep(0.03)

def randomMovement(object, isMoving=False, isInteractive=False, isAggressive=False):
    map = object.mapObject
    map_width =  int(map["width"])
    counter = 0
    threshold = random.randint(10, 20) * 2
    random_number = random.randint(2, 7)
    is_walking_right = random.randint(0, 1)
    while object.hitPoints > 0:

        #If enemy can attack character => attack
        if object.closeToAttack() and isAggressive and object.canAttack:
            print (object.name, "Attacked")
            object.simpleAttack(damage=1)
            Thread(target=monsterAttackCoolDown, args=[object]).start()

        #If character in line of sight of character => Run towards character
        elif object.spotCharacter() and isInteractive:
            vel_x = object.standard_vel_x * 2
            object.isSearching = True
            print (object.name, "Spotted Something and is walking towards it")
            if object.isLookingRight:
                object.walkRight()
            else:
                object.walkLeft()

        #Object reached left edge, move right
        elif object.x == 0 and isMoving and object.canControlActions:
            object.walkRight()
            counter = 0
            is_walking_right = 1

        #Object reached right edge, move left
        elif object.x == map_width and isMoving and object.canControlActions:
            object.walkLeft()
            counter = 0
            is_walking_right = 0

        #If object in boundry and he cant attack a character or he didn't spot one, wonder around
        elif object.canControlActions and isMoving and  counter < threshold:
            if is_walking_right == 1:
                object.walkRight()
                counter += 1
            else:
                object.walkLeft()
                counter += 1

        else:
            object.stopWalkingAnimation()
            sleep(random_number / 10)
            counter = 0
            threshold = random.randint(10, 20) * 2
            random_number = random.randint(2, 7)
            is_walking_right = random.randint(0, 1)

        sleep(0.03)

def takeDamage(object, damageTaken):
    map = object.mapObject
    object.hitPoints -= damageTaken

    #Object is Dead
    if object.hitPoints <= 0:
        print (object.name, "IS Dead")
        map.removeObject(object)
        object.canControlActions = False

    else:
        map_height = int(map["height"])
        map_width =  int(map["width"])
        object.canControlActions = False
        print (object.name, "Took damage", "Current Hit Points", object.hitPoints)
        object.currentImage = object.damage
        map.itemconfig(object.canvasObject, image=object.currentImage)


def returnToNormalAfterDamage(object):
    while object.hitPoints > 0:
        if object.currentImage == object.damage:
            sleep(0.5)
            object.canControlActions = True
            map = object.mapObject
            object.currentImage = object.stand
            map.itemconfig(object.canvasObject, image=object.currentImage)
        sleep(0.03)

def monsterAttackCoolDown(object): #So a monster won't attack forever
    map = object.mapObject
    print (object.name, "Can't Attack")
    object.canAttack = False
    object.currentImage = object.stand
    map.itemconfig(object.canvasObject, image=object.currentImage)
    sleep(1)
    object.canAttack = True
    print (object.name, "Can Attack")

def iceSpellThread(object, spellObject):
    map = object.mapObject
    # Set map height on canvas
    map_height = int(map["height"])
    spellObject.y += 100
    spell_y_location = map_height - spellObject.y

    map.setObjectOnTheMap(spellObject)
    map.coords(spellObject.canvasObject, (spellObject.x, spell_y_location))
    sleep(0.2)
    objectMetGround = False
    while not objectMetGround:
        #Set Vel and Acc for current drop
        spellObject.vel_y -= spellObject.acc_y
        spellObject.y -= spellObject.vel_y

        #If spell object will meet the ground during fall, End sequence
        for check_y in range(spellObject.y - spellObject.vel_y, spellObject.y):
            check_y_canvas_location = map_height - check_y
            if [spellObject.x, check_y_canvas_location] in map.groundPoints:
                objectMetGround = True
                spellObject.y = check_y

        spell_y_location = map_height - spellObject.y
        map.coords(spellObject.canvasObject, (spellObject.x, spell_y_location))
        sleep(0.03)
    map.itemconfig(spellObject.canvasObject, image=spellObject.endOfSpell)
    for check_x in range (spellObject.x - spellObject.damage_radius, spellObject.x + spellObject.damage_radius):
        for check_y in range(spellObject.y - spellObject.damage_radius, spellObject.y + spellObject.damage_radius):
            for object in map.objects:
                if [check_x, check_y] == [object.x, object.y]:
                    print (object.name, "Hit By Ice Spell", object.x, object.y)
                    Thread(target=takeDamage, args=[object, spellObject.damage]).run()

    sleep(0.5)
    map.removeObject(spellObject)
