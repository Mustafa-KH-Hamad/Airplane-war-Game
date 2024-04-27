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
            elif self.model.menu_active:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.model.start_button.collidepoint(mouse_pos):
                        self.model.menu_active = False
                        self.model.show_difficulty_options = True  # Set to True to show difficulty options
                    elif self.model.exit_button.collidepoint(mouse_pos):  # Added condition for exit button
                        pygame.quit()
                        sys.exit()
            elif self.model.show_difficulty_options:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.model.easy_button.collidepoint(mouse_pos):
                        self.model.difficulty_level = "easy"
                        self.model.show_difficulty_options = False
                        self.model.game_started = True
                        self.model.player_health = 3
                    elif self.model.medium_button.collidepoint(mouse_pos):
                        self.model.difficulty_level = "medium"
                        self.model.show_difficulty_options = False
                        self.model.game_started = True
                        self.model.player_health = 2
                    elif self.model.hard_button.collidepoint(mouse_pos):
                        self.model.difficulty_level = "hard"
                        self.model.show_difficulty_options = False
                        self.model.game_started = True
                        self.model.player_health = 1
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.model.play_bullet_sound()
                    bullet_y = self.model.player_y + self.model.player_height // 2 - self.model.bullet_height // 2
                    self.model.bullets.append(
                        pygame.Rect(self.model.player_x + self.model.player_width, bullet_y, self.model.bullet_width,
                                    self.model.bullet_height))
                elif (event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL) and self.model.score > 100:
                    self.model.play_bullet_sound()
                    bullet_y1 = self.model.player_y + self.model.player_height // 3 - self.model.bullet_height // 2
                    bullet_y2 = self.model.player_y + 2 * self.model.player_height // 3 - self.model.bullet_height // 2
                    self.model.bullets.append(
                        pygame.Rect(self.model.player_x + self.model.player_width, bullet_y1, self.model.bullet_width,
                                    self.model.bullet_height))
                    self.model.bullets.append(
                        pygame.Rect(self.model.player_x + self.model.player_width, bullet_y2, self.model.bullet_width,
                                    self.model.bullet_height))

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    # Toggle the pause state
                    self.model.paused = not self.model.paused
            elif self.model.menu_active:  # Check if the menu becomes active again
                # Reset game state
                self.model.menu_active = True
                self.model.start_button = pygame.Rect(300, 200, 200, 50)  # Position and size of start button
                self.model.exit_button = pygame.Rect(300, 300, 200, 50)
                self.model.difficulty_level = None
                self.model.show_difficulty_options = False
                self.model.game_started = False
                self.model.paused = False
                self.model.cloud_spawn_timer = 0
                self.model.clouds = []
                self.model.score = 0
                self.model.player_health = 3
                self.model.shield_timer = 0
                self.model.enemies = []
                self.model.bullets = []
                self.model.enemy_bullets = []

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
            self.model.menu_active = True

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
                    self.model.menu_active = True

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
                        self.model.menu_active = True
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
                        self.model.menu_active = True
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
                        self.model.menu_active = True

    def run(self):
        while True:
            self.handle_events()
            if self.model.game_started:  # Start the game only if game_started is True
                if not self.model.paused:  # Check if the game is not paused
                    self.update()  # Update game state only if not paused
            self.view.draw_background()
            if self.model.menu_active:
                self.view.draw_menu()
            elif self.model.show_difficulty_options:
                self.view.draw_difficulty_options()
            else:
                self.view.draw_player()
                self.view.draw_enemies()
                self.view.draw_bullets()
                self.view.draw_score()
                self.view.draw_player_health()
                self.view.draw_power_ups()
                self.view.draw_clouds()
                if self.model.paused:  # Check if the game is paused
                    self.view.draw_paused_text()  # Draw "Paused" text
            self.view.update_display()
            self.clock.tick(60)



