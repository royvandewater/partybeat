from django.db import models

# Create your models here.
class SongFile(models.Model):
    file = models.FileField(upload_to="music/%Y/%m/%d")
    name = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    album = models.CharField(max_length=255)

    def __unicode__(self):
        return ("{song.artist} - {song.album} - {song.name}".format(song=self))

    def save(self, force_insert=False, force_update=False):
        # Do stuff
        # print(dir(self.file))
        # Call the real save method
        super(SongFile, self).save(force_insert, force_update)

