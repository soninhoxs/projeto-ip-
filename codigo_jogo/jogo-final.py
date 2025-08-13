import pygame
import random

DEBUG_MODE = False  # hitboxes

# CONSTANTES
WIDTH, HEIGHT = 1400, 900
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
BROWN = (165, 42, 42)
YELLOW = (255, 255, 0)
GREEN = (0, 180, 0)
GRAY = (150, 150, 150)
BLUE = (0, 100, 200)
FPS = 60

# CLASSE DO JOGADOR
class Player:
    def __init__(self, x, y, img_left, img_right, img_front, width, height, speed=7):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image_left = img_left
        self.image_right = img_right
        self.image_front = img_front
        self.image = self.image_front
        self.base_speed = speed
        self.speed = speed
        self.hitbox_offset_x = 20
        self.hitbox_offset_y = 20
        self.hitbox_width = self.width - 40
        self.hitbox_height = self.height - 30

        # Variáveis para o pulo
        self.is_jumping = False
        self.y_velocity = 0
        self.gravity = 1
        self.jump_strength = -20
        self.ground_y = y  # Posição inicial no chão
        
        # Variáveis para lentidão
        self.slowed_timer = 0
        self.SLOWED_DURATION = 300  # 5 segundos
        
        # Variáveis para o contador de hotdogs
        self.hotdogs_eaten = 0 

    def update(self, keys):
        # Lógica para o timer de lentidão
        if self.slowed_timer > 0:
            self.slowed_timer -= 1
            if self.slowed_timer == 0:
                self.speed = self.base_speed  # Voltar a velocidade normal

        # Movimento horizontal
        moved = False
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
            self.x = max(self.x, 0)
            self.image = self.image_left
            moved = True

        if keys[pygame.K_RIGHT]:
            self.x += self.speed
            self.x = min(self.x, WIDTH - self.width)
            self.image = self.image_right
            moved = True

        # Se o jogador não se moveu horizontalmente, usa a imagem de frente
        if not moved:
            self.image = self.image_front

        # Lógica do pulo
        if keys[pygame.K_SPACE] and not self.is_jumping:
            self.is_jumping = True
            self.y_velocity = self.jump_strength

        # Aplica gravidade se estiver pulando ou no ar
        if self.is_jumping or self.y < self.ground_y:
            self.y += self.y_velocity
            self.y_velocity += self.gravity

        # Checa se o personagem voltou para o chão principal
        if self.y >= self.ground_y:
            self.y = self.ground_y
            self.is_jumping = False
            self.y_velocity = 0

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
        if DEBUG_MODE:
            pygame.draw.rect(surface, RED, self.get_rect(), 2)

    def get_rect(self):
        return pygame.Rect(
            self.x + self.hitbox_offset_x,
            self.y + self.hitbox_offset_y,
            self.hitbox_width,
            self.hitbox_height
        )

# CLASSE DOS ITENS
class Item:
    def __init__(self, x, y, kind, images):
        self.x = x
        self.y = y
        self.kind = kind
        self.speed = random.randint(3, 6)

        # Associa a imagem correta 
        self.image = images[kind]
        self.size = self.image.get_width()

        # Define a hitbox de acordo com o tipo de item
        hitbox_offsets = {
            "burger": (10, 10, self.size - 20, self.size - 20),
            "bomb": (30, 30, 60, 60),
            "hotdog": (10, 10, self.size - 20, self.size - 20),
            "donuts": (10, 10, self.size - 20, self.size - 20)
        }
        self.hitbox_offset_x, self.hitbox_offset_y, self.hitbox_width, self.hitbox_height = hitbox_offsets.get(kind, (0, 0, self.size, self.size))

    def fall(self):
        self.y += self.speed

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
        if DEBUG_MODE:
            color = GREEN if self.kind in ["burger", "donuts"] else YELLOW if self.kind == "bomb" else RED
            pygame.draw.rect(surface, color, self.get_rect(), 2)

    def get_rect(self):
        return pygame.Rect(
            self.x + self.hitbox_offset_x,
            self.y + self.hitbox_offset_y,
            self.hitbox_width,
            self.hitbox_height
        )

