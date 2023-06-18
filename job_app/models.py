from django.db import models
from bson.objectid import ObjectId

class User(models.Model):
    _id = models.CharField(primary_key=True, editable=False,max_length=255)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True)
    isAdmin = models.BooleanField(default=False)
    isAgent = models.BooleanField(default=False)
    skills = models.JSONField(default=list)
    profile = models.CharField(max_length=255, default='ww.png')
    timestamps = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        if not self._id:
            self._id = str(ObjectId())
        super().save(*args, **kwargs)


class Job(models.Model):
    _id = models.CharField(primary_key=True, editable=False,max_length=255)
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    hiring = models.BooleanField(default=True)
    description = models.TextField()
    company = models.CharField(max_length=255)
    salary = models.CharField(max_length=255)
    period = models.CharField(max_length=255)
    contract = models.CharField(max_length=255)
    requirements = models.JSONField()
    image_url = models.CharField(max_length=255)
    agent = models.ForeignKey(User, on_delete=models.CASCADE, to_field='_id')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self._id:
            self._id = str(ObjectId())
        super().save(*args, **kwargs)

class Bookmark(models.Model):
    _id = models.CharField(primary_key=True, editable=False,max_length=255)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    userId = models.CharField(max_length=255, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def save(self, *args, **kwargs):
        if not self._id:
            self._id = str(ObjectId())
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.job} - {self.userId}"

# Create your models here.
