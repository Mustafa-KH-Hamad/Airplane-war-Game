import pygame


class GameView:
    def __init__(self, model):
        self.model = model
        self.screen = model.screen
        pygame.font.init()
        self.font = pygame.font.SysFont(None, 48)

    def draw_background(self):
        self.screen.blit(self.model.imageA, (self.model.image_xA, 0))
        self.screen.blit(self.model.imageB, (self.model.image_xB, 0))

    def draw_player(self):
        self.screen.blit(self.model.player_image, (self.model.player_x, self.model.player_y))

    def draw_enemies(self):
        for enemy in self.model.enemies:
            if enemy[0] == "strong":
                self.screen.blit(self.model.strong_enemy_image, (enemy[1].x, enemy[1].y))
            else:
                self.screen.blit(self.model.enemy_image, (enemy[1].x, enemy[1].y))

    def draw_bullets(self):
        for bullet in self.model.bullets:
            pygame.draw.rect(self.screen, self.model.BLACK, bullet)

        for bullet in self.model.enemy_bullets:
            pygame.draw.rect(self.screen, self.model.BLUE, bullet)

    def draw_score(self):
        score_text = pygame.font.Font(None, 36).render("Score: " + str(self.model.score), True, self.model.BLUE)
        self.screen.blit(score_text, (10, 10))

    def draw_player_health(self):
        for i in range(self.model.player_health):
            self.screen.blit(self.model.heart_image, (self.model.screen_width - 40 - i * 30, 10))

    def draw_power_ups(self):
        for power_up in self.model.power_ups:
            pygame.draw.rect(self.screen, self.model.RED, power_up)

    def update_display(self):
        pygame.display.flip()

    def draw_game_over(self):
        background_image = pygame.image.load("Assets/gameover.png").convert()
        self.screen.blit(background_image, (0, 0))
        pygame.display.flip()
        pygame.time.delay(2000)  # Pause for 2 seconds
        self.model.menu_active = True

    def draw_game_over_win(self):
        background_image = pygame.image.load("Assets/gamewin.png").convert()
        self.screen.blit(background_image, (0, 0))
        pygame.display.flip()
        pygame.time.delay(2000)  # Pause for 2 seconds
        self.model.menu_active = True

    def draw_clouds(self):
        for cloud in self.model.clouds:
            self.screen.blit(self.model.cloud_image, (cloud[0], cloud[1]))

    def draw_menu(self):

        # Draw start and exit buttons
        start_text = pygame.font.Font(None, 36).render("Start", True, (0, 0, 0))
        exit_text = pygame.font.Font(None, 36).render("Exit", True, (0, 0, 0))

        # Draw buttons at custom positions
        start_button_rect = pygame.Rect(300, 250, 190, 150)
        exit_button_rect = pygame.Rect(300, 350, 190, 100)

        pygame.draw.rect(self.screen, (0, 0, 255), start_button_rect)
        pygame.draw.rect(self.screen, (0, 0, 255), exit_button_rect)

        self.screen.blit(start_text, (start_button_rect.x, start_button_rect.y))
        self.screen.blit(exit_text, (exit_button_rect.x, exit_button_rect.y))

        # Update model attributes for button detection
        self.model.start_button = start_button_rect
        self.model.exit_button = exit_button_rect

        background_image = pygame.image.load("Assets/menu.png").convert()
        self.screen.blit(background_image, (0, 0))





    def draw_difficulty_options(self):


        # Draw background image


        # Draw difficulty buttons
        # Define button texts
        easy_text = pygame.font.Font(None, 36).render("Easy", True, (0, 0, 0))
        medium_text = pygame.font.Font(None, 36).render("Medium", True, (0, 0, 0))
        hard_text = pygame.font.Font(None, 36).render("Hard", True, (0, 0, 0))

        # Define button rectangles
        easy_button_rect = pygame.Rect(250, 150, 220, 50)
        medium_button_rect = pygame.Rect(200, 270, 330, 50)
        hard_button_rect = pygame.Rect(260, 390, 190, 50)

        # Draw buttons
        pygame.draw.rect(self.screen, (0, 255, 0), easy_button_rect)
        pygame.draw.rect(self.screen, (0, 255, 0), medium_button_rect)
        pygame.draw.rect(self.screen, (0, 255, 0), hard_button_rect)

        # Blit button texts
        self.screen.blit(easy_text, (easy_button_rect.x, easy_button_rect.y))
        self.screen.blit(medium_text, (medium_button_rect.x, medium_button_rect.y))
        self.screen.blit(hard_text, (hard_button_rect.x, hard_button_rect.y))

        # Update model attributes for button detection
        self.model.easy_button = easy_button_rect
        self.model.medium_button = medium_button_rect
        self.model.hard_button = hard_button_rect

        background_image = pygame.image.load("Assets/difficulty.png").convert()
        self.screen.blit(background_image, (0, 0))

    def draw_paused_text(self):
        background_image = pygame.image.load("Assets/pause.png").convert()
        self.screen.blit(background_image, (0, 0))

        paused_text = self.font.render("Paused", True, (255, 0, 0))
        paused_text_rect = paused_text.get_rect(center=(self.model.screen_width // 2, self.model.screen_height // 2))
        self.screen.blit(paused_text, paused_text_rect)

