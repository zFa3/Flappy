#!usr/bin/env python3
import tkinter as tk
import random as rd
import time as tm


root = tk.Tk()
side_length = 500 # in pixels
root.geometry(f"{side_length}x{side_length}")
gameCanvas = tk.Canvas(root, width=side_length, height=side_length)

FPS = 20
gameOver = False
score = 0

############################# Bird #############################

# angle is determinated from the speed
# Bird Y location, Vertical velocity
bird = [side_length//2, 0]
birdX = 50
# pixels
birdRadius = 25

# color in hexadecimal format(hex)
birdColor = "#FDFD00"

# Recommended around 0.95
gravity = 0.97
# Lower the number, higher the "floatiness"
floatiness = 0.2
############################# Pipes #############################

# higher is faster
pipeSpeed = 10

# measured in pixels
pipeWidth = 75

# hexadecimal format
pipeColor = "#00FF00"
pipeMouthColor = "#00AF00"


# Additional Height - Added on to pipe height
pipeMouthHeight = 15
# additional width - Added onto the pipe width
pipeMouthWidth = 5

# how many birds tall is the gap
pipeGap = 6
# the properties of all the pipes
#list = [ pipe x coordinate, height, top or bottom (true or false) ]
pipes = [[50, 50, True], [50, 50, False]]

##################################################################

def click(event):
    global bird
    bird[1] = birdRadius * 1.25

def gameloop():
    global pipes, score, gameOver
    while not gameOver:
        tm.sleep(1/FPS)
        remove = False; draw()
        for i in range(len(pipes)):
            if not pipes[i][0] < 0:
                pipes[i] = [pipes[i][0] - pipeSpeed, pipes[i][1], pipes[i][2]]
            else:
                remove = True
        if remove:
            pipes.pop(0)
            score += 1
        if len(pipes) < 2:
            seed1 = rd.randint(pipeGap//2 * birdRadius + 50, int(side_length*5/8))
            seed2 = rd.randint(0, 1)
            pipes.append([side_length, seed1 - birdRadius * pipeGap, seed2])
            pipes.append([side_length, side_length - (seed1), not seed2])
        bird[0] += gravity * (FPS/2)
        bird[0] -= bird[1]
        bird[1] *= (gravity - floatiness)
        if bird[0] - birdRadius < 0 or bird[0] + birdRadius > side_length or ((bird[0] + birdRadius > abs(side_length - (list(sorted([(item[0], item[1]) for item in pipes if not item[2]], key = lambda x:x[0])))[0][1])) and birdX > (list(sorted([item[0] for item in pipes if not item[2]])))[0]) or\
            ((bird[0] - birdRadius < (list(sorted([(item[0], item[1]) for item in pipes if item[2]], key = lambda x:x[0])))[0][1])) and birdX > (list(sorted([item[0] for item in pipes if item[2]])))[0]:
            print(f"You got a score of: {score}")
            gameOver = True; draw()
            tm.sleep(1.5)
            root.destroy()

def draw(): # draws image to canvas every frame
    gameCanvas.delete("all")

    for i in pipes:
        # if the pipe is located
        #  on the top or bottom
        # of the screen
        if i[2]:
            # top pipes
            gameCanvas.create_rectangle(i[0], 0, i[0] + pipeWidth, i[1], fill = pipeColor)
            gameCanvas.create_rectangle(i[0] - pipeMouthWidth, i[1], i[0] + pipeWidth + pipeMouthWidth, i[1] + pipeMouthHeight, fill = pipeMouthColor)
        else:
            gameCanvas.create_rectangle(i[0], side_length, i[0] + pipeWidth, side_length - i[1], fill = pipeColor)
            gameCanvas.create_rectangle(i[0] - pipeMouthWidth, side_length - i[1], i[0] + pipeWidth + pipeMouthWidth, side_length - i[1] - pipeMouthHeight, fill = pipeMouthColor)

    gameCanvas.create_oval(birdX - birdRadius//2, bird[0] - birdRadius//2, birdX + birdRadius//2, bird[0] + birdRadius//2, fill = birdColor)

    gameCanvas.update()
    gameCanvas.pack()

root.bind("<Button-1>", click)
root.bind("<space>", click)

draw()
gameloop()
root.mainloop()
