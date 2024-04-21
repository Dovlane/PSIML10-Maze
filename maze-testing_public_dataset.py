import numpy as np
import imageio.v3 as iio
import os

BLACK = [0, 0, 0, 255]
WHITE = [255, 255, 255, 255]


pixelMoveNext = [[1, 0], [0, 1], [-1, 0], [0, -1]]
pixelMovePrev = [[-1, 0], [0, 1], [1, 0], [0, -1]]


def getNext(row, col, width, height, pixelMove, phase, boundaries, enable_exit):
    if (phase == 0 and row + pixelMove[phase][0] == boundaries[0]) or\
        (phase == 1 and col + pixelMove[phase][1] == boundaries[1]) or\
        (phase == 2 and row + pixelMove[phase][0] == boundaries[2]) or\
        (phase == 3 and col + pixelMove[phase][1] == boundaries[3]):
        phase += 1

    if phase == 4: # 4 = len(pixelMove)
        if enable_exit:
            return [-1, 0, 0]
        phase %= 4
    

    row += pixelMove[phase][0]
    col += pixelMove[phase][1]
    
    return [phase, row, col]


def equalColor(color1, color2):
    return (color1[:2] == color2[:2]).all()

def isTeleport(teleports, row, col):
    return row in teleports.keys() and col in teleports[row].keys()

"""
D:\Desktop\trenutniProgrami\testingPSIML\maze\maze_solution-7.png
4
0 94
50 97
150 97
199 94

D:/Desktop/trenutniProgrami/testingPSIML/maze/public-maze/set/09.png
7
25 5
19 237
119 5
218 5
233 233
173 235
119 236
"""

root_path = "D:/Desktop/trenutniProgrami/testingPSIML/maze/public-maze/"
set_path = "D:/Desktop/trenutniProgrami/testingPSIML/maze/public-maze/set/"
out_path = "D:/Desktop/trenutniProgrami/testingPSIML/maze/public-maze/outputs/"
input_directory_path = "D:/Desktop/trenutniProgrami/testingPSIML/maze/public-maze/inputs/"

input_paths = []
image_paths = []
output_paths = []


for root, dirs, files in os.walk(set_path):
    for filename in files:
        if filename.endswith(".png"):
            num = filename.replace(".png", '')
            input_path = os.path.join(input_directory_path, num + ".txt")
            output_path = os.path.join(out_path, num + ".txt")
            image_path = os.path.join(set_path, num + ".png")
            image_paths.append(image_path)
            input_paths.append(input_path)
            output_paths.append(output_path)
                
i = 7
j = 9
# input_paths = input_paths[0:i]
# image_paths = image_paths[0:i]
# output_paths = output_paths[0:i]
# input_paths = [input_paths[i], input_paths[j]]
# image_paths = [image_paths[i], image_paths[j]]
# output_paths = [output_paths[i], output_paths[j]]
# input_paths = [input_paths[j]]
# image_paths = [image_paths[j]]
# output_paths = [output_paths[j]]


