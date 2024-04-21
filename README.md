# PSIML10-Maze
Below is a text for one of the three tasks that were part of application for universary 10th PSIML.

# Description
In this problem, you are given an image that contains a simple maze. Images can vary in size, but there are some general rules when it comes to how does the maze look like. Each pixel in the maze is either empty, hence free to step on or occupied by wall. Pixels that are not empty cannot be visited. Maze can also contain multiple gaps around the border that we call entrances. You can enter the maze in any one of the and exit in any other else. The goal is to find the shortest path one can traverse the maze on. Some definitions are given below.
There is one example of a maze anda a valid path. Nothe that your path doesn't have to be centered like this one, you just can't stand on  walls.

![maze_example](https://github.com/Dovlane/PSIML10-Maze/assets/57462728/972a4012-5948-41e2-92e2-0f2bbdafebef)

However, this maze is not just an ordinary maze. It can also contain a certain number of teleports. Those are special pixels that make you able to enter it and exit in any other teleport. You should also find the shortest path using teleports.

## Task 1: Count entrances
Count the number of entrances in the given maze.

## Task 2: Shortest path
Find the length of the shortest path in the maze.

## Task 3: Shortest path with a twist
Find the length of the shortest path in the maze if you are allowed to use teleports.

## Input
Input starts with a path to the image that contains maze. This image is guranteed to be in the PNG format. The next line contains the number of teleports N. The following N lines contain two numbers - row and column for each telport in the maze.

## Output
Output should contain three lines. The first line represents number of entrances in the maze. The second contains the length of the shortest path while the third contains the length of the shortest path if you are allowed to use teleports. Note that you are not required to use any teleport if the shortest path can be obtained without them. In case there is no valid path in the maze, output -1.

## Scoring
Each test case can bring a maximum of 100 points. Correctly counted entrances in the first task brin 20 points per test case. The correct length of the shortest path brings another 50 points while the remaining 30 points are given for the length of the shortest path with teleports included.

## Definitions
  - Pixel is said to be neighboring to another pixel if one can move either left, right, up, or down by exactly one step.
  - Path is a list of neighboring pixels.
  - The shortest path is a path that visits the least number of pixels.
