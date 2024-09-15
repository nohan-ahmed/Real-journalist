from django.db import models
from django.utils.text import slugify

from accounts.models import User
from accounts.constants import LANGUAGES

# Create your models here.
class Specialization(models.Model):
    name = models.CharField(max_length=250,unique=True)
    slug = models.SlugField(max_length=250, unique=True)
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
    
