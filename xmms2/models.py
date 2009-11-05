from django.db import models

# Create your models here.
class Song(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    album = models.CharField(max_length=255)
    error = models.CharField(max_length=255)
    position = models.IntegerField()

    def __unicode__(self):
        return ("{0}: {1}".format(self.position, self.title))

class LastUpdate(models.Model):
    time = models.TimeField()
