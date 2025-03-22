from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
# Create your models here.

User = get_user_model()

class Question(models.Model):
    CATEGORY_CHOICES = [
        ('Easy','Easy'),
        ('Medium','Medium'),
        ('Hard','Hard')
    ]
    TAG_CHOICES = [
        ('Array','Array'),
        ('Matrix','Matrix'),
        ('String','String'),
        ('Stack','Stack'),
        ('Queue','Queue'),
        ('LinkedList','LinkedList'),
        ('Hash','Hash'),
        ('Tree','Tree'),
        ('BinaryTree','BinaryTree'),
        ('BinarySearchTree','BinarySearchTree'),
        ('Heap','Heap'),
        ('Graph','Graph')
    ]
    title = models.CharField(max_length=255,unique=True,db_index=True)
    link = models.URLField(max_length=255,unique=True)
    category = models.CharField(max_length=10,choices=CATEGORY_CHOICES)
    tag = models.CharField(max_length=30,choices=TAG_CHOICES)
    slug = models.SlugField(unique=True,null=True)
    is_enable = models.BooleanField(default=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args,**kwargs)
    
    def __str__(self):
        return self.title

class Solved(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    