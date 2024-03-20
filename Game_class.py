import datetime,json,random,pygame
from Background_class import Background
from Bonus_class import Bonus
from Control_class import Control
from Enemy_class import Enemy
from Explosion_class import Explosion
from Player_class import Player
from const import (BLACK, FPS, HEALTH_STATE, GAME_STATE, MAX_TUTO_STEP, SCORE_FONT, SCORE_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH, BONUS_RATE_MIN, BONUS_RATE_MAX, NB_ENNEMY_ALLOWED_TO_PASS, TUTO_DURATION, MIN_ENEMY_DELAY, MAX_ENEMY_DELAY)
from Menu import Menu
from Reward_class import Reward
from Idle_class import Idle
from Statistics import Statistics

class Game():

    apparition_rate = datetime.datetime.now() + datetime.timedelta(seconds=random.randint(0, 7))
    apparition_rate_bonus = datetime.datetime.now() + datetime.timedelta(seconds=random.randint(BONUS_RATE_MIN, BONUS_RATE_MAX))

    def __init__(self):
        super().__init__() 
        # pygame setup
        pygame.init()
        pygame.mouse.set_visible(False)
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

        #Setting up Fonts
        self.font = pygame.font.SysFont("Verdana", 30)
        self.font_small = pygame.font.SysFont("Verdana", 20)
        self.waiting_verre = [self.font.render("Placer un verre", True, BLACK),
                              self.font.render("pour demarrer", True, BLACK)]
        self.font_score = pygame.font.Font("src/fonts/" + SCORE_FONT, SCORE_SIZE)
        self.menu = Menu()
        self.reward = Reward()
        self.idle = Idle()
        self.statistics = Statistics()

        self.start_time = datetime.datetime.now()
        self.reset()


    def reset(self):
        self.state = GAME_STATE.MENU

        self.score = 0
        self.tuto_step = 0        

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
        # self.player.blit(self.screen)
        # self.menu.render(self.screen)
        if self.state == GAME_STATE.MENU:
            self.statistics.render(self.screen)
            self.menu.render(self.screen)

        if self.state == GAME_STATE.IDLE:
            # self.player.blit(self.screen)
            # self.display_waiting()
            self.idle.render(self.screen)
            return
        if self.state == GAME_STATE.REWARD:
            self.reward.render(self.screen)
            return

        for enemy in self.enemies:
            enemy.blit(self.screen)

        self.playerBullets.draw(self.screen)
        self.enemyBullets.draw(self.screen)
        self.explosions.draw(self.screen)
        if self.state != GAME_STATE.MENU:
            self.bonus.draw(self.screen)
            self.player.blit(self.screen)
            self.display_score = self.font_score.render("SCORE: " + str(self.score), True, BLACK)
            self.screen.blit(self.display_score, ((SCREEN_WIDTH / 2) - (self.display_score.get_rect().width / 2), 20))

        return

    def exit_requested(self):
        return not pygame.get_init()

    def update(self):
        if self.state == GAME_STATE.IDLE:
            print("idle")
            pass

        if self.state == GAME_STATE.MENU:
            if self.control.shoot():
                self.player.set_player_school(self.menu.chose_school())
                self.start_time = datetime.datetime.now()
                self.state = GAME_STATE.TUTO
                self.player.animate()
            if self.control.up():
                self.menu.move("UP")
            if self.control.down():
                self.menu.move("DOWN")
            if self.control.left():
                self.menu.move("LEFT")
            if self.control.right():
                self.menu.move("RIGHT")

        self.background.animate(self.state != GAME_STATE.IDLE and self.state != GAME_STATE.MENU)
        self.background.update()

        self.player.update(self.playerBullets)

        if self.state == GAME_STATE.TUTO or self.state == GAME_STATE.RUNNING or self.state==GAME_STATE.ENDING:
            self.playerBullets.update()
            self.enemyBullets.update()
            self.explosions.update()
            self.enemies.update(self.enemyBullets)
            
        self.collisions()
        self.spawn()

        # if self.state == GAME_STATE.TUTO:
        #     if datetime.datetime.now() - self.start_time >= datetime.timedelta(TUTO_DURATION):
        #         self.state = GAME_STATE.RUNNING
                        
        if self.player.is_dead():
            self.state=GAME_STATE.ENDING
            
        if self.state==GAME_STATE.ENDING and len(self.explosions) == 0:
            self.statistics.add_score(self.score,self.player.school)
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

    def spawn(self):
        if self.state!=GAME_STATE.TUTO and self.state!=GAME_STATE.RUNNING:
            return

        if self.state==GAME_STATE.TUTO:
            if(len(self.enemies) == 0 and self.player.is_alive()):
                if self.tuto_step == 0 or self.tuto_step == 1:
                    self.enemies.add(Enemy(list(self.enemiesAttributes.values())[0])) 
                if self.tuto_step == 2:
                    self.enemies.add(Enemy(list(self.enemiesAttributes.values())[0])) 
                    self.enemies.add(Enemy(list(self.enemiesAttributes.values())[1])) 
                    self.enemies.add(Enemy(list(self.enemiesAttributes.values())[2]))
                if self.tuto_step == 3:
                    self.enemies.add(Enemy(list(self.enemiesAttributes.values())[3]))
                    bonus = random.choices(list(self.bonusAttributes.values()),
                                           [val["weight"] for val in self.bonusAttributes.values()], k=1)[0]
                    self.bonus.add(Bonus(bonus))
                if self.tuto_step == 4:
                    self.enemies.add(Enemy(list(self.enemiesAttributes.values())[6]))
                if self.tuto_step == 5:
                    if (len(self.enemies) != 0 ) :
                        return
                    else:
                        bonus = random.choices(list(self.bonusAttributes.values()),
                                               [val["weight"] for val in self.bonusAttributes.values()], k=1)[0]
                        self.bonus.add(Bonus(bonus))
                        bonus = random.choices(list(self.bonusAttributes.values()),
                                               [val["weight"] for val in self.bonusAttributes.values()], k=1)[0]
                        self.bonus.add(Bonus(bonus))
                        bonus = random.choices(list(self.bonusAttributes.values()),
                                               [val["weight"] for val in self.bonusAttributes.values()], k=1)[0]
                        self.bonus.add(Bonus(bonus))
                self.tuto_step += 1

            if self.tuto_step >= MAX_TUTO_STEP:
                Game.apparition_rate = datetime.datetime.now() + datetime.timedelta(seconds=random.randint(MIN_ENEMY_DELAY, MAX_ENEMY_DELAY))
                Game.apparition_rate_bonus = datetime.datetime.now() + datetime.timedelta(seconds=random.randint(BONUS_RATE_MIN, BONUS_RATE_MAX))
                self.state = GAME_STATE.RUNNING
            return
                                      
        if Game.apparition_rate <= datetime.datetime.now():
            self.enemies.add(Enemy(random.choice(list(self.enemiesAttributes.values()))))
            Game.apparition_rate += datetime.timedelta(seconds=random.randint(MIN_ENEMY_DELAY, MAX_ENEMY_DELAY))
        if(len(self.enemies) == 0 and self.player.is_alive()):
            self.enemies.add(Enemy(random.choice(list(self.enemiesAttributes.values()))))

        if Game.apparition_rate_bonus <= datetime.datetime.now():
            bonus = random.choices(list(self.bonusAttributes.values()), [val["weight"] for val in self.bonusAttributes.values()], k=1)[0]                
            self.bonus.add(Bonus(bonus))
            Game.apparition_rate_bonus += datetime.timedelta(seconds=random.randint(BONUS_RATE_MIN, BONUS_RATE_MAX))

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
                self.player.receive_damage(self.player.max_health / NB_ENNEMY_ALLOWED_TO_PASS)
                enemy.kill()
            if enemy.is_dead():
                self.explosions.add(Explosion(enemy.pos))
                enemy.kill()
                self.score += enemy.points
    def idleMode(self):
        self.state = GAME_STATE.IDLE
    def menuMode(self):
        self.state = GAME_STATE.MENU

    def isIdle(self):
        return self.state == GAME_STATE.IDLE

    def rewardMode(self):
        self.state = GAME_STATE.REWARD