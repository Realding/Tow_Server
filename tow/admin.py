from django.contrib import admin

# Register your models here.
from tow import models

admin.site.register(models.UserInfo)
admin.site.register(models.GameInfo)
admin.site.register(models.PlayerOnGame)