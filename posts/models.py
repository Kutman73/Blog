from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Hashtag(models.Model):
    # icon = models.ImageField(null=True)
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    image = models.ImageField()
    title = models.CharField(max_length=255)
    description = models.TextField()
    hashtags = models.ManyToManyField(Hashtag)

    def __str__(self):
        return f'{self.author.username}_{self.title}'


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.author.username}_{self.post}'
