
import sys
import pygame
from time import sleep

from bullet import Bullet
from alien import Alien

def check_keydown_events(event,ai_settings,screen,ship,bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        #创建一颗子弹，并将其加入到编组bullets
        fire_bullet(ai_settings,screen,ship,bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event,ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings,screen,stats,sb, play_button, ship, aliens, bullets):
    """响应键盘和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            #check_keydown_events(event,ship)
            check_keydown_events(event,ai_settings,screen,ship,bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """在玩家单击play按钮时开始新游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        #隐藏光标
        pygame.mouse.set_visible(False)
        #重置游戏设置
        ai_settings.initialize_dynamic_settings()
        #重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True

        #重置积分牌图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()

        sb.prep_ships()

        #清空子弹和外星人列表
        bullets.empty()
        aliens.empty()

        #创建一群新的外星人，并让飞船居中
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

def fire_bullet(ai_settings,screen,ship,bullets):
    """如果还没有达到限制就发射一颗子弹"""
    if ai_settings.bullet_sum < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
        ai_settings.bullet_sum += 1

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, aliens_hit, bombs, bullets):
    """响应子弹和外星人的碰撞"""
    #删除发生碰撞的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, False, True)
    aliens_hit.add(collisions)
    #有时当一个子弹消灭两个外星人时，统计的也是一个，这里需要改变算法，所有被击落的外星人都存放在字典collisions中，
    # 遍历字典可以累加被击落的外星人
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points*len(aliens)
            sb.prep_score()
            #aliens_hit.add(aliens)
            #显示爆炸图片
            #display(ai_settings, screen, aliens.rect)

        # 从预先创建完毕的爆炸中取出一个爆炸对象
        # for aliens_var in aliens_hit:
        #     #print(aliens_var)
        #     #print(aliens_var.rect[0])
        #     #print(aliens_var.rect[1])
        #     for bomb in bombs:
        #         print('爆炸')
        #         if not bomb.visible:
        #             print('启动！')
        #             # 爆炸对象设置爆炸位置
        #             bomb.set_pos(aliens_var.rect[0], aliens_var.rect[1])
        #             # 爆炸对象状态设置为True
        #             bomb.visible = True
        #             break
         #   aliens_hit.remove(aliens_var)

        check_high_score(stats, sb)

    if len(aliens) == 0:
        #删除现有的子弹并新建一群外星人
        bullets.empty()
        #每过一关速度将加快
        ai_settings.increase_speed()

        #提高等级
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, aliens_hit, bombs, bullets):
    """更新子弹位置，并删除已消失的子弹"""
    #更新子弹位置
    bullets.update()

    #删除已经消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
        #print(len(bullets))

    #检查是否有子弹击中外星人
    #如果是这样，就删除相应的子弹和外星人
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, aliens_hit, bombs, bullets)

def update_screen(ai_settions,screen,stats,sb, ship, aliens, bullets, play_button):
    """更新屏幕上的图像，并切换到新屏幕"""
    #每次循环时都重绘屏幕
    screen.fill(ai_settions.bg_color)
    ship.blitme()
    #alien.blitme()
    aliens.draw(screen)
    #在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    #如果游戏处于非活动状态，就绘制play按钮
    if not stats.game_active:
        play_button.draw_button()

    #绘制得分图案
    sb.show_score()

    #让最近绘制的屏幕可见
    pygame.display.flip()

def get_number_rows(ai_settings,ship_height,alien_height):
    """计算屏幕可容纳多少行外星人"""
    available_space_y = (ai_settings.screen_height-(3*alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def get_number_aliens_x(ai_settings,alien_width):
    """计算每行可容纳多少个外星人"""
    available_space_x = ai_settings.screen_width - 2*alien_width
    number_aliens_x = int(available_space_x/(2*alien_width))
    return number_aliens_x


def create_alien(ai_settings,screen,aliens,alien_number,row_number):
    """创建一个外星人并将其放到当前行"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """创建外星人群"""
    #创建一个外星人，并计算一行可容纳多少个外星人
    #外星人间距为外星人宽度
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings,alien.rect.width)
    number_rows = get_number_rows(ai_settings,ship.rect.height,alien.rect.height)

    #创建第一行外星人
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            #创建一个外星人并将其加入当前行
            create_alien(ai_settings,screen,aliens,alien_number,row_number)

def check_fleet_edges(ai_settings, aliens):
    """有外星人到达边缘时采取相应的措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """将整群外星人下移，并改变他们的方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """响应被外星人撞到的飞船"""
    print(stats.ships_left)
    if stats.ships_left > 0:
        # 将ships_left减少1
        stats.ships_left -= 1
        #print(stats.ships_left)
        # 暂停
        sleep(0.5)
    else:
        stats.set_high_score(stats.high_score)
        stats.game_active = False
        pygame.mouse.set_visible(True)

    #更新记分牌
    sb.prep_ships()

    # 清空外星人列表和子弹列表
    aliens.empty()
    bullets.empty()

    # 创建一群新的外星人，并将飞船放到屏幕底端中央
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()

def update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """更新外星人群众所有外星人的位置"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    #检查是否有卫星人到达底部
    check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets)

    #检测子弹和外星人之间的碰撞
    if pygame.sprite.spritecollideany(ship,aliens):
        #print("ship hit!!!")
        ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)

def check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """判断外星人是否到达底部"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #像飞船被撞一样处理
            ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
            break

def check_high_score(stats, sb):
    """检查是否诞生了新的最高得分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

def display(ai_settings, screen, rect):
    bomb_image = pygame.image.load('images/bz.png')
    screen.blit(bomb_image, rect)
