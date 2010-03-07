from django.db import models

# Create your models here.
class Song(models.Model):
    name = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    album = models.CharField(max_length=255)
    error = models.CharField(max_length=255)
    position = models.IntegerField()
    xmms_id = models.IntegerField()
    active = models.BooleanField()

    def __unicode__(self):
        return ("{0}: {1}".format(self.position, self.name))

class XmmsStatus(models.Model):
    timeout = models.IntegerField(help_text="Cache refresh time in milliseconds, set too low and xmms2 will crash")
    current_action = models.IntegerField(help_text="0: Stopped, 1: Playing, 2: Paused")
    last_update = models.DateTimeField()
    playlist_size = models.IntegerField(help_text="Sets number of songs currently in playlist")
    current_position = models.IntegerField(help_text="Current position of player in playlist")
    seek = models.IntegerField()
    max_seek = models.IntegerField()
    volume = models.IntegerField()

class Action(models.Model):
    """
    Each action is a task to be performed by the xmms2 player. This includes,
    but is not limited to: play, pause, next, previous, add item to playlist,
    remove item from playlist, reorder item in playlist, etc
    """
    command = models.CharField(max_length=255)

    def __unicode__(self):
        return ("{0}".format(self.command))