# CLASSE DO JOGO
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Tá Chovendo Hambúrguer - Flinn")
        self.clock = pygame.time.Clock()

        # Estados
        self.state = "menu"
        self.fase_1_completed = False
        self.score = 0
        self.items = []
        self.spawn_timer = 0
        self.spawn_interval = 30
        self.WIN_SCORE_FASE_1 = 15 # Ganhar na primeira fase
        self.WIN_SCORE_FASE_2 = 10 # Ganhar na segunda fase
        self.chosen_character = "flinn"
        self.lives = 3
        self.heart_image = None
        
        self.player_width = 120
        self.player_height = 160
        self.char_select_width = 300
        self.char_select_height = 390
        
        self.load_assets()

        # Dicionário de imagens para passar para a classe Item
        self.item_images = {
            "burger": self.burger_image,
            "bomb": self.bomb_image,
            "donuts": self.donuts_image,
            "hotdog": self.hotdog_image
        }

        self.player = Player(
            WIDTH // 2 - self.player_width // 2,
            HEIGHT - self.player_height - 10,
            self.flinn_jogo_image_left,
            self.flinn_jogo_image_right,
            self.flinn_jogo_image_front,
            self.player_width,
            self.player_height
        )

        self.char1_pos = (WIDTH // 4 - self.char_select_width // 2, HEIGHT // 2 - self.char_select_height // 2 + 50)
        self.char2_pos = (3 * WIDTH // 4 - self.char_select_width // 2, HEIGHT // 2 - self.char_select_height // 2 + 50)

    def load_assets(self): # Imagens
        try:
            self.menu_background = pygame.transform.scale(pygame.image.load("tela_inicial.png").convert_alpha(), (WIDTH, HEIGHT))
            self.background_image = pygame.transform.scale(pygame.image.load("tela_fasesn.png").convert(), (WIDTH, HEIGHT))
            self.fase1_wallpaper = pygame.transform.scale(pygame.image.load("tela_fase1.jpg").convert_alpha(), (WIDTH, HEIGHT))
            self.fase2_wallpaper = pygame.transform.scale(pygame.image.load("tela_fase2.jpg").convert_alpha(), (WIDTH, HEIGHT))
            self.escolha_wallpaper = pygame.transform.scale(pygame.image.load("escolhapersonagens.png").convert_alpha(), (WIDTH, HEIGHT))
            self.instrucoes_wallpaper = pygame.transform.scale(pygame.image.load("instrucoes.png").convert_alpha(), (WIDTH, HEIGHT))
            self.game_over_wallpaper = pygame.transform.scale(pygame.image.load("tela_perdeu.png").convert_alpha(), (WIDTH, HEIGHT))
            self.game_win_wallpaper = pygame.transform.scale(pygame.image.load("fim_jogo.png").convert_alpha(), (WIDTH, HEIGHT)) 
            self.restart_button_image = pygame.transform.scale(pygame.image.load("restart.png").convert_alpha(), (100, 100))
            self.continue_button_image = pygame.transform.scale(pygame.image.load("seta_continuar.png").convert_alpha(), (150, 130))

            self.flinn_image_left_select = pygame.transform.scale(pygame.image.load("flinn.png").convert_alpha(), (self.char_select_width, self.char_select_height))
            self.flinn_image_right_select = pygame.transform.flip(self.flinn_image_left_select, True, False)

            self.macaco_image_left_select = pygame.transform.scale(pygame.image.load("macaco.png").convert_alpha(), (self.char_select_width, self.char_select_height))
            self.macaco_image_right_select = pygame.transform.flip(self.macaco_image_left_select, True, False)

            self.macaco_jogo_image_left = pygame.transform.scale(pygame.image.load("macaco_jogo.png").convert_alpha(), (self.player_width, self.player_height))
            self.macaco_jogo_image_right = pygame.transform.flip(self.macaco_jogo_image_left, True, False)
            self.macaco_jogo_image_front = self.macaco_jogo_image_left

            self.flinn_jogo_image_left = pygame.transform.scale(pygame.image.load("personagem2.png").convert_alpha(), (self.player_width, self.player_height))
            self.flinn_jogo_image_right = pygame.transform.scale(pygame.image.load("personagem.png").convert_alpha(), (self.player_width, self.player_height))
            self.flinn_jogo_image_front = pygame.transform.scale(pygame.image.load("flinn_frente.png").convert_alpha(), (self.player_width, self.player_height))

            self.burger_size = 80
            self.bomb_size = 120
            self.hotdog_size = 80
            
            self.burger_image = pygame.transform.scale(pygame.image.load("hamburguer.png").convert_alpha(), (self.burger_size, self.burger_size))
            self.bomb_image = pygame.transform.scale(pygame.image.load("bomba.png").convert_alpha(), (self.bomb_size, self.bomb_size))
            self.hotdog_image = pygame.transform.scale(pygame.image.load("cachorro_quente_mofado.png").convert_alpha(), (self.hotdog_size, self.hotdog_size))
            
            loaded_donuts_image = pygame.image.load("donut.png").convert_alpha()
            self.donuts_image = pygame.transform.scale(loaded_donuts_image, (80, 80))

            self.heart_image = pygame.transform.scale(pygame.image.load("coracao.png").convert_alpha(), (80, 80))
            self.play_button_image = pygame.transform.scale(pygame.image.load("botao_play.png").convert_alpha(), (350, 400))
            self.poison_hotdog_image = pygame.transform.scale(pygame.image.load("cachorro_quente_mofado.png").convert_alpha(), (80, 80)) 

            # FONTE
            self.font_fases = pygame.font.Font("Pixeled.ttf", 35)
            self.font_game_over = pygame.font.Font("Pixeled.ttf", 40)
            self.font_button = pygame.font.Font("Pixeled.ttf", 25)
            self.font_timer = pygame.font.Font("Pixeled.ttf", 30) 

        except pygame.error as e:
            print(f"Erro ao carregar a imagem ou fonte: {e}")
            pygame.quit()
            exit()

    def reset_game(self):
        self.score = 0
        self.items = []
        self.player.x = WIDTH // 2 - self.player.width // 2
        self.player.y = self.player.ground_y
        self.player.is_jumping = False
        self.player.y_velocity = 0
        self.lives = 3
        self.player.speed = self.player.base_speed # Garante que a velocidade do jogador é restaurada
        self.player.hotdogs_eaten = 0 

    def spawn_item(self):
        size = 80 
        x_pos = random.randint(0, WIDTH - size)
        
        if self.state == 'fase_1_playing':
            # 10% cachorro-quente mofado
            if random.random() < 0.1:
                kind = "hotdog"
            else:
                # 90% restante
                # 54% hambúrguer
                # 36% bomba
                kind = "burger" if random.random() < 0.6 else "bomb"
                
        elif self.state == 'fase_2_playing':
            # 80% de chance de ser uma bomba
            # 20% de chance de ser um donut
            kind = "bomb" if random.random() < 0.8 else "donuts"
        else:
            return
            
        self.items.append(Item(x_pos, -100, kind, images=self.item_images))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if self.state == 'menu':
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.draw_menu().collidepoint(event.pos):
                        self.state = 'instrucoes'

            elif self.state == 'instrucoes':
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.draw_continue_button().collidepoint(event.pos):
                        self.state = 'escolha_personagem'

            elif self.state == 'escolha_personagem':
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    char1_rect = pygame.Rect(self.char1_pos[0], self.char1_pos[1], self.char_select_width,
                                             self.char_select_height)
                    char2_rect = pygame.Rect(self.char2_pos[0], self.char2_pos[1], self.char_select_width,
                                             self.char_select_height)

                    if char1_rect.collidepoint(event.pos):
                        self.chosen_character = "flinn"
                        self.player.image_left = self.flinn_jogo_image_left
                        self.player.image_right = self.flinn_jogo_image_right
                        self.player.image_front = self.flinn_jogo_image_front
                        self.player.hitbox_offset_x = 20
                        self.player.hitbox_offset_y = 20
                        self.player.hitbox_width = self.player_width - 40
                        self.player.hitbox_height = self.player_height - 30
                        self.player.image = self.player.image_front
                        self.state = 'fases'
                    elif char2_rect.collidepoint(event.pos):
                        self.chosen_character = "macaco"
                        self.player.image_left = self.macaco_jogo_image_left
                        self.player.image_right = self.macaco_jogo_image_right
                        self.player.image_front = self.macaco_jogo_image_front
                        self.player.hitbox_offset_x = 30
                        self.player.hitbox_offset_y = 40
                        self.player.hitbox_width = self.player_width - 60
                        self.player.hitbox_height = self.player_height - 60
                        self.player.image = self.player.image_front
                        self.state = 'fases'

            elif self.state == 'fases':
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    fase1_button_rect, fase2_button_rect = self.draw_fases()
                    if fase1_button_rect.collidepoint(event.pos):
                        self.reset_game()
                        self.state = 'fase_1_playing'
                    if self.fase_1_completed and fase2_button_rect.collidepoint(event.pos):
                        self.reset_game()
                        self.state = 'fase_2_playing'

            elif self.state == 'game_over' or self.state == 'game_win': # Estado de vitória
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    restart_button_rect = self.draw_restart_button()
                    if restart_button_rect.collidepoint(event.pos):
                        self.reset_game()
                        self.state = 'fases'

        return True

    def update(self):
        keys = pygame.key.get_pressed()

        if self.state == 'fase_1_playing':
            self.player.update(keys)

            self.spawn_timer += 1
            if self.spawn_timer >= self.spawn_interval:
                self.spawn_timer = 0
                self.spawn_item()

            player_rect = self.player.get_rect()
            for item in self.items[:]:
                item.fall()
                if item.y > HEIGHT:
                    self.items.remove(item)
                elif player_rect.colliderect(item.get_rect()):
                    if item.kind == "burger":
                        self.score += 1
                        self.items.remove(item)
                    elif item.kind == "bomb":
                        self.lives -= 1
                        self.items.remove(item)
                        if self.lives <= 0:
                            self.state = 'game_over'
                    elif item.kind == "hotdog":  # Cachorro-quente mofado
                        self.player.speed = self.player.base_speed // 2  # Reduz a velocidade
                        self.player.slowed_timer = self.player.SLOWED_DURATION
                        self.player.hotdogs_eaten += 1 
                        self.items.remove(item)

            if self.score >= self.WIN_SCORE_FASE_1:
                self.fase_1_completed = True
                self.state = 'fases'

        elif self.state == 'fase_2_playing':
            self.player.update(keys)
            self.spawn_timer += 1
            if self.spawn_timer >= self.spawn_interval:
                self.spawn_timer = 0
                self.spawn_item()

            player_rect = self.player.get_rect()
            for item in self.items[:]:
                item.fall()
                if item.y > HEIGHT:
                    self.items.remove(item)
                elif player_rect.colliderect(item.get_rect()):
                    if item.kind == "donuts":
                        self.score += 1
                        self.items.remove(item)
                    elif item.kind == "bomb":
                        self.lives -= 1
                        self.items.remove(item)
                        if self.lives <= 0:
                            self.state = 'game_over'

            if self.score >= self.WIN_SCORE_FASE_2:
                self.state = 'game_win' # Estado de vitória da Fase 2

    def draw_text(self, text, x, y, color=BLACK, centered=False, font_size=36):
        font = pygame.font.SysFont(None, font_size)
        img = font.render(text, True, color)
        text_rect = img.get_rect()
        if centered:
            text_rect.center = (x, y)
        else:
            text_rect.topleft = (x, y)
        self.screen.blit(img, text_rect)
        return text_rect

    def draw_menu(self):
        self.screen.blit(self.menu_background, (0, 0))
        button_rect = self.play_button_image.get_rect(x=20, y=HEIGHT - 350)
        self.screen.blit(self.play_button_image, button_rect)
        return button_rect

    def draw_instrucoes(self):
        self.screen.blit(self.instrucoes_wallpaper, (0, 0))
        return self.draw_continue_button()

    def draw_continue_button(self):
        button_width, button_height = self.continue_button_image.get_size()
        button_x = WIDTH - button_width - 50
        button_y = 50
        button_rect = self.continue_button_image.get_rect(topleft=(button_x, button_y))
        self.screen.blit(self.continue_button_image, button_rect)
        return button_rect

    def draw_escolha_personagem(self):
        self.screen.blit(self.escolha_wallpaper, (0, 0))
        self.draw_text("Escolha seu personagem", WIDTH // 2, HEIGHT // 4, BLACK, centered=True, font_size=50)
        self.screen.blit(self.flinn_image_left_select, self.char1_pos)
        font_flint = pygame.font.SysFont(None, 45)
        text_flint = font_flint.render("Flint Lockwood", True, WHITE)
        text_flint_rect = text_flint.get_rect(center=(self.char1_pos[0] + self.char_select_width // 2, self.char1_pos[1] + self.char_select_height + 40))
        frame_flint_rect = text_flint_rect.inflate(40, 15)
        pygame.draw.rect(self.screen, BLACK, frame_flint_rect, border_radius=10)
        pygame.draw.rect(self.screen, WHITE, frame_flint_rect, 2, border_radius=10)
        self.screen.blit(text_flint, text_flint_rect)
        self.screen.blit(self.macaco_image_left_select, self.char2_pos)
        font_macaco = pygame.font.SysFont(None, 45)
        text_macaco = font_macaco.render("Macaco Steve", True, WHITE)
        text_macaco_rect = text_macaco.get_rect(center=(self.char2_pos[0] + self.char_select_width // 2, self.char2_pos[1] + self.char_select_height + 40))
        frame_macaco_rect = text_macaco_rect.inflate(40, 15)
        pygame.draw.rect(self.screen, BLACK, frame_macaco_rect, border_radius=10)
        pygame.draw.rect(self.screen, WHITE, frame_macaco_rect, 2, border_radius=10)
        self.screen.blit(text_macaco, text_macaco_rect)
        if DEBUG_MODE:
            char1_rect = pygame.Rect(self.char1_pos[0], self.char1_pos[1], self.char_select_width, self.char_select_height)
            char2_rect = pygame.Rect(self.char2_pos[0], self.char2_pos[1], self.char_select_width, self.char_select_height)
            pygame.draw.rect(self.screen, RED, char1_rect, 2)
            pygame.draw.rect(self.screen, RED, char2_rect, 2)

    def draw_fases(self):
        self.screen.blit(self.background_image, (0, 0))
        button_width, button_height = 300, 80
        button_x = WIDTH - button_width - 150
        spacing = 80
        total_button_height = (button_height * 2) + spacing
        start_y = (HEIGHT - total_button_height) // 2
        fase1_rect = pygame.Rect(button_x, start_y, button_width, button_height)
        pygame.draw.rect(self.screen, BLUE, fase1_rect, border_radius=20)
        img = self.font_fases.render("Fase 1", True, WHITE)
        text_rect = img.get_rect(center=(fase1_rect.centerx, fase1_rect.centery))
        self.screen.blit(img, text_rect)
        fase2_rect = pygame.Rect(button_x, start_y + button_height + spacing, button_width, button_height)
        color = BLUE if self.fase_1_completed else GRAY
        pygame.draw.rect(self.screen, color, fase2_rect, border_radius=20)
        img = self.font_fases.render("Fase 2", True, WHITE)
        text_rect = img.get_rect(center=(fase2_rect.centerx, fase2_rect.centery))
        self.screen.blit(img, text_rect)
        return fase1_rect, fase2_rect

    def draw_hearts(self):
        heart_x = WIDTH - 90
        heart_y = 10
        for i in range(self.lives):
            self.screen.blit(self.heart_image, (heart_x - (i * 60), heart_y))

    def draw_restart_button(self):
        button_width, button_height = self.restart_button_image.get_size()
        button_x = WIDTH - button_width - 20
        button_y = 20
        restart_rect = self.restart_button_image.get_rect(topleft=(button_x, button_y))
        self.screen.blit(self.restart_button_image, restart_rect)
        return restart_rect

    def draw_hotdog_counter(self):
        self.screen.blit(self.poison_hotdog_image, (10, 80)) 
        self.draw_text(f"{self.player.hotdogs_eaten}", 10 + self.poison_hotdog_image.get_width() + 10,
                       80 + self.poison_hotdog_image.get_height() // 2, color=WHITE, font_size=40, centered=True)

    def draw_slow_timer(self):
        if self.player.slowed_timer > 0:
            remaining_time = self.player.slowed_timer / FPS # Converte frames para segundos
            text = f"{remaining_time:.1f}s"
            self.draw_text(text, WIDTH - 10, HEIGHT - 30, color=WHITE, font_size=30, centered=False)

    def draw(self):
        self.screen.fill(BLACK)
        if self.state == 'menu':
            self.draw_menu()
        elif self.state == 'instrucoes':
            self.draw_instrucoes()
        elif self.state == 'escolha_personagem':
            self.draw_escolha_personagem()
        elif self.state == 'fases':
            self.screen.blit(self.background_image, (0, 0))
            self.draw_fases()
        elif self.state == 'fase_1_playing' or self.state == 'fase_2_playing':
            if self.state == 'fase_1_playing':
                self.screen.blit(self.fase1_wallpaper, (0, 0))
                # Imagem hambúrguer para o contador
                self.screen.blit(self.burger_image, (10, 10))
                self.draw_text(f"{self.score}", 10 + self.burger_image.get_width() + 10,
                               10 + self.burger_image.get_height() // 2, color=WHITE, font_size=40, centered=True)
                
                # Cachorro-quente como contador
                self.draw_hotdog_counter()
                
            elif self.state == 'fase_2_playing':
                self.screen.blit(self.fase2_wallpaper, (0, 0))
                # Imagem donut para o contador
                self.screen.blit(self.donuts_image, (10, 10))
                self.draw_text(f"{self.score}", 10 + self.donuts_image.get_width() + 10,
                               10 + self.donuts_image.get_height() // 2, color=WHITE, font_size=40, centered=True)

            if self.chosen_character == "flinn":
                self.player.image_left = self.flinn_jogo_image_left
                self.player.image_right = self.flinn_jogo_image_right
                self.player.image_front = self.flinn_jogo_image_front
            elif self.chosen_character == "macaco":
                self.player.image_left = self.macaco_jogo_image_left
                self.player.image_right = self.macaco_jogo_image_right
                self.player.image_front = self.macaco_jogo_image_front

            self.player.draw(self.screen)
            self.draw_hearts()

            # Time
            self.draw_slow_timer()
            
            for item in self.items:
                item.draw(self.screen)
        elif self.state == 'game_over':
            self.screen.blit(self.game_over_wallpaper, (0, 0))
            self.draw_restart_button()
        elif self.state == 'game_win': # Estado de vitória
            self.screen.blit(self.game_win_wallpaper, (0, 0))
            self.draw_restart_button()

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()

if __name__ == "__main__":
    Game().run()