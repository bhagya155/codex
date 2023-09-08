from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class Post(models.Model):
    sr_no = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=50)
    content = models.TextField()
    slug = models.SlugField(max_length=155)
    timestamp = models.DateTimeField(blank=True)

    def __str__(self):
        return  self.title + " by "+ self.author

class BlogComment(models.Model):
    sr_no = models.AutoField(primary_key=True)
    comment = models.TextField(max_length=100)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    parent = models.ForeignKey('self',on_delete=models.CASCADE,null=True)
    timestamp = models.DateTimeField(default=now)
    def __str__(self):
        return  self.comment[0:10] + "... by"+ self.user.first_name
