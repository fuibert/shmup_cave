import datetime
import json
import random
import pygame
from Background_class import Background
from Bonus_class import Bonus
from Control_class import Control
from Enemy_class import Enemy
from Explosion_class import Explosion
from Player_class import Player
from const import BLACK, FPS, HEALTH_STATE, GAME_STATE, SCORE_FONT, SCORE_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH
from Menu import Menu
from Statistics import Statistics

class Game():

    apparition_rate = datetime.datetime.now() + datetime.timedelta(seconds=random.randint(0, 7))
    apparition_rate_bonus = datetime.datetime.now() + datetime.timedelta(seconds=random.randint(0, 7))

    def __init__(self):
        super().__init__() 
        # pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode((1080, 1920), pygame.FULLSCREEN | pygame.SCALED)
        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        if len(self.joysticks) > 1:
            print("too many joysticks, plug only one. Bouffon va")
            exit()
        self.clock = pygame.time.Clock()

        with open("attributes.json", "r") as f:
            data = json.loads(f.read())
            self.playerAttributes = data["player"]
            self.enemiesAttributes = data["enemies"]
            self.bonusAttributes = data["bonus"]   
        
        with open("score_board.json", "r") as f:
            self.score_board = json.loads(f.read())

        self.score_max = 0
        for item in self.score_board:
            if len(self.score_board[item]) > 0:
                if max(self.score_board[item]) > self.score_max:
                    self.score_max = max(self.score_board[item])
                    self.school_score_max = item


        #Setting up Fonts
        self.font = pygame.font.SysFont("Verdana", 30)
        self.font_small = pygame.font.SysFont("Verdana", 20)
        self.waiting_verre = [self.font.render("Placer un verre", True, BLACK),
                              self.font.render("pour demarrer", True, BLACK)]
        self.font_score = pygame.font.Font("src/fonts/" + SCORE_FONT, SCORE_SIZE)
        self.menu = Menu()
        self.statistics = Statistics()
        
        self.reset()

        self.reset()

    def reset(self):
        self.state = GAME_STATE.MENU
        self.score = 0

        if len(self.joysticks) > 0:
            self.player = Player(self.playerAttributes,self.joysticks[0])
            self.control = Control(self.joysticks[0])
        else:
            self.player = Player(self.playerAttributes,None)
            self.control = Control(None)
            
        SCREEN_WIDTH, SCREEN_HEIGHT = self.screen.get_size()
        
        self.background = Background(SCREEN_WIDTH)
        self.playerBullets = pygame.sprite.Group()
        self.enemyBullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bonus = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.statistics.reset(self.score_board)
        self.menu.reset()

    def check_exit(self):
        if not pygame.get_init():
            return False
        if self.control.escape():
            pygame.quit()
            return True

        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
        return False

    def display_waiting(self):
        self.screen.blit(self.waiting_verre[0], 
                         ((SCREEN_WIDTH - self.waiting_verre[0].get_rect().width) / 2,
                         SCREEN_HEIGHT / 2 + 15))
        self.screen.blit(self.waiting_verre[1], 
                         ((SCREEN_WIDTH - self.waiting_verre[0].get_rect().width) / 2,
                         SCREEN_HEIGHT / 2 - 15))

    def render(self):
        self.background.render(self.screen)        
        self.player.blit(self.screen)
        # self.menu.render(self.screen)
        if self.state == GAME_STATE.MENU:
            self.statistics.render(self.screen)
            self.menu.render(self.screen)
            
        if self.state == GAME_STATE.IDLE:
            self.player.blit(self.screen)
            self.display_waiting()
            return

        for enemy in self.enemies:
            enemy.blit(self.screen)

        self.playerBullets.draw(self.screen)
        self.enemyBullets.draw(self.screen)
        self.explosions.draw(self.screen)
        self.bonus.draw(self.screen)
            
        self.display_score = self.font_score.render("SCORE: " + str(self.score), True, BLACK)
        self.screen.blit(self.display_score, ((SCREEN_WIDTH / 2) - (self.display_score.get_rect().width / 2), 20))

        self.player.blit(self.screen)
        return

    def exit_requested(self):
        return not pygame.get_init()

    def update(self):
        if self.state == GAME_STATE.IDLE:
            if self.control.shoot():
                self.state = GAME_STATE.TUTO
                self.player.animate()

        if self.state == GAME_STATE.MENU:
            if self.control.shoot():
                self.player.set_player_school(self.menu.chose_school("SHOOT"))
                self.state = GAME_STATE.IDLE
            if self.control.up():
                self.menu.chose_school("UP")
            if self.control.down():
                self.menu.chose_school("DOWN")
            if self.control.left():
                self.menu.chose_school("LEFT")
            if self.control.right():
                self.menu.chose_school("RIGHT")

        self.background.animate(self.state != GAME_STATE.IDLE)
        self.background.update()

        self.player.update(self.playerBullets)

        if self.state == GAME_STATE.TUTO or self.state == GAME_STATE.RUNNING or self.state==GAME_STATE.ENDING:
            self.playerBullets.update()
            self.enemyBullets.update()
            self.explosions.update()
            self.enemies.update(self.enemyBullets)
            
        self.collisions()
        self.spawn()                    

        if self.player.is_dead():
            self.state=GAME_STATE.ENDING
            
        if self.state==GAME_STATE.ENDING and len(self.explosions) == 0:
            self.score_board[self.player.school].append(self.score)
            self.store_score()
            self.state = GAME_STATE.ENDED
            return

    def loop(self):
        if self.check_exit():
            return

        # fill the screen with a color to wipe away anything from last frame
        self.update()
        # RENDER YOUR GAME HERE
        self.render()

        # flip() the display to put your work on screen
        pygame.display.flip()
    
        self.clock.tick(FPS)  # limits FPS to 60

    def store_score(self):
        if self.score_max < self.score:
            self.score_max = self.score
            self.school_score_max = self.player.school
        with open("score_board.json", "w") as f:
            f.write(json.dumps(self.score_board))

    def spawn(self):
        if self.state==GAME_STATE.ENDED or self.state==GAME_STATE.ENDING:
            return                    
 #           if Game.apparition_rate <= datetime.datetime.now():
 #               self.enemies.add(Enemy(random.choice(list(self.enemiesAttributes.values()))))
 #               Game.apparition_rate += datetime.timedelta(seconds=randint(0, 7))
        if(len(self.enemies) == 0 and self.player.is_alive()):
            self.enemies.add(Enemy(random.choice(list(self.enemiesAttributes.values()))))

        if Game.apparition_rate_bonus <= datetime.datetime.now():
            bonus = random.choices(list(self.bonusAttributes.values()), [val["weight"] for val in self.bonusAttributes.values()], k=1)[0]                
            self.bonus.add(Bonus(bonus))
            Game.apparition_rate_bonus += datetime.timedelta(seconds=random.randint(0, 7))

    def collisions(self):
        for bonus in self.bonus:
            bonus.update()
        for hit in pygame.sprite.spritecollide(self.player, self.enemyBullets, False, pygame.sprite.collide_mask): # type: ignore
            self.player.hit(hit)

        for bonus in pygame.sprite.spritecollide(self.player, self.bonus, False, pygame.sprite.collide_mask): # type: ignore
            self.player.add_bonus(bonus)
            bonus.kill()

        if not self.player.is_dead():
            for enemy in pygame.sprite.spritecollide(self.player, self.enemies, False, pygame.sprite.collide_mask): # type: ignore
                self.explosions.add(Explosion(self.player.pos))
                self.player.receive_damage(self.player.health)
                enemy.kill()
                break                    

        for enemy in self.enemies:
            for hit in pygame.sprite.spritecollide(enemy, self.playerBullets, False,  pygame.sprite.collide_mask): # type: ignore
                enemy.hit(hit)
            if enemy.passed():
                self.player.receive_damage(10)
                enemy.kill()
            if enemy.is_dead():
                self.explosions.add(Explosion(enemy.pos))
                enemy.kill()
                self.score += enemy.points