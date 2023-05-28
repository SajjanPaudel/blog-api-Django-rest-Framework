from django.db import models
from django.contrib.auth.models import User
from autoslug import AutoSlugField

class Topic(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    blog_header_image = models.ImageField(blank=True, upload_to="image/", default='image/default.jpg' )
    blog_title = models.CharField(max_length=500)
    blog_summary = models.CharField(max_length=1000,null=True)
    blog_content = models.TextField(null=True,blank=True)
    # blog_content = RichTextField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    blog_slug= AutoSlugField(populate_from='blog_title',unique=True,null=True,default=None)
    
    def __str__(self):
        return self.blog_title   
        return self.user
          

    class Meta:
        ordering = ['-updated_date']
# Create your models here.


