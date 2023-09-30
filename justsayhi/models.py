from django.db import models
from django.utils import timezone


class Team(models.Model):
    team_id = models.CharField(max_length=32, blank=False, null=False, unique=True, db_index=True)
    name = models.CharField(max_length=256, blank=False, null=False)
    token = models.CharField(max_length=256, blank=False, null=False)

    authed_user_id = models.CharField(max_length=256, blank=False, null=False)
    authed_user_access_token = models.CharField(max_length=256, blank=False, null=False)

    created = models.DateTimeField(auto_now_add=timezone.now)
    updated = models.DateTimeField(auto_now=timezone.now)

    def __str__(self):
        return f'{self.name} ({self.team_id})'


class AutoMessage(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='auto_messages')
    text = models.TextField(blank=False, null=False)

    created = models.DateTimeField(auto_now_add=timezone.now)

    def __str__(self):
        return f'{self.text[:128]}'
