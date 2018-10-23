
import pygame
from pygame.sprite import Sprite

class Hit(Sprite):

    def __init__(self,ai_settings,screen, mouse_x, mouse_y):
        """初始化飞船并设置其位置"""
        super(Hit, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        #加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('images/bz.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        #将每首新飞船放在屏幕底部中央
        self.rect.x = mouse_x
        self.rect.y = mouse_y

    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image,self.rect)

