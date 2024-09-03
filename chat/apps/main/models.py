from django.db import models
from django.contrib.auth.models import User


class BaseModel(models.Model):
    """
    Abstract base model with common fields.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Room(BaseModel):
    """
    Model representing a chat room.
    """
    name = models.CharField(max_length=255, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return self.name


class Chat(BaseModel):
    """
    Model representing a chat message.
    """
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    message = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.user.username if self.user else 'Unknown'}: {self.message}"
