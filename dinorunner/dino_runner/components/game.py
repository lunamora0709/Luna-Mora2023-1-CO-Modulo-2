import pygame

from dino_runner.utils.constants import BG, DEAD, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, FONT_STYLE, RESET, DEFAULT_TYPE, DEAD

from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import Obstacle_Manager
from dino_runner.components.obstacles.cloud import Cloud
from dino_runner.components.power_ups.power_up_manager import PowerUpManager
HI_COLOR = pygame.Color(202, 197, 196)
SCORE_COLOR = pygame.Color(0, 0, 0)

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.player = Dinosaur()
        self.obstacle_manager = Obstacle_Manager()
        self.cloud = Cloud()
        self.running = False
        self.score = 0
        self.death_count = 0
        self.power_ups_manager = PowerUpManager()
        self.best_score = 0 

    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.game_over = True
                self.show_menu()
        pygame.display.quit()
        pygame.quit()

    def run(self):
        # Game loop: events - update - draw
        self.reset_game()
        self.playing = True
        while self.playing:
            self.events() 
            self.update()
            self.draw()

    
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                
    def update(self):
        self.update_score()
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.cloud.update(self.game_speed)
        self.power_ups_manager.update(self)
        
    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.draw_score()
        self.draw_power_up_time()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.cloud.draw(self.screen)
        self.power_ups_manager.draw(self.screen)
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def draw_score(self):
        self.generate_text(f"Score:{self.score}", 965, 15, 20, SCORE_COLOR)
        self.generate_text(f"Best score:{self.best_score}", 1000, 35, 20, HI_COLOR)
        
    def draw_power_up_time(self):
        if self.player.has_power_up:
            time_to_show = round((self.player.power_time_up - pygame.time.get_ticks())/1000, 2)
            if time_to_show >= 0:
               self.generate_text(
                    f'{self.player.type.capitalize()}, enable for {time_to_show}',
                     550,
                     50,  
                     18,
                     SCORE_COLOR  
               )
            else:
                self.has_power_up = False
                self.player.type = DEFAULT_TYPE

    def update_score(self):
        self.score += 1

        if self.death_count >= 0:
            if self.score % 100 == 0 and self.game_speed < 700:
                self.game_speed += 4
        
        if self.score >= self.best_score:
            self.best_score = self.score


    def handle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False
            elif event.type == pygame.KEYDOWN:
                self.run()

    def generate_text(self, text, half_screen_width, half_screen_heigh, size, color):
        
        font = pygame.font.Font(FONT_STYLE, size)
        text = font.render(f"{text}", True, color)
        text_rec = text.get_rect()
        text_rec.center = (half_screen_width, half_screen_heigh)
        self.screen.blit(text, text_rec)

    def show_menu(self):
        print(self.death_count)
        self.screen.fill((255, 255, 255))
        half_screen_heigh = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2

        if self.death_count == 0:
            self.generate_text("Press any key to play...",  550,550 // 2, 45, SCORE_COLOR)
            self.screen.blit(ICON, (half_screen_width - 50, half_screen_heigh + 40))
        else:
            self.generate_text("You Died",  half_screen_width , half_screen_heigh - 170, 70, SCORE_COLOR)
            self.generate_text(f"Deaths: {self.death_count}", half_screen_width, half_screen_heigh , 40, SCORE_COLOR)
            self.generate_text(f"Score: {self.score}",  half_screen_width, half_screen_heigh+50, 45, SCORE_COLOR)
            self.generate_text(f"Best Score: {self.best_score}", half_screen_width, half_screen_heigh + 100, 47, SCORE_COLOR)
            self.generate_text("Press any key to restart", half_screen_width, half_screen_heigh +170, 50, SCORE_COLOR)
            self.screen.blit(DEAD, ( half_screen_width - 40, half_screen_heigh - 120))
            self.screen.blit(RESET, ( half_screen_width - 35, half_screen_heigh + 210))
        pygame.display.update()
        self.handle_events_on_menu()

    def reset_game(self):
        self.obstacle_manager.reset_obstacles()
        self.score = 0
        self.game_speed = 20
        self.power_ups_manager.reset_power_ups()
        