for input_path, image_path, output_path in zip(input_paths, image_paths, output_paths):
    N = 0
    phase = 0
    teleports = {}
    with open(input_path) as file_txt:
        lines = file_txt.readlines()
        N = int(lines[1])
        for i in range(N):
            row, col = [int(x) for x in lines[i+2].split()]
            if not row in teleports.keys():
                teleports[row] = {}
            teleports[row][col] = True  
    # for i in range(N):
    #     row, col = [int(x) for x in input().split()]
    #     if not row in teleports.keys():
    #         teleports[row] = {}
    #     teleports[row][col] = True    
        
    image_file = iio.imread(image_path)
    height, width, _ = image_file.shape
    image = np.array(image_file)
    visited = [[(-1, -1) for _ in range(width)] for _ in range(height)]

    boundariesNext = [height, width, -1, -1]
    boundariesPrev = [-1, width, height, -1]


    gates = 0
    row = 0
    col = 0
    queue = []

    while phase != -1:
        if visited[row][col] == (-1, -1) and equalColor(image[row][col], WHITE):
            queue.append([row, col, gates, 0])
            visited[row][col] = (gates, 0)
            next_row, next_col = row, col
            phase_tmp = phase
            while True:
                phase_tmp, next_row, next_col = getNext(next_row, next_col, width, height, pixelMoveNext, phase, boundariesNext, False)
                if visited[next_row][next_col] == (-1, -1) and equalColor(image[next_row][next_col], WHITE):
                    queue.append([next_row, next_col, gates, 0])
                    visited[next_row][next_col] = (gates, 0)
                else:
                    break
            
            phase_tmp = phase
            prev_row, prev_col = row, col
            while True:
                phase_tmp, prev_row, prev_col = getNext(prev_row, prev_col, width, height, pixelMovePrev, phase, boundariesPrev, False)
                if visited[prev_row][prev_col] == (-1, -1) and equalColor(image[prev_row][prev_col], WHITE):
                    queue.append([prev_row, prev_col, gates, 0])
                    visited[prev_row][prev_col] = (gates, 0)
                else:
                    break
            gates += 1
        phase, row, col = getNext(row, col, width, height, pixelMoveNext, phase, boundariesNext, True)

    pathDist = -1
    pathDistTwist = -1

    visited_2 = [row[:] for row in visited]
    queue_2 = queue.copy()

    if gates >= 2:
        found = False
        while len(queue_2) > 0:
            row, col, gate, dist = queue_2.pop(0)
            next_rows = []
            next_cols = []
            if row - 1 >= 0:
                next_rows.append(row - 1)
                next_cols.append(col)
            if row + 1 < height:
                next_rows.append(row + 1)
                next_cols.append(col)
            if col - 1 >= 0:
                next_cols.append(col - 1)
                next_rows.append(row)
            if col + 1 < width:
                next_cols.append(col + 1)
                next_rows.append(row)

            teleportPixel = isTeleport(teleports, row, col)

            if teleportPixel:
                for tel_row in teleports.keys():
                    for tel_col in teleports[tel_row].keys():
                        if (row != tel_row or col != tel_col) and isTeleport(teleports, tel_row, tel_col):
                            next_rows.append(tel_row)
                            next_cols.append(tel_col)
            
            for next_row, next_col in zip(next_rows, next_cols):
                if visited_2[next_row][next_col] == (-1, -1):
                    if equalColor(image[next_row][next_col], WHITE):
                        visited_2[next_row][next_col] = (gate, dist + 1)
                        queue_2.append([next_row, next_col, gate, dist + 1])
                elif visited_2[next_row][next_col][0] != gate:
                    otherGateDist = visited_2[next_row][next_col][1]
                    pathDistTwist = dist + otherGateDist + 2
                    # if teleportPixel and isTeleport(teleports, next_row, next_col):
                    #     pathDistTwist -= 1
                    found = True
                    break
            
            if found:
                break
        

        if pathDistTwist != -1:
            found = False
            while len(queue) > 0:
                row, col, gate, dist = queue.pop(0)
                next_rows = []
                next_cols = []
                if row - 1 >= 0:
                    next_rows.append(row - 1)
                    next_cols.append(col)
                if row + 1 < height:
                    next_rows.append(row + 1)
                    next_cols.append(col)
                if col - 1 >= 0:
                    next_cols.append(col - 1)
                    next_rows.append(row)
                if col + 1 < width:
                    next_cols.append(col + 1)
                    next_rows.append(row)
                
                
                for next_row, next_col in zip(next_rows, next_cols):
                    if visited[next_row][next_col] == (-1, -1):
                        if equalColor(image[next_row][next_col], WHITE):
                            visited[next_row][next_col] = (gate, dist + 1)
                            queue.append([next_row, next_col, gate, dist + 1])
                    elif visited[next_row][next_col][0] != gate:
                        otherGateDist = visited[next_row][next_col][1]
                        pathDist = dist + otherGateDist + 2
                        found = True
                        break
                
                if found:
                    break


        
    myOutput = [str(gates) + "\n", str(pathDist) + "\n", str(pathDistTwist) + "\n"]     
    
    with open(output_path) as outtxt:
        rightOtput = outtxt.readlines()
        rightOtputCmp = rightOtput[:3]
        if (rightOtputCmp == myOutput):
            print("OK")
            print(rightOtput)
        else:
            print("WA")
            print(image_path)
            print(teleports)
            print(myOutput)
            print(rightOtput)
    # print(gates)
    # print(pathDist)
    # print(pathDistTwist)
