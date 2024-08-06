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
    title = models.CharField(max_length=100)
    desc = models.TextField()
    requirements = models.ManyToManyField(Requirements, related_name='ideas')
    category = models.ManyToManyField(Category, related_name='ideas')
    member = models.ManyToManyField(Member, related_name='ideas')

    def save(self, *args, **kwargs):
        key = load_key('secret.key')
        self.title = encrypt_message(self.get_plain_title(), key)
        self.desc = encrypt_message(self.get_plain_desc(), key)
        super().save(*args, **kwargs)

    def get_plain_title(self):
        key = load_key('secret.key')
        return decrypt_message(self.title, key)

    def get_plain_desc(self):
        key = load_key('secret.key')
        return decrypt_message(self.desc, key)
