from django.contrib.auth import get_user_model
from django.db import models


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('manager', 'Manager'),
        ('worker', 'Worker'),
    ]

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='worker')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} ({self.role})'

    @classmethod
    def create_for_user(cls, user):
        profile, created = cls.objects.get_or_create(user=user)
        if created:
            profile.role = 'worker'
            profile.save()
        return profile
