import pygame
import random

class GameModel:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Set up the screen
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Simple 2D Game")
        # Load cloud image
        self.cloud_image = pygame.image.load("Assets/cloud.png").convert_alpha()
        self.cloud_image = pygame.transform.scale(self.cloud_image, (100, 110))  # Resize to 50x50 pixels

        # Cloud settings
        self.cloud_spawn_timer = 0
        self.cloud_width = 100  # Adjust cloud width as needed
        self.cloud_height = 50  # Adjust cloud height as needed
        self.cloud_speed = 2  # Adjust cloud speed as needed
        self.clouds = []


        # Load background music
        pygame.mixer.music.load("Assets/music1.mp3")
        pygame.mixer.music.play(loops=-1)  # -1 to loop indefinitely
        pygame.mixer.music.set_volume(0.5)

        # Load heart image and resize it
        self.heart_image = pygame.image.load("Assets/health.png").convert_alpha()
        self.heart_image = pygame.transform.scale(self.heart_image, (30, 30))

        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)

        # Load background images
        self.imageA = pygame.image.load("Assets/b1.jpg").convert_alpha()
        self.imageB = pygame.image.load("Assets/b2.jpg").convert_alpha()

        # Set initial position of the images
        self.image_xA = 0
        self.image_xB = self.screen_width

        # Set the speed at which the images scroll
        self.scroll_speed = 1

        # Load images
        self.player_image = pygame.image.load("Assets/Player.png").convert_alpha()
        self.player_image = pygame.transform.scale(self.player_image, (50, 50))
        self.enemy_image = pygame.image.load("Assets/enemy.png").convert_alpha()
        self.enemy_image = pygame.transform.scale(self.enemy_image, (50, 50))
        self.strong_enemy_image = pygame.image.load("Assets/enemy2.png").convert_alpha()
        self.strong_enemy_image = pygame.transform.scale(self.strong_enemy_image, (70, 70))

        # Load death animation images and resize them
        self.death_animation_frames = [pygame.transform.scale(pygame.image.load(f"Assets/{i}.png").convert_alpha(), (30, 30)) for i in range(1, 4)]
        self.death_animation_index = 0  # Index to track the current frame of the death animation
        self.death_animation_speed = 5  # Speed at which to switch frames for the death animation

        # Player settings
        self.player_width = 50
        self.player_height = 50
        self.player_x = 50
        self.player_y = self.screen_height // 2 - self.player_height // 2
        self.player_speed = 5

        # Bullet settings
        self.bullet_width = 10
        self.bullet_height = 5
        self.bullet_speed = 7
        self.bullets = []

        # Enemy settings
        self.enemy_width = 50
        self.enemy_height = 50
        self.enemy_speed = 3
        self.enemy_bullet_speed = 5  # Speed of enemy bullets
        self.enemies = []

        # Enemy bullet settings
        self.enemy_bullets = []
        self.power_ups = []

        # Score
        self.score = 0

        # Player health
        self.player_health = 3

        # Shield timer
        self.shield_timer = 0

        # Timer for controlling animation speed
        self.animation_timer = 0

    # Function to create a new enemy
    def create_enemy(self):
        enemy_y = random.randint(0, self.screen_height - self.enemy_height)
        self.enemies.append(("normal", pygame.Rect(self.screen_width - self.enemy_width, enemy_y, self.enemy_width, self.enemy_height)))

    # Function to create a new enemy with higher health
    def create_strong_enemy(self):
        enemy_y = random.randint(0, self.screen_height - self.enemy_height)
        self.enemies.append(("strong", pygame.Rect(self.screen_width - self.enemy_width, enemy_y, 70, 70), 2))

    # Function to create a new enemy bullet
    def create_enemy_bullet(self, enemy):
        bullet_y = enemy[1].y + enemy[1].height // 2 - self.bullet_height // 2
        self.enemy_bullets.append(pygame.Rect(enemy[1].x, bullet_y, self.bullet_width, self.bullet_height))

    # Function to create a power-up
    def create_power_up(self):
        power_up_y = random.randint(0, self.screen_height - self.power_up_height)
        return pygame.Rect(random.randint(0, self.screen_width - self.power_up_width), power_up_y, self.power_up_width, self.power_up_height)

    # Function to play bullet sound
    def play_bullet_sound(self):
        bullet_sound = pygame.mixer.Sound("Assets/shoot.wav")
        bullet_sound.set_volume(0.1)  # Adjust volume as needed
        bullet_sound.play()

    # Function to play death animation
    def play_death_animation(self, x, y):
        # Calculate position for the animation to be centered on the enemy
        anim_x = x + (self.enemy_width - self.death_animation_frames[0].get_width()) // 2
        anim_y = y + (self.enemy_height - self.death_animation_frames[0].get_height()) // 2

        # Draw the current frame of the death animation
        self.screen.blit(self.death_animation_frames[self.death_animation_index], (anim_x, anim_y))
        # Update the animation timer
        self.animation_timer += 1
        # Check if it's time to switch frames
        if self.animation_timer >= self.death_animation_speed:
            # Reset the animation timer
            self.animation_timer = 0
            # Move to the next frame
            self.death_animation_index += 1
            # Check if reached the end of the animation frames
            if self.death_animation_index >= len(self.death_animation_frames):
                # Reset the animation index to restart the animation
                self.death_animation_index = 0

    # Function to display "You Died" message
    def display_game_over(self):
        game_over_text = pygame.font.Font(None, 36).render("You Died!", True, (255, 0, 0))
        self.screen.blit(game_over_text, (self.screen_width // 2 - 100, self.screen_height // 2 - 20))
        pygame.display.flip()
        pygame.time.delay(2000)  # Pause for 2 seconds
        pygame.quit()
        quit()

    def display_game_over_win(self):
        game_over_win_text = pygame.font.Font(None, 36).render("You Won congrats! GG!", True, (255, 0, 0))
        self.screen.blit(game_over_win_text, (self.screen_width // 2 - 100, self.screen_height // 2 - 20))
        pygame.display.flip()
        pygame.time.delay(2000)  # Pause for 2 seconds
        pygame.quit()
        quit()
    def update_clouds(self):
        self.cloud_spawn_timer += 1
        if self.cloud_spawn_timer >= 300:  # Spawn a cloud every 5 seconds (assuming 60 FPS)
            self.spawn_cloud()
            self.cloud_spawn_timer = 0

        for cloud in self.clouds:
            cloud[0] -= self.cloud_speed  # Move the cloud horizontally

    def spawn_cloud(self):
        cloud_y = random.randint(0, self.screen_height - self.cloud_height)
        self.clouds.append([self.screen_width, cloud_y])