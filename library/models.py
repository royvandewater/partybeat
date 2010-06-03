from django.db import models
from django.conf import settings
import mutagen
import shutil
import os
import errno

from daemon.models import Action

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST:
            pass
        else: raise

# Create your models here.
class SongFile(models.Model):
    file = models.FileField(upload_to="music/%Y/%m/%d", max_length=255)
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

        # don't Call the real save method
        # super(SongFile, self).save(force_insert, force_update)

        # Get the temporary file
        temp_file = self.file.file

        # Get the filetype
        filetype = (temp_file.name.rpartition(".")[2]).lower()

        # Save backup of old names
        old_name = self.name
        old_artist = self.artist
        old_album = self.album
        old_track_number = self.track_number

        # First obtain all metadata
        try:
            if filetype == "mp3":
                from mutagen.mp3 import MP3
                mp3 = MP3(temp_file.file.name)

                self.name = mp3["TIT2"].text[0]
                self.artist = mp3["TPE1"].text[0]
                self.album = mp3["TALB"].text[0]
                try:
                    self.track_number = int(mp3["TRCK"][0].partition("/")[0])
                except (ValueError, KeyError):
                    self.track_number = 0
            elif filetype in ("flac","ogg"):
                info = None
                if filetype == "flac":
                    from mutagen.flac import FLAC
                    info = FLAC(temp_file.file.name)

                elif filetype == "ogg":
                    from mutagen.oggvorbis import OggVorbis
                    info = OggVorbis(temp_file.file.name)

                self.name = self.print_list(info["title"])
                self.artist = self.print_list(info["artist"])
                self.album = self.print_list(info["album"])
                try:
                    self.track_number = int(self.print_list(info["tracknumber"]))
                except ValueError:
                    self.track_number = 0

            elif filetype == "m4a":
                from mutagen.m4a import M4A
                info = M4A(temp_file.file.name)
                self.name = info["\xa9nam"]
                self.artist = info["\xa9ART"]
                self.album = info["\xa9alb"]
                try:
                    self.track_number = int(info["trkn"][0])
                except (ValueError, KeyError):
                    self.track_number = 0
            else:
                self.name = temp_file.file.name.rpartition("/")[2]
                self.artist = "Unknown"
                self.album = "Unknown"

        except KeyError:
            self.name = temp_file.file.name.rpartition("/")[2]
            self.artist = "Unknown"
            self.album = "Unknown"
            self.track_number = 0

        # Check if manual data was entered
        if old_name: self.name = old_name
        if old_artist: self.artist = old_artist
        if old_album: self.album = old_album
        if old_track_number: self.track_number = old_track_number

        # Now move the temporary file to its resting place
        music_directory = "{0}music".format(settings.MEDIA_ROOT)
        music_sub_directory = "{0}/{1}/".format(self.artist, self.album).lower().replace(" ","_")

        destination_directory = "{0}/{1}".format(music_directory, music_sub_directory)

        music_file = "{0}.{1}".format(self.name, filetype).lower().replace(" ","_")

        mkdir_p(destination_directory)
        # shutil.copy(temp_file.file.name, "{0}{1}".format(destination_directory, destination_file))
        destination_file = "".join([destination_directory, music_file])
        shutil.copy(temp_file.file.name, destination_file)
        os.remove(temp_file.file.name)

        import pdb
        pdb.set_trace()
        # self.file = models.FileField(destination_file)
        self.file = destination_file
        # self.file._committed = True

        super(SongFile, self).save(force_insert, force_update)
