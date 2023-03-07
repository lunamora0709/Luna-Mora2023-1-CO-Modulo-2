import pygame
from dino_runner.components.obstacles.bird import Bird
from dino_runner.components.obstacles.cactus import LargeCactus,SmallCactus
from dino_runner.utils.constants import SMALL_CACTUS,LARGE_CACTUS,BIRD


class ObstacleManager:
    def __init__(self):
        self.obstacles =[]
        self.small_cactus = True
        self.large_cactus = False
        self.bird = False

    def update(self, game):
        if len(self.obstacles) == 0 and self.small_cactus:
            cactus = SmallCactus(SMALL_CACTUS)
            self.obstacles.append(cactus)    
            self.small_cactus = False
            self.large_cactus = True
            self.bird = False
        elif len(self.obstacles) == 0 and self.large_cactus:
            cactus = LargeCactus(LARGE_CACTUS)
            self.obstacles.append(cactus)
            self.small_cactus = False
            self.large_cactus = False
            self.bird = True
        elif len(self.obstacles) == 0 and self.bird:
            bird = Bird(BIRD)
            self.obstacles.append(bird)
            self.small_cactus = True
            self.large_cactus = False
            self.bird = False

        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)

            if game.player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(1000)
                game.playing = False

       
    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)