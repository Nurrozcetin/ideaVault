from django.db import models
from .utils import encrypt_message, decrypt_message, load_key

class Category(models.Model):
    name = models.CharField(max_length=100)

class Member(models.Model):
    name = models.CharField(max_length=100)
    job = models.CharField(max_length=50)

class Requirements(models.Model):
    name = models.CharField(max_length=100)

class Idea(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    title = models.CharField(max_length=100)
    desc = models.TextField()
    requirements = models.ManyToManyField(Requirements, related_name='ideas')
    category = models.ManyToManyField(Category, related_name='ideas')
    member = models.ManyToManyField(Member, related_name='ideas')

    def save(self, *args, **kwargs):
        key = load_key('secret.key')
        if not self.pk:  
            self.id = encrypt_message(self.get_plain_id(), key)
        super().save(*args, **kwargs)

    def get_plain_id(self):
        return decrypt_message(self.id, load_key('secret.key'))
