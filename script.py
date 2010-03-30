from library.models import *

print("updating track numbers...")
for song in SongFile.objects.all():
    try:
        print(".")
        song.save()
    except:
        print("Failed on: {0}".format(song))
print("Done!")
