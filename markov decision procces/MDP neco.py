import pygame
import numpy as np
import random
import os

matrix_size = 5
matrix = np.zeros((matrix_size, matrix_size))
cell_size = 100

## localde caliştirmak icin :: image_path = "C:/Users/pc/OneDrive/Masaüstü/markov decision procces/images/"

# Docker konteyner içerisinde çalışırken dosyaların yolu
image_path = "/usr/src/app/images/"


car_image = pygame.image.load(image_path + "car.png")
new_size = (int(cell_size * 0.8), int(cell_size * 0.8))
car_image = pygame.transform.scale(car_image, new_size)

finish_image = pygame.image.load(image_path + "finish.png")
finish_image = pygame.transform.scale(finish_image, (cell_size, cell_size))

hole_image = pygame.image.load(image_path + "hole.png")
hole_image = pygame.transform.scale(hole_image, (cell_size, cell_size))

block_image = pygame.image.load(image_path + "block.png")
block_image = pygame.transform.scale(block_image, (cell_size, cell_size))

car_position = [4, 0]
finish_position = [0, 4]
hole_positions = [[2, 3], [2, 2]]
block_positions = [[0, 2], [1, 2]]

path = []

window_width = cell_size * matrix_size
window_height = cell_size * matrix_size
learning_rate = 0.1
discount_factor = 0.9
exploration_prob = 0.2
num_episodes = 1000
num_states = matrix_size * matrix_size
num_actions = 4
Q = np.zeros((num_states, num_actions))

previous_action = None
game_over = False

def state_to_index(state):
    return state[0] * matrix_size + state[1]

def index_to_state(index):
    row = index // matrix_size
    col = index % matrix_size
    return [row, col]

def choose_action(state):
    valid_actions = []
    if state[0] > 0:
        valid_actions.append(0)
    if state[0] < matrix_size - 1:
        valid_actions.append(1)
    if state[1] > 0:
        valid_actions.append(2)
    if state[1] < matrix_size - 1:
        valid_actions.append(3)

    if previous_action is not None:
        opposites = {0: 1, 1: 0, 2: 3, 3: 2}
        if opposites[previous_action] in valid_actions:
            valid_actions.remove(opposites[previous_action])

    if random.uniform(0, 1) < exploration_prob:
        return random.choice(valid_actions)
    else:
        q_values = [Q[state_to_index(state), action] for action in valid_actions]
        max_q_value_index = np.argmax(q_values)
        return valid_actions[max_q_value_index]

def update_Q(state, action, reward, next_state):
    current_index = state_to_index(state)
    next_index = state_to_index(next_state)
    max_next_Q = np.max(Q[next_index])
    Q[current_index, action] = Q[current_index, action] + learning_rate * (reward + discount_factor * max_next_Q - Q[current_index, action])

def move(action):
    global generation, game_over
    next_state = list(car_position)
    if action == 0:
        next_state[0] -= 1
    elif action == 1:
        next_state[0] += 1
    elif action == 2:
        next_state[1] -= 1
    elif action == 3:
        next_state[1] += 1

    reward = -0.01

    if next_state in hole_positions:
        reward = -1
        reset_game()
        generation += 1
    elif next_state in block_positions:
        return -0.05
    elif next_state != car_position:
        path.append(next_state)
        car_position[:] = next_state

    if car_position == finish_position:
        reward = 1
     #   game_over = True
     
    return reward

def reset_game():
    global previous_action
    car_position[0] = 4
    car_position[1] = 0
    previous_action = None

def draw_game_over_message():
    message = "Congarts, Ai finished at {} generation!".format(generation)
    text_surface = myfont.render(message, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(window_width/2, window_height/2))
    screen.blit(text_surface, text_rect)

pygame.init()
screen = pygame.display.set_mode((window_width, window_height))
myfont = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()
generation = 1
step = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    if game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_game_over_message()
        pygame.display.flip()
        continue

    screen.fill((255, 255, 255))

    for x in range(matrix_size):
        for y in range(matrix_size):
            rect = pygame.Rect(y * cell_size, x * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, (200, 200, 200), rect, 1)

    for hole in hole_positions:
        screen.blit(hole_image, (hole[1] * cell_size, hole[0] * cell_size))

    for block in block_positions:
        screen.blit(block_image, (block[1] * cell_size, block[0] * cell_size))

    screen.blit(car_image, (car_position[1] * cell_size + cell_size * 0.1, car_position[0] * cell_size + cell_size * 0.1))
    screen.blit(finish_image, (finish_position[1] * cell_size, finish_position[0] * cell_size))

    steps_label = myfont.render('Steps: {}'.format(step), 1, (0, 0, 0))
    generation_label = myfont.render('Generation: {}'.format(generation), 1, (0, 0, 0))
    screen.blit(steps_label, (10, 10))
    screen.blit(generation_label, (10, 50))

    pygame.display.flip()

    if car_position == finish_position:
        reward = 1
        game_over = True
        draw_game_over_message()
        pygame.display.flip()
        pygame.time.wait(2000)  # Delay for 2 seconds (or any other preferred time)
        reset_game()
        generation += 1
        game_over = False

    if not game_over:
        action = choose_action(car_position)
        previous_position = list(car_position)
        reward = move(action)
        next_position = list(car_position)
        previous_action = action

        update_Q(previous_position, action, reward, next_position)
        

        step += 1
        if car_position in hole_positions:
            generation += 1
            step = 0

    clock.tick(10)

pygame.quit()
