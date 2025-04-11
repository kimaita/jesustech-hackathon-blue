from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# UserProfile model to store extra fields for the default User model
class UserProfile(models.Model):
    USER_TYPE_CHOICES = (
        (1, "Student"),
        (2, "Instructor"),
        (3, "Admin"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, null=True, blank=True)
    user_type = models.PositiveIntegerField(choices=USER_TYPE_CHOICES, default=1)

    def __str__(self):
        return self.user.username


# Signal to create/update UserProfile when User is created/updated
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.userprofile.save()
