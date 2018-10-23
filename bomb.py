import pygame

class Bomb(object):
    # 初始化爆炸
    def __init__(self, screen):
        self.main_screen = screen
        # 加载爆炸资源
        self.image = [pygame.image.load("images/bz.png") for v in range(1, 8)]
        # 设置当前爆炸播放索引
        self.index = 0
        # 图片爆炸播放间隔
        self.interval = 20
        self.interval_index = 0
        # 爆炸位置
        self.position = [0, 0]
        # 是否可见
        self.visible = False

    # 设置爆炸播放的位置
    def set_pos(self, x, y):
        self.position[0] = x
        self.position[1] = y

    # 爆炸播放
    def action(self):
        # 如果爆炸对象状态不可见，则不计算坐标
        if not self.visible:
            return

        # 控制每一帧图片的播放间隔
        self.interval_index += 1
        if self.interval_index < self.interval:
            return
        self.interval_index = 0

        self.index = self.index + 1
        if self.index >= len(self.image):
            self.index = 0
            self.visible = False

    # 绘制爆炸
    def draw(self):
        # 如果对象不可见，则不绘制
        if not self.visible:
            return
        self.main_screen.blit(self.image[self.index], (self.position[0], self.position[1]))