from django.db import models

# Create your models here.


# 用户表
class UserInfo(models.Model):
    # 如果没有models.AutoField，默认会创建一个id的自增列
    username = models.CharField(max_length=128, unique=True, default="nameless")
    password = models.CharField(max_length=128)
    on_game = models.BooleanField(default=False)


    def __str__(self):
        return self.username


# 比赛信息
class GameInfo(models.Model):
    game_id = models.IntegerField(default=1)
    game_mode = models.IntegerField(default=1,unique=True)
    max_game_number = models.IntegerField(default=2)
    player_number = models.IntegerField(default=0)
    full = models.BooleanField(default=False)
    started = models.BooleanField(default=False)

    def __str__(self):
        return str(self.game_id)


# 比赛玩家信息
class PlayerOnGame(models.Model):
    game = models.ForeignKey(GameInfo, on_delete=models.CASCADE)
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    ready = models.BooleanField(default=False)
    shake_times = models.FloatField(default=0)
    on_wait = models.BooleanField(default=False)
    # percent = models.IntegerField(default=0)

    def __str__(self):
        return str(self.game.game_id) + ":" + self.user.username

