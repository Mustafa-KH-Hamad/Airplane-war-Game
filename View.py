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
        game_over_text = pygame.font.Font(None, 36).render("You Died!", True, (255, 0, 0))
        self.screen.blit(game_over_text, (self.model.screen_width // 2 - 100, self.model.screen_height // 2 - 20))
        pygame.display.flip()
        pygame.time.delay(2000)  # Pause for 2 seconds
        pygame.quit()
        quit()

    def draw_game_over_win(self):
        game_over_win_text = pygame.font.Font(None, 36).render("You Won congrats! GG!", True, (255, 0, 0))
        self.screen.blit(game_over_win_text, (self.model.screen_width // 2 - 100, self.model.screen_height // 2 - 20))
        pygame.display.flip()
        pygame.time.delay(2000)  # Pause for 2 seconds
        pygame.quit()
        quit()

    def draw_clouds(self):
        for cloud in self.model.clouds:
            self.screen.blit(self.model.cloud_image, (cloud[0], cloud[1]))

    def draw_menu(self):
        self.screen.fill((255, 255, 255))  # Fill the screen with white color

        # Draw start and exit buttons
        start_text = pygame.font.Font(None, 36).render("Start", True, (0, 0, 0))
        exit_text = pygame.font.Font(None, 36).render("Exit", True, (0, 0, 0))
        pygame.draw.rect(self.screen, (0, 0, 255), self.model.start_button)
        pygame.draw.rect(self.screen, (0, 0, 255), self.model.exit_button)
        self.screen.blit(start_text, (350, 215))
        self.screen.blit(exit_text, (360, 315))

    def draw_difficulty_options(self):
        self.screen.fill((255, 255, 255))  # Fill the screen with white color

        # Draw difficulty buttons
        easy_text = pygame.font.Font(None, 36).render("Easy", True, (0, 0, 0))
        medium_text = pygame.font.Font(None, 36).render("Medium", True, (0, 0, 0))
        hard_text = pygame.font.Font(None, 36).render("Hard", True, (0, 0, 0))
        pygame.draw.rect(self.screen, (0, 255, 0), self.model.easy_button)
        pygame.draw.rect(self.screen, (0, 255, 0), self.model.medium_button)
        pygame.draw.rect(self.screen, (0, 255, 0), self.model.hard_button)
        self.screen.blit(easy_text, (300, 215))
        self.screen.blit(medium_text, (300, 285))
        self.screen.blit(hard_text, (300, 355))

    def draw_paused_text(self):
        paused_text = self.font.render("Paused", True, (255, 0, 0))
        paused_text_rect = paused_text.get_rect(center=(self.model.screen_width // 2, self.model.screen_height // 2))
        self.screen.blit(paused_text, paused_text_rect)

