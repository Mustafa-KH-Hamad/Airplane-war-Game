import pygame
import sys
import random

class GameController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.clock = pygame.time.Clock()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.model.play_bullet_sound()
                    bullet_y = self.model.player_y + self.model.player_height // 2 - self.model.bullet_height // 2
                    self.model.bullets.append(pygame.Rect(self.model.player_x + self.model.player_width, bullet_y, self.model.bullet_width, self.model.bullet_height))
                elif (event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL) and self.model.score > 100:
                    self.model.play_bullet_sound()
                    bullet_y1 = self.model.player_y + self.model.player_height // 3 - self.model.bullet_height // 2
                    bullet_y2 = self.model.player_y + 2 * self.model.player_height // 3 - self.model.bullet_height // 2
                    self.model.bullets.append(pygame.Rect(self.model.player_x + self.model.player_width, bullet_y1, self.model.bullet_width, self.model.bullet_height))
                    self.model.bullets.append(pygame.Rect(self.model.player_x + self.model.player_width, bullet_y2, self.model.bullet_width, self.model.bullet_height))

    def update(self):
        # Scroll the background images
        self.model.image_xA -= self.model.scroll_speed
        self.model.image_xB -= self.model.scroll_speed

        # Reset the images if they go off-screen
        if self.model.image_xA <= -self.model.screen_width:
            self.model.image_xA = self.model.screen_width
        if self.model.image_xB <= -self.model.screen_width:
            self.model.image_xB = self.model.screen_width

        if self.model.score >= 2000:
            self.view.draw_game_over_win()
            pygame.quit()
            sys.exit()

        # Boundaries for player
        self.model.player_y = max(0, min(self.model.player_y, self.model.screen_height - self.model.player_height))
        self.model.player_x = max(0, min(self.model.player_x, self.model.screen_width - self.model.player_width))

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.model.player_y -= self.model.player_speed
        if keys[pygame.K_DOWN]:
            self.model.player_y += self.model.player_speed
        if keys[pygame.K_RIGHT]:
            self.model.player_x += self.model.player_speed
        if keys[pygame.K_LEFT]:
            self.model.player_x -= self.model.player_speed

        # Boundaries for player
        self.model.player_y = max(0, min(self.model.player_y, self.model.screen_height - self.model.player_height))

        # Create new enemy randomly
        if random.randint(0, 100) < 5:
            if self.model.score >= 100:
                self.model.create_enemy()
                self.model.create_strong_enemy()
            else:
                self.model.create_enemy()

        # Move enemies
        for enemy in self.model.enemies:
            if enemy[0] == "normal":
                enemy[1].x -= self.model.enemy_speed
            else:
                enemy[1].x -= self.model.enemy_speed

        # Remove enemies that go off screen
        self.model.enemies = [enemy for enemy in self.model.enemies if enemy[1].x > 0]

        # Enemy shooting
        for enemy in self.model.enemies:
            if enemy[0] == "strong" and random.randint(0, 100) < 2:
                self.model.create_enemy_bullet(enemy)

        # Move enemy bullets and check collisions with player
        for bullet in self.model.enemy_bullets:
            bullet.x -= self.model.enemy_bullet_speed
            if bullet.colliderect(pygame.Rect(self.model.player_x, self.model.player_y, self.model.player_width, self.model.player_height)):
                if self.model.shield_timer == 0:
                    self.model.player_health -= 1
                    self.model.shield_timer = 2000
                if self.model.player_health <= -1:
                    self.view.draw_game_over()

        # Remove bullets that go off screen
        self.model.enemy_bullets = [bullet for bullet in self.model.enemy_bullets if bullet.x > 0]
        self.model.clouds = [cloud for cloud in self.model.clouds if cloud[0] + self.model.cloud_width > 0]
        for cloud in self.model.clouds[:]:
            cloud[0] -= self.model.cloud_speed

        # Move bullets and check collisions
        for bullet in self.model.bullets[:]:
            bullet.x += self.model.bullet_speed
            for enemy_index, enemy in enumerate(self.model.enemies[:]):
                if bullet.colliderect(enemy[1]):
                    if enemy[0] == "strong":
                        updated_enemy = (enemy[0], enemy[1], enemy[2] - 1)
                        if updated_enemy[2] <= 0:
                            self.model.play_death_animation(enemy[1].x, enemy[1].y)
                            self.model.enemies.pop(enemy_index)
                            self.model.score += 20
                        else:
                            self.model.enemies[enemy_index] = updated_enemy
                    else:
                        self.model.play_death_animation(enemy[1].x, enemy[1].y)
                        self.model.enemies.remove(enemy)
                        self.model.score += 10
                    self.model.bullets.remove(bullet)
                    break

        # Remove bullets that go off screen
        self.model.bullets = [bullet for bullet in self.model.bullets if bullet.x < self.model.screen_width]

        # Collision detection between player and enemies
        for enemy in self.model.enemies:
            if enemy[1].colliderect(pygame.Rect(self.model.player_x, self.model.player_y, self.model.player_width,
                                                self.model.player_height)):
                if self.model.shield_timer == 0:
                    self.model.player_health -= 1
                    self.model.shield_timer = 2000
                    self.model.play_death_animation(enemy[1].x, enemy[1].y)
                    if self.model.player_health <= -1:
                        self.view.draw_game_over()
                        pygame.quit()
                        sys.exit()
                    self.model.enemies.remove(enemy)
                    break

        # Update shield timer
        if self.model.shield_timer > 0:
            self.model.shield_timer -= 1000 / 60
            if self.model.shield_timer < 0:
                self.model.shield_timer = 0
        self.model.update_clouds()
        self.check_collisions()

    def check_collisions(self):
        # Player-enemy collision detection
        for enemy in self.model.enemies:
            if enemy[1].colliderect(pygame.Rect(self.model.player_x, self.model.player_y, self.model.player_width,
                                                self.model.player_height)):
                if self.model.shield_timer == 0:
                    self.model.player_health -= 1
                    self.model.shield_timer = 2000
                    self.model.play_death_animation(enemy[1].x, enemy[1].y)
                    if self.model.player_health <= 0:  # Adjusted condition to retain one more hit
                        self.view.draw_game_over()
                        pygame.quit()
                        sys.exit()
                    self.model.enemies.remove(enemy)
                    break

        # Cloud collision detection
        for cloud in self.model.clouds:
            cloud_rect = pygame.Rect(cloud[0], cloud[1], self.model.cloud_width, self.model.cloud_height)
            if cloud_rect.colliderect(pygame.Rect(self.model.player_x, self.model.player_y, self.model.player_width,
                                                  self.model.player_height)):
                if self.model.shield_timer == 0:
                    self.model.player_health -= 1
                    self.model.shield_timer = 2000  # Resetting shield timer
                    if self.model.player_health <= 0:  # Adjusted condition to retain one more hit
                        self.view.draw_game_over()
                        pygame.quit()
                        sys.exit()


    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.view.draw_background()
            self.view.draw_player()
            self.view.draw_enemies()
            self.view.draw_bullets()
            self.view.draw_score()
            self.view.draw_player_health()
            self.view.draw_power_ups()
            self.view.draw_clouds()
            self.view.update_display()
            self.clock.tick(60)
