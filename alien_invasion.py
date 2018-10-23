
import sys
import pygame
from pygame.sprite import Group

from settings import Settions
from ship import Ship
import game_functions as gf
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from bomb import Bomb

'''管理事件代码'''
def run_game():
    pygame.init()
    ai_settings = Settions()
    #screen = pygame.display.set_mode((1000,600))
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption("Alien Invassion")

    #创建一个用于存储游戏统计信息的实例
    stats = GameStats(ai_settings)
    stats.high_score = stats.get_high_score()
    sb = Scoreboard(ai_settings, screen, stats)

    #创建一首飞船
    ship = Ship(ai_settings,screen)
    #创建一个用于存储子弹的编组
    bullets = Group()
    bullets_sum = Group()
    #创建一个外星人编组
    #alien = Alien(ai_settings,screen)
    aliens = Group()
    aliens_hit = Group() #存放被击落的外星人编组
    # 创建爆炸对象
    bombs = [Bomb(screen) for _ in range(5)]
    #创建外星人群
    gf.create_fleet(ai_settings,screen,ship,aliens)

    #创建play按钮
    play_button = Button(ai_settings, screen, "play")
    #bg_color = (230,230,230)
    while True:
        '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        '''
        #gf.check_events(ship)
        # draw_elements(bombs)
        # action_elements(bombs)
        gf.check_events(ai_settings,screen,stats,sb, play_button, ship, aliens, bullets)
        if stats.game_active:
            ship.update()
            #bullets.update()

            #删除已消失的子弹,
            #不应从列表或编组中直接删除条目，应从副本里检索.copy()是调用副本
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, aliens_hit,bombs, bullets)
            gf.update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets)
            '''
            screen.fill(ai_settings.bg_color)
            ship.blitme()
            pygame.display.flip()
            '''
        #gf.update_screen(ai_settings,screen,ship)
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)


# # 绘制
# def draw_elements(bombs):
#     # 绘制爆炸图片
#     for bomb in bombs:
#         if bomb.visible:
#             bomb.draw()
#
#     # 动作
# def action_elements(bombs):
#     # 切换爆炸图片
#     for bomb in bombs:
#         if bomb.visible:
#             bomb.action()

run_game()
