from django.db import models
import eyeD3

# Create your models here.
class SongFile(models.Model):
    file = models.FileField(upload_to="music/%Y/%m/%d")
    name = models.CharField(max_length=255, blank=True)
    artist = models.CharField(max_length=255, blank=True)
    album = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return ("{song.artist} - {song.album} - {song.name}".format(song=self))

    def save(self, force_insert=False, force_update=False):
        # Call the real save method
        super(SongFile, self).save(force_insert, force_update)
        # Do stuff
        tag = eyeD3.Tag()
        tag.link(self.file.path)
        self.name = tag.getTitle()
        self.artist = tag.getArtist()
        self.album = tag.getAlbum()
        # Save again!
        super(SongFile, self).save(force_insert, force_update)

