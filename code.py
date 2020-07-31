import cv2
import numpy as np
import random as rd
import sys

# *---------------------------------Config area---------------------------------*

softness = 9  # How Many times the softness code will run (More doesnt mean better)
structures = True
seeds = None  # The Gen Seed (None = Random)
GenType = 5  # 5 - Archipelago / 6 - Continent

# *-----------------------------------------------------------------------------*

img_width = 1000
img_height = 1000
xpw, xfw, ypw, yfw = 0, 1, 0, 1  # Water pixel jump
xpi, xfi, ypi, yfi = 0, 10, 0, 10  # Island pixel jump
rd.seed(seeds)
print("Seed is: " + str(seeds))

blank_image = np.zeros((img_width, img_height, 3), np.uint8)
# B,G,R
blue = (255, 0, 1)
green = (1, 240, 1)
yellow = (1, 255, 160)
red = (1, 1, 255)

matriz_water = np.ones((img_width, img_height), dtype=object)  # 1000 x 1000
matriz_island = np.zeros((int(img_width/10), int(img_height/10)), dtype=object)  # 100 x 100

print("Generating Islands Noises...")
IslandX = img_width / (img_width/100)
IslandY = img_height / (img_width/100)
for x in range(int(IslandX)):
    for y in range(int(IslandY)):
        if 1 < x < (IslandX - 1) and 1 < y < (IslandY - 1):
            if rd.randint(0, 100) < 50:
                matriz_island[x][y] = 1
        else:
            matriz_island[x][y] = 0

print("Generating Sand...")
for s in range(softness):
    for x in range(int(IslandX)):
        for y in range(int(IslandY)):
            if 1 < x < (IslandX-1) and 1 < y < (IslandY-1):
                adj_isl = 0
                adj_wat = 0
                for xx in range(-1, 2):
                    for yy in range(-1, 2):
                        if (matriz_island[x + xx][y + yy] == 1) and (matriz_island[x][y] == 0):
                            adj_wat += 1
                        if (matriz_island[x + xx][y + yy] == 0) and (matriz_island[x][y] == 1):
                            adj_isl += 1
                if adj_wat >= 5:
                    matriz_island[x][y] = 1
                if adj_isl >= GenType:
                    matriz_island[x][y] = 0

print("Generating Grass...")
for x in range(int(IslandX)):
    for y in range(int(IslandY)):
        if 1 < x < (IslandX-1) and 1 < y < (IslandY-1) and (matriz_island[x][y] == 1):
            adj_isl = 0
            for xx in range(-1, 2):
                for yy in range(-1, 2):
                    if matriz_island[x + xx][y + yy] == 1:
                        adj_isl += 1
            if adj_isl >= 5:
                matriz_island[x][y] = 2

if structures:
    print("Generating Structures...")
    for x in range(int(IslandX)):
        for y in range(int(IslandY)):
            if 1 < x < (IslandX-1) and 1 < y < (IslandY-1) and (matriz_island[x][y] == 2):
                adj_isl = 0
                for xx in range(-1, 2):
                    for yy in range(-1, 2):
                        if matriz_island[x + xx][y + yy] == 2:
                            adj_isl += 1
                if adj_isl >= 8:
                    if rd.randint(0, 1000) > 999:
                        matriz_island[x][y] = 3

# Image Render
print("Rendering water...")
for x in range(img_width):
    for y in range(img_height):
        if matriz_water[x][y] == 1:
            blank_image[xpw:xfw, ypw:yfw] = blue
        ypw, yfw = ypw + 1, yfw + 1
    xpw, xfw = xpw + 1, xfw + 1
    ypw, yfw = 0, 1

print("Rendering dirt, sand and structures...")
for x in range(int(IslandX)):
    for y in range(int(IslandY)):
        if matriz_island[x][y] == 1:
            blank_image[xpi:xfi, ypi:yfi] = yellow
        if matriz_island[x][y] == 2:
            blank_image[xpi:xfi, ypi:yfi] = green
        if matriz_island[x][y] == 3:
            blank_image[xpi:xfi, ypi:yfi] = red
        ypi, yfi = ypi + 10, yfi + 10
    xpi, xfi = xpi + 10, xfi + 10
    ypi, yfi = 0, 10

print("Finish.")
cv2.imwrite("map.jpg", blank_image)
