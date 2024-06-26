from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    youtube_link = models.URLField()
    youtube_title = models.CharField(max_length=1000)
    generated_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.youtube_title
    
class Chat(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    message = models.TextField()
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.message