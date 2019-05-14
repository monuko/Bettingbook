from django.db import models
import json
from django.core.cache import cache

class Bets(models.Model):
    gameTime = models.CharField(max_length=100)
    gameDate = models.CharField(max_length=100)
    #group = models.ForeignKey(Group, on_delete=models.CASCADE) # Group Class 
    homeTeam = models.CharField(max_length=100) 
    awayTeam = models.CharField(max_length=100)
    betType = models.CharField(max_length=100)
    #title = models.ForeignKey(Title, on_delete=models.CASCADE) # Title Class
    eventID = models.CharField(max_length=100)
    homeOdds = models.FloatField()
    awayOdds = models.FloatField()
    drawOdds = models.FloatField()

'''
class Group():
    group = models.CharField()
    # Apparently Group should have foriegn key reletionship with titles 
    
class Title():
    title = models.CharField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    key = models.CharField()
'''

class SingletonModel(models.Model):

    class Meta:
        abstract = True

    def set_cache(self):
        cache.set(self.__class__.__name__, self)

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)
        self.set_cache()

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        if cache.get(cls.__name__) is None:
            obj, created = cls.objects.get_or_create(pk=1)
            if not created:
                obj.set_cache()
        return cache.get(cls.__name__)

class APIRequest(SingletonModel):
    # stores in "HH:MM"
    lastRequestHour = models.IntegerField(default=0) # Max Value 23
    lastRequestMinute = models.IntegerField(default=0) # Max Value 59
    remainingRequests = models.IntegerField()
    usedRequests = models.IntegerField()

