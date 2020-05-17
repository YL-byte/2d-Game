from tkinter import *
from PIL import ImageTk, Image
import guiEventHandler as geh
from objects import Ground

class App(Frame):
    def __init__(self, master=Tk()):
        self.master = master
        Frame.__init__(self, master)
        master.title("My Game")

        #Main Frame for the game to take place in
        self.mainFrame = Frame(master, width=3000, height=700)
        self.mainFrame.focus_set()  # give keyboard focus to the label
        self.mainFrame.grid(column=0, row=1)

        #Set Keyboard Actions
        self.focus_set()

        #Quit Button
        # self.quitButton = Button(master, text="Quit", command=quit).grid(column=0, row=0,stick=W)
        #Stats
        self.hpLabel = Label(master, text="HP: ").grid(row=0, column=0,stick=W)
        self.hpLabelStats = Label(master, text="HP: ").grid(row=0, column=1, stick=W)
        self.manaLabel = Label(master, text="MP: ").grid(row=0, column=2, stick=W)
        self.manaLabelStats = Label(master, text="MP: ").grid(row=0, column=3, stick=W)

        #This is the map where the actual game takes place
        self.gameMap = App.Map(self.mainFrame)
        self.gameMap.grid(row=1, column=0, stick=W)
        #Needs to be last
        self.grid(row=0, column=0)
        self.controlledObject = None

    def bindKeyPress(self):

        self.mainFrame.bind("<Key>", lambda e: geh.keyDown(e, self.controlledObject))
        self.mainFrame.bind("<KeyRelease>", lambda e: geh.keyUp(e, self.controlledObject))

    class Map(Canvas):
        def __init__(self, master, width=1525, height=700, gravity=2):
            self.width = width
            self.height = height
            self.gravity = gravity
            Canvas.__init__(self, width=width, height=height, bg="grey")
            # self.map = Canvas(master, width=2000, height=500)
            self.mapLayout = []
            self.bind("<Button-1>", geh.mouseClick)
            self.objects = [] #All objects in the map
            self.groundPoints = []

        def setObjectOnTheMap(self, object):
            object.mapObject = self
            object_height = object.currentImage.height()
            map_width = int(self["width"])
            map_height = int(self["height"])
            object_x_pos_on_canvas = object.x
            object_y_pos_on_canvas = map_height - object_height - object.y
            # object.currentImage = object.stand
            object.canvasObject = self.create_image(object_x_pos_on_canvas, object_y_pos_on_canvas, image=object.currentImage, anchor=S)
            self.tag_bind(object.canvasObject, '<ButtonPress-1>', lambda e : geh.objectClick(e, object))

        def removeObject(self, object):
            self.delete(object.canvasObject)
            object.x = -1
            object.y = -1

        def createGround(self, x_start, x_stop, y_start, y_stop):
            self.create_line(x_start, y_start, x_stop, y_stop, fill="black")

            #Add the ground points to the list of ground points so when an object stands on the ground it wont fall
            for x in range(x_start, x_stop):
                if y_start < y_stop:
                    for y in range(y_start, y_stop):
                        self.groundPoints.append([x, y])
                        print ([x, y])

                else: #It is a straight line
                    self.groundPoints.append([x, y_start])
