from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify

from .managers import Manager
from .constants import COUNTRIES, LANGUAGES
# Create your models here.

class User(AbstractUser):
    profile_image = models.ImageField(upload_to='accounts/media/images', default='static/images/default_avatar.png')
    email = models.EmailField(unique=True, max_length=254)
    date_of_birth = models.DateField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    objects = Manager()
    
    def __str__(self) -> str:
        return self.username
    
class UserAddress(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='userAddress')
    country = models.CharField(max_length=250, choices=COUNTRIES)
    city = models.CharField(max_length=250)
    zip_code = models.IntegerField()
    create_at = models.DateTimeField(auto_now_add=True)
    def __str__(self) -> str:
        return f"Country: {self.country}, City: {self.city}"
    
class Specialization(models.Model):
    name = models.CharField(max_length=250,unique=True)
    slug = models.SlugField(max_length=250, unique=True, blank=True, null=True)
    created_at = models.DateTimeField( auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Specialization, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.name
    
class Journalist(models.Model):
    user = models.OneToOneField(to=User, related_name='journalist', on_delete=models.CASCADE)
    specialization = models.ManyToManyField(to=Specialization)
    languages = models.CharField(max_length=100, choices=LANGUAGES)
    awards = models.CharField(max_length=250, blank=True, null=True)
    def __str__(self):
        return f'{self.user.username}'
    
class Education(models.Model):
    journalist = models.ForeignKey(to=Journalist, on_delete=models.CASCADE, related_name='educations')
    institute = models.CharField(max_length=250)
    degree_type = models.CharField(max_length=250)
    field_of_study = models.CharField(max_length=250)
    start_year = models.DateField()
    end_year = models.DateField()
    def __str__(self) -> str:
        return self.degree_type
    
class Subscription(models.Model):
    subscriber = models.ForeignKey(User, related_name='subscriptions', on_delete=models.CASCADE)
    subscribed_to = models.ForeignKey(to=Journalist, related_name='subscribers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('subscriber', 'subscribed_to')

    def __str__(self):
        return f'{self.subscriber.username} subscribed to {self.subscribed_to.user}'