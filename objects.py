import random
from PIL import ImageTk, Image
import tkinter as tk
from time import sleep
from threading import Thread
from threadingController import takeDamage

class Item:
    def __init__(self, name=None):
        self.name = name

class Ground:
    def __init__(self, x_start, x_stop, y_start, y_stop):
        self.x_start = x_start
        self.x_stop = x_stop
        self.y_start = y_start
        self.y_stop = y_stop

class Character:
    def __init__(self, type=None, name=None, hitPoints=10, manaPoints=0, x=0, y=0, z=0, x_vel=0, y_vel=0, z_vel=0,
                 standard_vel_x = 5, standard_vel_y=30,
                 inventory=[], strength=8, intelligence=8, charisma=8, dexterity=8, attack=0, defense=0,
                 characters_path="assets/characters/",
                 currentImage=None, objectAnimationDir = None, #object animation dir conatins the objects images
                 stand="stand.png", blink="blink.png", duck = "duck.png", jump="jump.png", fall="fall.png", spell="spell.png",
                 damage="damage.png", shock="shock.png",
                 walk1="walk1.png", walk2="walk2.png", walk3="walk3.png", walk4="walk4.png",
                 attack1="attack1.png", attack2="attack2.png", attack3="attack3.png", attack4="attack4.png",
                 defense1="defense1.png", defense2="defense2.png", defense3="defense3.png", defense4="defense4.png",
                 mapObject=None):

        #Plot related Variables
        self.name = name
        self.type = type

        self.attack = attack
        self.defense = defense
        self.attack_range = 100 #Distance in pixels in which the attack is effective
        self.sight_range = 500 #Distance in pixels in which a character can see
        self.canAttack = True #A monster has a cooldown of about 1 sec between attacks
        self.isSearching = False #If a monster is searching it will look for the objecrs until it gives up

        #Location and velocity Information
        self.mapObject = mapObject #Which map is the character in
        self.mapObject.objects.append(self) #Add this object to the appropriate map list of objects
        self.canvasObject = None #This is the canbasObject the character will be in
        self.isLookingRight = True #If looking left then False
        self.x = x
        self.y = y
        self.z = z
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.z_vel = z_vel
        self.standard_vel_x = standard_vel_x
        self.standard_vel_y = standard_vel_y
        self.canControlActions = True #False if player is in jump sequence or falling or ducking
        self.isFalling = False

        #Game Stats
        self.hitPoints = hitPoints
        self.manaPoints = manaPoints
        self.maxHitPoints = hitPoints
        self.maxManaPoints = manaPoints
        self.strength = strength
        self.intelligence = intelligence
        self.charisma = charisma
        self.dexterity = dexterity

        self.spells = {}
        self.inventory = inventory

        #Animation Information for activities
        self.characters_path =characters_path
        self.animationPath = self.characters_path + objectAnimationDir
        self.blinkInterval = random.randint(3, 8)
        self.animationDir = {
            "stand":stand, "blink":blink, "duck":duck, "jump": jump, "fall": fall, "spell": spell,
            "shock": shock, "damage": damage,
            "walk1":walk1, "walk2":walk2, "walk3":walk3, "walk4":walk4,
            "attack1":attack1, "attack2":attack2, "attack3":attack3, "attack4":attack4,
            "defense1":defense1, "defense2":defense2, "defense3":defense3, "defense4":defense4
        }
        self.flipAllObjectsImages()
        self.animationCounter = 0 #Counter for animation to go smoother
        self.animationCounterThreshold = 5

        #Internal Information
        if self.__class__ == Character:
            self.id = Character.id
            Character.allCharacters.append(self)
            Character.id += 1
    id = 0
    allCharacters = []

    #Objects Functions
    def walkingAnimation(self):
        if self.canControlActions:
            if (self.currentImage == self.stand or self.currentImage == self.blink):
                self.currentImage = self.walk1
                self.mapObject.itemconfig(self.canvasObject, image=self.currentImage)
                self.animationCounter = 0

            elif self.animationCounter < self.animationCounterThreshold:
                self.animationCounter += 1

            elif self.currentImage == self.walk1:
                self.currentImage = self.walk2
                self.mapObject.itemconfig(self.canvasObject, image=self.currentImage)
                self.animationCounter = 0

            elif self.currentImage == self.walk2:
                self.currentImage = self.walk3
                self.mapObject.itemconfig(self.canvasObject, image=self.currentImage)
                self.animationCounter = 0

            elif self.currentImage == self.walk3:
                self.currentImage = self.walk4
                self.mapObject.itemconfig(self.canvasObject, image=self.currentImage)
                self.animationCounter = 0

            elif self.currentImage == self.walk4:
                self.currentImage = self.walk1
                self.mapObject.itemconfig(self.canvasObject, image=self.currentImage)
                self.animationCounter = 0

    def closeToAttack(self):
        if self.canControlActions:
            checked_y = self.y

            if self.isLookingRight:
                for checked_x in range(self.x, self.x + self.attack_range):
                    object = self.getObjectFromCoor(checked_x, checked_y)#Returns object if spotted; returns None if no object found
                    if object != None:
                        if object.type != self.type:
                            return True
            else:
                for checked_x in range(self.x - self.attack_range, self.x):
                    object = self.getObjectFromCoor(checked_x, checked_y)#Returns object if spotted; returns None if no object found
                    if object != None:
                        if object.type != self.type:
                            return True

        return False

    def spotCharacter(self):
        if self.canControlActions:
            checked_y = self.y
            if self.isLookingRight:
                for checked_x in range(self.x, self.x + self.sight_range):
                    object = self.getObjectFromCoor(checked_x, checked_y) #Returns object if spotted; returns None if no object found
                    if object != None:
                        if object.type != self.type and object.x != self.x:
                            return True
            else:
                for checked_x in range(self.x - self.sight_range, self.x):
                    object = self.getObjectFromCoor(checked_x, checked_y)#Returns object if spotted; returns None if no object found
                    if object != None:
                        if object.type != self.type and object.x != self.x:
                            return True

        return False

    def simpleAttack(self, damage=1):
        if self.canControlActions:
            map = self.mapObject
            self.currentImage = self.attack1
            map.itemconfig(self.canvasObject, image=self.currentImage)
            checked_y = self.y
            sleep(0.05)
            if self.isLookingRight:
                for checked_x in range(self.x, self.x + self.attack_range):
                    object = self.getObjectFromCoor(checked_x, checked_y)
                    if object!= None:
                        Thread(target=takeDamage, args=[object, 1]).run()

            else:
                for checked_x in range(self.x - self.attack_range, self.x):
                    object = self.getObjectFromCoor(checked_x, checked_y)
                    if object!= None:
                        Thread(target=takeDamage, args=[object, 1]).run()

    def getObjectFromCoor(self, checked_x, checked_y):
        map = self.mapObject
        for object in map.objects:
            if object.x == checked_x and object.y == checked_y and self != object:
                return object
        return None

        # self.currentImage = self.stand
        # map.itemconfig(self.canvasObject, image=self.currentImage)

    def walkLeft(self):
        # objectwidth = self.stand.width()
        # object_height = self.stand.height()
        # map_width = int(self.mapObject["width"])
        map_height = int(self.mapObject["height"])
        object_x_pos_on_canvas = self.x
        object_y_pos_on_canvas = map_height - self.y

        if (self.canControlActions):
            self.x_vel = -1 * self.standard_vel_x
            if self.isLookingRight:
                self.isLookingRight = False
                self.flipAllObjectsImages(flipRight=False)
            self.walkInWidthBoundry()
            self.mapObject.coords(self.canvasObject, (object_x_pos_on_canvas, object_y_pos_on_canvas))  # change coordinates
            self.walkingAnimation()

    def walkRight(self):
        # objectwidth = self.stand.width()
        # object_height = self.stand.height()
        # map_width = int(self.mapObject["width"])
        map_height = int(self.mapObject["height"])
        object_x_pos_on_canvas = self.x
        object_y_pos_on_canvas = map_height - self.y

        if self.canControlActions:
            self.x_vel = self.standard_vel_x
            if not self.isLookingRight: #If player is looking Left
                self.isLookingRight = True
                self.flipAllObjectsImages(flipRight=True)
            self.walkInWidthBoundry()
            self.mapObject.coords(self.canvasObject, (object_x_pos_on_canvas, object_y_pos_on_canvas))  # change coordinates
            self.walkingAnimation()

    def walkInWidthBoundry(self):
        map_width = int(self.mapObject["width"])
        self_width = self.stand.width()

        if self.x + self.x_vel in range(0, map_width):
            self.x += self.x_vel

        elif self.x < map_width - self.x:
            self.x = 0

        else:
            self.x = map_width - 1

    def stopWalkingAnimation(self):
        self.currentImage = self.stand
        self.mapObject.itemconfig(self.canvasObject, image=self.currentImage)
        self.animationCounter = 0

    def duckAnimation(self):
        self.currentImage = self.duck
        self.mapObject.itemconfig(self.canvasObject, image=self.currentImage)
        self.animationCounter = 0
        self.canControlActions = False

    def stopDuckAnimation(self):
        self.canControlActions = True

    def flipAllObjectsImages(self, flipRight=True):
        if flipRight == True:
            # print (self.name, "is looking Right")

            self.stand = ImageTk.PhotoImage(Image.open(self.animationPath + self.animationDir["stand"]))
            self.currentImage = self.stand
            self.blink = ImageTk.PhotoImage(Image.open(self.animationPath + self.animationDir["blink"]))
            self.duck = ImageTk.PhotoImage(Image.open(self.animationPath + self.animationDir["duck"]))
            self.jump = ImageTk.PhotoImage(Image.open(self.animationPath + self.animationDir["jump"]))
            self.fall = ImageTk.PhotoImage(Image.open(self.animationPath + self.animationDir["fall"]))
            self.spell = ImageTk.PhotoImage(Image.open(self.animationPath + self.animationDir["spell"]))
            self.shock = ImageTk.PhotoImage(Image.open(self.animationPath + self.animationDir["shock"]))
            self.damage = ImageTk.PhotoImage(Image.open(self.animationPath + self.animationDir["damage"]))

            self.walk1 = ImageTk.PhotoImage(Image.open(self.animationPath + self.animationDir["walk1"]))
            self.walk2 = ImageTk.PhotoImage(Image.open(self.animationPath + self.animationDir["walk2"]))
            self.walk3 = ImageTk.PhotoImage(Image.open(self.animationPath + self.animationDir["walk3"]))
            self.walk4 = ImageTk.PhotoImage(Image.open(self.animationPath + self.animationDir["walk4"]))
            self.attack1 = ImageTk.PhotoImage(Image.open(self.animationPath + self.animationDir["attack1"]))
            self.attack2 = ImageTk.PhotoImage(Image.open(self.animationPath + self.animationDir["attack2"]))
            self.attack3 = ImageTk.PhotoImage(Image.open(self.animationPath + self.animationDir["attack3"]))
            self.attack4 = ImageTk.PhotoImage(Image.open(self.animationPath + self.animationDir["attack4"]))
            self.defense1 = ImageTk.PhotoImage(Image.open(self.animationPath + self.animationDir["defense1"]))
            self.defense2 = ImageTk.PhotoImage(Image.open(self.animationPath + self.animationDir["defense2"]))
            self.defense3 = ImageTk.PhotoImage(Image.open(self.animationPath + self.animationDir["defense3"]))
            self.defense4 = ImageTk.PhotoImage(Image.open(self.animationPath + self.animationDir["defense4"]))

        else:
            # print (self.name, "is looking Left")

            self.stand = ImageTk.PhotoImage(Image.open(self.animationPath + self.animationDir["stand"]).transpose(Image.FLIP_LEFT_RIGHT))
            self.currentImage = self.stand
            self.blink = ImageTk.PhotoImage(Image.open(self.animationPath + self.animationDir["blink"]).transpose(Image.FLIP_LEFT_RIGHT))
            self.duck = ImageTk.PhotoImage(Image.open(self.animationPath + self.animationDir["duck"]).transpose(Image.FLIP_LEFT_RIGHT))
            self.jump = ImageTk.PhotoImage(Image.open(self.animationPath + self.animationDir["jump"]).transpose(Image.FLIP_LEFT_RIGHT))
            self.spell = ImageTk.PhotoImage(Image.open(self.animationPath + self.animationDir["spell"]).transpose(Image.FLIP_LEFT_RIGHT))
            self.shock = ImageTk.PhotoImage(Image.open(self.animationPath + self.animationDir["shock"]).transpose(Image.FLIP_LEFT_RIGHT))
            self.damage = ImageTk.PhotoImage(Image.open(self.animationPath + self.animationDir["damage"]).transpose(Image.FLIP_LEFT_RIGHT))
            self.fall = ImageTk.PhotoImage(Image.open(self.animationPath + self.animationDir["fall"]).transpose(Image.FLIP_LEFT_RIGHT))
            self.walk1 = ImageTk.PhotoImage(Image.open(self.animationPath + self.animationDir["walk1"]).transpose(Image.FLIP_LEFT_RIGHT))
            self.walk2 = ImageTk.PhotoImage(Image.open(self.animationPath + self.animationDir["walk2"]).transpose(Image.FLIP_LEFT_RIGHT))
            self.walk3 = ImageTk.PhotoImage(Image.open(self.animationPath + self.animationDir["walk3"]).transpose(Image.FLIP_LEFT_RIGHT))
            self.walk4 = ImageTk.PhotoImage(Image.open(self.animationPath + self.animationDir["walk4"]).transpose(Image.FLIP_LEFT_RIGHT))
            self.attack1 = ImageTk.PhotoImage(Image.open(self.animationPath + self.animationDir["attack1"]).transpose(Image.FLIP_LEFT_RIGHT))
            self.attack2 = ImageTk.PhotoImage(Image.open(self.animationPath + self.animationDir["attack2"]).transpose(Image.FLIP_LEFT_RIGHT))
            self.attack3 = ImageTk.PhotoImage(Image.open(self.animationPath + self.animationDir["attack3"]).transpose(Image.FLIP_LEFT_RIGHT))
            self.attack4 = ImageTk.PhotoImage(Image.open(self.animationPath + self.animationDir["attack4"]).transpose(Image.FLIP_LEFT_RIGHT))
            self.defense1 = ImageTk.PhotoImage(Image.open(self.animationPath + self.animationDir["defense1"]).transpose(Image.FLIP_LEFT_RIGHT))
            self.defense2 = ImageTk.PhotoImage(Image.open(self.animationPath + self.animationDir["defense2"]).transpose(Image.FLIP_LEFT_RIGHT))
            self.defense3 = ImageTk.PhotoImage(Image.open(self.animationPath + self.animationDir["defense3"]).transpose(Image.FLIP_LEFT_RIGHT))
            self.defense4 = ImageTk.PhotoImage(Image.open(self.animationPath + self.animationDir["defense4"]).transpose(Image.FLIP_LEFT_RIGHT))

    def iceSpell(self):
        spellObject = Spell(castingObject=self)

class Spell:
    def __init__(self, castingObject=None, name=None, type=None, damage=1, damage_radius=0, duration=1,
                x=0, y=0, vel_x=0, vel_y=0, acc_x=0, acc_y=0,
                specificAnimationPath=None,
                mapObject=None
                ):

        self.castingObject = castingObject
        self.name = name
        self.type = type #Fire, Ice, Earth, Water
        self.damage = damage
        self.duration = duration
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.acc_x = acc_x
        self.acc_y = acc_y
        self.damage_radius = damage_radius
        self.mapObject = castingObject.mapObject
        self.middleOfSpell = ImageTk.PhotoImage(Image.open(Spell.animationPath + specificAnimationPath + "//middleOfSpell.png"))
        self.endOfSpell = ImageTk.PhotoImage(Image.open(Spell.animationPath + specificAnimationPath + "//endOfSpell.png"))
        self.currentImage = self.middleOfSpell
        self.mapObject = mapObject
        self.canvasObject = None
    animationPath="assets/spells/"