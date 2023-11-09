# This Code is Heavily Inspired By The YouTuber: Cheesy AI
# Code Changed, Optimized And Commented By: NeuralNine (Florian Dedov)

import math
import random
import sys
import os

import neat
import pygame

# Constants
# WIDTH = 1600
# HEIGHT = 880

WIDTH = 1920
HEIGHT = 1080

CAR_SIZE_X = 60
CAR_SIZE_Y = 60

BORDER_COLOR = (255, 255, 255, 255) # Color To Crash on Hit

current_generation = 0 # Generation counter
class Car:
    def __init__(self):
        # Initialization code for the car
        self.sprite = pygame.image.load('car.png').convert()
        self.sprite = pygame.transform.scale(self.sprite, (CAR_SIZE_X, CAR_SIZE_Y))
        self.rotated_sprite = self.sprite
        self.position = [830, 920]
        self.angle = 0
        self.speed = 0
        self.speed_set = False
        self.center = [self.position[0] + CAR_SIZE_X / 2, self.position[1] + CAR_SIZE_Y / 2]
        self.radars = []
        self.drawing_radars = []
        self.alive = True
        self.distance = 0
        self.time = 0

    def update(self, game_map):
        if not self.speed_set:
            self.speed = 20
            self.speed_set = True

        self.rotated_sprite = self.rotate_center(self.sprite, self.angle)
        self.position[0] += math.cos(math.radians(360 - self.angle)) * self.speed
        self.position[0] = max(self.position[0], 20)
        self.position[0] = min(self.position[0], WIDTH - 120)

        self.distance += self.speed
        self.time += 1

        self.position[1] += math.sin(math.radians(360 - self.angle)) * self.speed
        self.position[1] = max(self.position[1], 20)
        self.position[1] = min(self.position[1], WIDTH - 120)

        self.center = [int(self.position[0]) + CAR_SIZE_X / 2, int(self.position[1]) + CAR_SIZE_Y / 2]

        self.corners = self.calculate_corners()

        self.check_collision(game_map)
        self.radars.clear()

        for d in range(-90, 120, 45):
            self.check_radar(d, game_map)

    def draw(self, screen):
        screen.blit(self.rotated_sprite, self.position)
        self.draw_radar(screen)

    # Add the rest of the Car class functions here

class NeuralNetwork:
    def __init__(self, genome, config):
        self.net = neat.nn.FeedForwardNetwork.create(genome, config)

    def activate(self, inputs):
        return self.net.activate(inputs)

class Simulation:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.generation_font = pygame.font.SysFont("Arial", 30)
        self.alive_font = pygame.font.SysFont("Arial", 20)
        self.game_map = pygame.image.load('map.png').convert()
        self.current_generation = 0

        config_path = "./config.txt"
        self.config = neat.config.Config(neat.DefaultGenome,
                                         neat.DefaultReproduction,
                                         neat.DefaultSpeciesSet,
                                         neat.DefaultStagnation,
                                         config_path)

        self.population = neat.Population(self.config)
        self.population.add_reporter(neat.StdOutReporter(True))
        self.stats = neat.StatisticsReporter()
        self.population.add_reporter(self.stats)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)

            for i, car in enumerate(self.cars):
                output = self.nets[i].activate(car.get_data())
                choice = output.index(max(output))
                if choice == 0:
                    car.angle += 10
                elif choice == 1:
                    car.angle -= 10
                elif choice == 2:
                    if car.speed - 2 >= 12:
                        car.speed -= 2
                else:
                    car.speed += 2

            still_alive = 0
            for i, car in enumerate(self.cars):
                if car.is_alive():
                    still_alive += 1
                    car.update(self.game_map)
                    self.genomes[i][1].fitness += car.get_reward()

            if still_alive == 0:
                break

            counter += 1
            if counter == 30 * 40:
                break

            self.screen.blit(self.game_map, (0, 0))
            for car in self.cars:
                if car.is_alive():
                    car.draw(self.screen)

            text = self.generation_font.render("Generation: " + str(self.current_generation), True, (0, 0, 0))
            text_rect = text.get_rect()
            text_rect.center = (900, 450)
            self.screen.blit(text, text_rect)

            text = self.alive_font.render("Still Alive: " + str(still_alive), True, (0, 0, 0))
            text_rect = text.get_rect()
            text_rect.center = (900, 490)
            self.screen.blit(text, text_rect)

            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    simulation = Simulation()
    simulation.run()
