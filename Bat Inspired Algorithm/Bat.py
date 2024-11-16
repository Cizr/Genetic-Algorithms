import random
import numpy as np
import matplotlib.pyplot as plt

#Parameters
N = 5  #Numb Bats
Loudness = 0.5  #Loudness
Pulse_Rate = 0.5  #Pulse rate
Max_Generations = 100  #num of iterations

#maze (0 = open, 1 = wall)
maze = np.array([
    [0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0],
    [1, 1, 0, 0, 0],
    [0, 0, 0, 1, 0]
])

#start and goal positions
start = (0, 0)
goal = (4, 4)


def initialize_bats():
    bats = []
    for _ in range(N):
        bat = list(start)  #start position
        bats.append(bat)
    return bats

#Fitness func aka (the distance from the goal)
def fitness(position):
    return abs(position[0] - goal[0]) + abs(position[1] - goal[1])

#Check if a move is valid (inside the maze and not a wall)
def is_valid_move(position):
    x, y = position
    if 0 <= x < maze.shape[0] and 0 <= y < maze.shape[1] and maze[x][y] == 0:
        return True
    return False

#randomly move the bat and ensure validity
def move_bat(bat, best_position):
    new_bat = list(bat)

    direction = random.choice(['up', 'down', 'left', 'right'])
    if direction == 'up': new_bat[0] -= 1
    elif direction == 'down': new_bat[0] += 1
    elif direction == 'left': new_bat[1] -= 1
    elif direction == 'right': new_bat[1] += 1

    #if move is invalid stay in place
    if not is_valid_move(new_bat):
        new_bat = bat

    #apply best solution with some probability (Pulse)
    if random.random() < Pulse_Rate:
        new_bat = best_position

    return new_bat

#Visualization
def visualize(maze, bat_positions, goal):
    plt.imshow(maze, cmap='gray', origin='upper')  # Plot the maze
    plt.scatter(*start, color='blue', label='Start', s=100, marker='o')  # Start position
    plt.scatter(*goal, color='red', label='Goal', s=100, marker='x')  # Goal position
    for bat in bat_positions:
        plt.scatter(bat[1], bat[0], color='green', label='Bat Position', s=50)  # Bat positions
    plt.legend()
    plt.show()

#Bat Algorithm
def bat_algorithm():
    bats = initialize_bats()
    best_bat = start
    best_fitness = fitness(best_bat)
    all_positions = []  #store bat positions for visualization

    print("Starting Bat Algorithm\n")
    print(f"Initial Best Position: {best_bat} with Fitness: {best_fitness}")

    for generation in range(Max_Generations):
        print(f"Generation {generation}:")
        for i in range(N):
            bat = bats[i]
            new_bat = move_bat(bat, best_bat)
            new_fitness = fitness(new_bat)

            #update best position if needed
            if new_fitness < best_fitness:
                best_bat = new_bat
                best_fitness = new_fitness
                print(f"  - Bat {i} moved to {new_bat} with Fitness: {new_fitness} (New Best Position)")

            #update bat's position with some probability
            if random.random() < Loudness:
                bats[i] = new_bat
            else:
                print(f"  - Bat {i} remained at {bat} with Fitness: {fitness(bat)}")

        print(f"Best Position at Generation {generation}: {best_bat} with Fitness: {best_fitness}\n")

        #store bat positions for visualization
        all_positions.append([bat for bat in bats])

        #stop if the goal is reached
        if best_bat == list(goal):
            print(f"Goal reached at {best_bat}!")
            break

    #visualize the maze and bat positions
    visualize(maze, all_positions[-1], goal)  # Visualize the final bat positions

bat_algorithm()
