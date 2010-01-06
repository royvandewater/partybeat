from django.db import models
import eyeD3
import mutagen

from xmms2_django.daemon.models import Action

# Create your models here.
class SongFile(models.Model):
    file = models.FileField(upload_to="music/%Y/%m/%d")
    name = models.CharField(max_length=255, blank=True)
    artist = models.CharField(max_length=255, blank=True)
    album = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return ("{song.artist} - {song.album} - {song.name}".format(song=self))

    def print_list(self, list):
        total = list[0]
        for item in list[1:]:
            total += " - " + item
        return total

    def save(self, force_insert=False, force_update=False):
        # Call the real save method
        super(SongFile, self).save(force_insert, force_update)
        # If name, artist and album are set, user is overriding id3 read
        if not (self.name and self.artist and self.album):
            # Get the filetype
            filetype = (self.file.name.rpartition(".")[2]).lower()
            if filetype == "mp3":
                from mutagen.mp3 import MP3
                mp3 = MP3(self.file.path)

                self.name = mp3["TIT2"]
                self.artist = mp3["TPE1"]
                self.album = mp3["TALB"]
            elif filetype == "flac":
                from mutagen.flac import FLAC
                flac = FLAC(self.file.path)

                self.name = self.print_list(flac["title"])
                self.artist = self.print_list(flac["artist"])
                self.album = self.print_list(flac["album"])

            elif filetype == "ogg":
                from mutagen.oggvorbis import OggVorbis
                ogg = OggVorbis(self.file.path)

                self.name = self.print_list(ogg["title"])
                self.artist = self.print_list(ogg["artist"])
                self.album = self.print_list(ogg["album"])

            else:
                self.name = self.file.name.rpartition("/")[2]
                self.artist = "Unknown"
                self.album = "Unknown"
            # Save again!
            super(SongFile, self).save(force_insert, force_update)
