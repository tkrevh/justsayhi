from django.contrib import admin

# Register your models here.
from justsayhi.models import Team, AutoMessage


class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'team_id', )


class AutoMessageAdmin(admin.ModelAdmin):
    list_display = ('text', 'team', )


admin.site.register(Team)
admin.site.register(AutoMessage, AutoMessageAdmin)