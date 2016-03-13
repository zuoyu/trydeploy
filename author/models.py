from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class Author(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    github = models.CharField(max_length=1024, blank=True, default='')
    picture = models.ImageField(upload_to='profile_pic/', blank=True, null=True, default='')
