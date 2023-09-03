import pygame, random, time


class Collectible:
    def __init__(self, x: float, y: float, sprite: pygame.surface):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.rect = self.sprite.get_rect() # Create a rectangular collision for Collectible

    def update(self):
        pass

    def render(self, screen: pygame.Surface):
        screen.blit(self.sprite, (self.x, self.y))

    def randomize_position(self):
        # These make it so the collectable spawns randomly
        self.x = random.randint(50, 1250)
        self.y = random.randint(50, 670)
        self.rect.x = self.x
        self.rect.y = self.y


class Player:
    def __init__(self, x: float, y: float, sprite: pygame.surface):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.speed = 200
        self.angle = 0
        self.direction = "up"
        self.moving = False
        self.rect = self.sprite.get_rect() # Create a rectangular collision for player

    def update(self, delta_time):
        if self.moving:
            self.move(delta_time)
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def render(self, screen: pygame.Surface):
        # This is needed to render sprites on screen, the second argument is where the spirte loads in screen
        screen.blit(self.sprite, (self.x, self.y)) 

    def set_angle(self, new_angle: int):
        rotation = new_angle - self.angle
        self.sprite = pygame.transform.rotate(self.sprite, rotation)
        self.angle = new_angle

    def move(self, delta_time):
        # Adjust player movement direction
        if self.direction == "up":
            self.y -= self.speed * delta_time
        elif self.direction == "down":
            self.y += self.speed * delta_time
        elif self.direction == "left":
            self.x -= self.speed * delta_time
        elif self.direction == "right":
            self.x += self.speed * delta_time

        # set a boarder to prevent moving off the screen
        self.x = min((1230, self.x))
        self.x = max((0, self.x))

        self.y = min((670, self.y))
        self.y = max((0, self.y))


class Text:
    def __init__(self, x, y, text: str):
        self.x = x
        self.y = y
        self.text = text
        self.font = pygame.font.SysFont("Calibri", 36)

    def update(self):
        pass

    def render(self, screen: pygame.Surface):
        self.rendered = self.font.render(self.text, True, "white")
        screen.blit(self.rendered, (self.x, self.y))


class Game:
    def __init__(self):
        pygame.init() # intially sets up pygame
        self.running = True
        self.screen = pygame.display.set_mode((1280, 720)) # sets GUI resolution size
        self.sprites = self.load_sprites()
        self.score = 0
        self.player = Player(200, 200, self.sprites["spaceship"])

        # Create the collectible with a random start location
        self.collectible = Collectible(50, 50, self.sprites["collectible"])
        self.collectible.randomize_position()

        # Create scoreboard
        self.text = Text(600, 50, str(self.score))

        # Create movement buttons angle / direction
        self.keybinds = {
            pygame.K_w: (0, "up"),
            pygame.K_d: (270, "right"),
            pygame.K_s: (180, "down"),
            pygame.K_a: (90, "left")
        }

        # Load in background music and reduce volume
        pygame.mixer.music.load("sfx/music.ogg")
        pygame.mixer.music.set_volume(0.25)
        pygame.mixer.music.play()

        # set collectible sfx
        self.collect_sound = pygame.mixer.Sound("sfx/collect.wav")
        self.collect_sound.set_volume(0.25)

    def poll_events(self):
        # The game runs while running = true
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # Move character while key is being held down
            if event.type == pygame.KEYDOWN and event.key in self.keybinds:
                self.player.set_angle(self.keybinds[event.key][0])
                self.player.direction = self.keybinds[event.key][1]
                self.player.moving = True

            # Stop moving character if movement key stops being pressed
            if event.type == pygame.KEYUP and event.key in self.keybinds:
                if self.keybinds[event.key][1] == self.player.direction:
                    self.player.moving = False

    def update(self):
        # Compute delta time to prevent processing speed issue
        now = time.time()
        delta_time = now - self.previous_time
        self.previous_time = now

        self.player.update(delta_time)
        self.collectible.update()

        # If the player collides with an object the collectable randomly respawns elsewhere, increases player speed, and adds 1 to the score.
        if self.player.rect.colliderect(self.collectible.rect):
            self.collectible.randomize_position()
            self.player.speed += 100
            self.collect_sound.play()
            self.score += 1

        self.text.update()
        self.text.text = str(self.score)

    def render(self):
        # create the gameboard filling everything in back to front. Background, player, text, collectible
        self.screen.fill("black")
        self.screen.blit(self.sprites["background"], (0,0))
        self.player.render(self.screen)
        self.collectible.render(self.screen)
        self.text.render(self.screen)

        pygame.display.update()

    def run(self):
        self.previous_time = time.time()
        while self.running:
            self.poll_events()
            self.update()
            self.render()
        pygame.quit()

    def load_sprites(self) -> dict:
        sprites = {}
        sprites["spaceship"] = pygame.image.load("gfx/ship.png").convert_alpha() # convert_alpha is required because it has transparency
        sprites["background"] = pygame.image.load("gfx/simple_game_bg.png").convert_alpha()
        sprites["collectible"] = pygame.image.load("gfx/collectible.png").convert_alpha()

        # Downscale
        sprites["spaceship"] = pygame.transform.scale(sprites["spaceship"], (48, 48))

        return sprites

run_game = Game()
run_game.run()
