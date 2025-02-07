from django.db import models
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from users.models import User
class Art(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='arts') 
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=50, blank=True, null=True) 
    tags = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.FloatField(null=False, default= 0)
    file = models.FileField(
        upload_to='arts/img/',
        validators=[
            FileExtensionValidator(
                allowed_extensions=['png', 'jpg', 'jpeg', 'gif', 'jfif', 'mp4', 'avi', 'mov', 'webm'],
                message=(
                    "Le fichier doit être une vidéo (.avi, .mp4, .mov, .webm) "
                    "ou une image (.jpg, .png, .gif, .jfif)"
                )
            )
        ]
    )
    def __str__(self):
        return f"{self.title} "
