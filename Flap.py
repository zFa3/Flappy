#!usr/bin/env python3
import tkinter as tk
import random as rd
import time as tm


root = tk.Tk()
side_length = 500 # in pixels
root.geometry(f"{side_length}x{side_length}")
gameCanvas = tk.Canvas(root, width=side_length, height=side_length)
FPS = 20

############################# Bird #############################

# angle is determinated from the speed
# Bird Y location, Vertical velocity
bird = [side_length//2, 0]

# pixels
birdRadius = 25

# color in hexadecimal format(hex)
birdColor = "#FDFD00"

# recommended around 0.95
gravity = 0.97
# the lower the number
# the more "floaty"
floatiness = 0.2
############################# Pipes #############################

# higher is faster
pipeSpeed = 5

# measured in pixels
pipeWidth = 75

# hexadecimal format
pipeColor = "#00FF00"
pipeMouthColor = "#00AF00"


# Additional Height - Added on to pipe height
pipeMouthHeight = 15
# additional width - Added onto the pipe width
pipeMouthWidth = 5


# the properties of all the pipes
#list = [ pipe x coordinate, height, top or bottom (true or false) ]
pipes = [[50, 50, True], [50, 50, False]]

##################################################################

def click(event):
    global bird
    bird[1] = birdRadius

def gameloop():
    global pipes
    while 1:
        tm.sleep(1/FPS)
        remove = False
        draw()
        for i in range(len(pipes)):
            if not pipes[i][0] < 0:
                pipes[i] = [pipes[i][0] - pipeSpeed, pipes[i][1], pipes[i][2]]
            else:
                remove = True
        if remove:
            pipes.pop(0)
        if len(pipes) < 2:
            seed1 = rd.randint(0, int(side_length*5/8))
            seed2 = rd.randint(0, 1)
            pipes.append([side_length, seed1 - birdRadius * 4, seed2])
            pipes.append([side_length, side_length - (seed1), not seed2])
        bird[0] = bird[0] * (2 - gravity)
        bird[0] -= bird[1]
        bird[1] *= (gravity - floatiness)
        if bird[0] + birdRadius < 0 or bird[0] - birdRadius > side_length:
            print("GAME OVER")

def draw(): # draws image to canvas every frame
    gameCanvas.delete("all")

    for i in pipes:
        # if the pipe is located
        #  on the top or bottom
        # of the screen
        if i[2]:
            gameCanvas.create_rectangle(i[0], 0, i[0] + pipeWidth, i[1], fill = pipeColor, outline = '')
            gameCanvas.create_rectangle(i[0] - pipeMouthWidth, i[1], i[0] + pipeWidth + pipeMouthWidth, i[1] + pipeMouthHeight, fill = pipeMouthColor, outline = '')
        else:
            gameCanvas.create_rectangle(i[0], side_length, i[0] + pipeWidth, side_length - i[1], fill = pipeColor, outline = '')
            gameCanvas.create_rectangle(i[0] - pipeMouthWidth, side_length - i[1], i[0] + pipeWidth + pipeMouthWidth, side_length - i[1] - pipeMouthHeight, fill = pipeMouthColor, outline = '')

    gameCanvas.create_oval(15 - birdRadius//2, bird[0] - birdRadius//2, 15 + birdRadius//2, bird[0] + birdRadius//2, fill = birdColor)

    gameCanvas.update()
    gameCanvas.pack()

root.bind("<Button-1>", click)
draw()
gameloop()
root.mainloop()
