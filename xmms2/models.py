from django.db import models

# Create your models here.
class Song(models.Model):
    name = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    album = models.CharField(max_length=255)
    error = models.CharField(max_length=255)
    position = models.IntegerField()
    xmms_id = models.IntegerField()

    def __unicode__(self):
        return ("{0}: {1}".format(self.position, self.name))

class XmmsStatus(models.Model):
    timeout = models.IntegerField(help_text="Cache refresh time in milliseconds, set too low and xmms2 will crash")
    current_action = models.IntegerField(help_text="0: Stopped, 1: Playing, 2: Paused")
    last_update = models.DateTimeField()
