import pygame

class GameView:
    def __init__(self, model):
        self.model = model
        self.screen = model.screen

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

