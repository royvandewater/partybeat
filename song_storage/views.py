from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

from models import *
from xmms2_django.daemon.models import Action

def get_blank(request):
    try:
        return render_to_response('blank.html') if request.POST['source'] == "ajax" else HttpResponseRedirect('/')
    except (KeyError):
        return HttpResponseRedirect('/')

def artists(request):
    songFiles = SongFile.objects.all().order_by('artist')
    artists = []
    for song in songFiles:
        if not song.artist in artists:
            artists.append(song.artist)

    return generic_xml(request, "artists", "artist", artists)

def albums(request, artist=None):
    if artist:
        songFiles = SongFile.objects.filter(artist__icontains=artist.replace("_", " "))
    else:
        songFiles = SongFile.objects.all()

    albums = []
    for song in songFiles:
        if not song.album in albums:
            albums.append(song.album)

    return generic_xml(request, "albums", "album", albums)

def songs(request, artist=None, album=None):
    print(artist)
    print(album)
    if artist and album:
        songFiles = SongFile.objects.filter(artist__icontains=artist.replace("_", " "), album__icontains=album.replace("_", " "))
    elif album:
        songFiles = SongFile.objects.filter(album__icontains=album.replace("_", " "))
    elif artist:
        songFiles = SongFile.objects.filter(artist__icontains=artist.replace("_", " "))
    else:
        songFiles = SongFile.objects.all()

    songs = []
    for song in songFiles:
        songs.append(song.name)

    return generic_xml(request, "songs", "song", songs)

def generic_xml(request, category, item_name, items):
    xml_data = dict(category=category, item_name=item_name, items=items)
    return render_to_response('generic.xml', locals())

def library(request):
    songFiles = SongFile.objects.all() 
    return render_to_response('library.html', locals())

def add(request, song_id):
    songFile = SongFile.objects.get(id=song_id)
    action = Action()
    action.command = "add_" + songFile.file.path
    action.save()
    return get_blank(request)

def upload(request):
    return get_blank(request)
