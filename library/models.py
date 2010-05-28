from django.db import models
import mutagen

from daemon.models import Action

# Create your models here.
class SongFile(models.Model):
    file = models.FileField(upload_to="music/%Y/%m/%d")
    name = models.CharField(max_length=255, blank=True)
    artist = models.CharField(max_length=255, blank=True)
    album = models.CharField(max_length=255, blank=True)
    track_number = models.IntegerField(default=0)

    def __unicode__(self):
        return ("{song.track_number}: {song.artist} - {song.album} - {song.name}".format(song=self))

    def print_list(self, list):
        total = list[0]
        for item in list[1:]:
            total += " - " + item
        return total

    def save(self, force_insert=False, force_update=False):

        import pdb
        pdb.set_trace()

        # Call the real save method
        super(SongFile, self).save(force_insert, force_update)

        # Get the filetype
        filetype = (self.file.name.rpartition(".")[2]).lower()

        # Save backup of old names
        old_name = self.name
        old_artist = self.artist
        old_album = self.album
        old_track_number = self.track_number
        try:
            if filetype == "mp3":
                from mutagen.mp3 import MP3
                mp3 = MP3(self.file.path)

                self.name = mp3["TIT2"]
                self.artist = mp3["TPE1"]
                self.album = mp3["TALB"]
                try:
                    self.track_number = int(mp3["TRCK"][0].partition("/")[0])
                except (ValueError, KeyError):
                    self.track_number = 0
            elif filetype in ("flac","ogg"):
                info = None
                if filetype == "flac":
                    from mutagen.flac import FLAC
                    info = FLAC(self.file.path)

                elif filetype == "ogg":
                    from mutagen.oggvorbis import OggVorbis
                    info = OggVorbis(self.file.path)

                self.name = self.print_list(info["title"])
                self.artist = self.print_list(info["artist"])
                self.album = self.print_list(info["album"])
                try:
                    self.track_number = int(self.print_list(info["tracknumber"]))
                except ValueError:
                    self.track_number = 0

            elif filetype == "m4a":
                from mutagen.m4a import M4A
                info = M4A(self.file.path)
                self.name = info["\xa9nam"]
                self.artist = info["\xa9ART"]
                self.album = info["\xa9alb"]
                try:
                    self.track_number = int(info["trkn"][0])
                except (ValueError, KeyError):
                    self.track_number = 0
            else:
                self.name = self.file.name.rpartition("/")[2]
                self.artist = "Unknown"
                self.album = "Unknown"

        except KeyError:
            self.name = self.file.name.rpartition("/")[2]
            self.artist = "Unknown"
            self.album = "Unknown"
            self.track_number = 0

        # Check if manual data was entered
        if old_name: self.name = old_name
        if old_artist: self.artist = old_artist
        if old_album: self.album = old_album
        if old_track_number: self.track_number = old_track_number

        # Save again!
        super(SongFile, self).save(force_insert, force_update)
