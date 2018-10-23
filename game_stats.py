
class GameStats():
    """跟踪游戏的统计信息"""

    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        self.reset_stats()

        #游戏启动时处于激活状态
        self.game_active = False

        #在任何情况下都不要重置最高分
        self.high_score = 0
        self.level = 1

    def reset_stats(self):
        """初始化在游戏运行期间可能变化的统计信息"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0 #统计得分

    def get_high_score(self):
        list = []
        history_high_score = 0
        try:
            with open("config/config.txt") as file_object:
                for line in file_object:
                    list.append(line.rstrip().split("="))

            key = 0
            while key < len(list):
                if list[key][0] == "history_high_score":
                    history_high_score = int(list[key][1])
                    break
                key += 1
        except:
            history_high_score = 0

        return history_high_score

    def set_high_score(self,high_score):
        str1 = "history_high_score=" + str(high_score)
        try:
            with open("config/config.txt",'w') as file_object:
                file_object.write(str1)
        except:
            pass


