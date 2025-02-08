from django.contrib import admin

from app import models

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ("handle",)

admin.site.register(models.User, UserAdmin)