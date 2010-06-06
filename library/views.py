from django.core import serializers
from django.core.files.uploadedfile import UploadedFile
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

import json
import zipfile

from models import *
from forms import *
from daemon.models import Action

def ignore_case_and_the(name):
    name = name.lower()
    if name.startswith("the "):
        try:
            name = name[4:]
        except KeyError:
            name = "the "
    return name

def get_filetype(filepath):
    return filepath.rpartition(".")[2]

def get_filename(filepath):
    return filepath.rpartition("/")[2]

def is_ajax(request):
    if request.POST.has_key('source') and request.POST['source'] == "ajax":
        return True
    else:
        return False

def get_json(data):
    try:
        # Assume its a queryset
        JSONSerializer = serializers.get_serializer("json")
        json_serializer = JSONSerializer()
        return json_serializer.serialize(data)
    except AttributeError:
        # Assume its a dict and serialize
        try:
            return json.dumps(data)
        except TypeError:
            # We probably have a 'querysetValues' object here
            # set() removes the duplicates. However, it also removes the ability to order.
            # so we use list to make it orderable again and then sort it.
            data = list(set(data))
            data.sort(key=ignore_case_and_the)
            return json.dumps(data)

def get_blank(request):
    try:
        return render_to_response('blank.html') if is_ajax(request) else HttpResponseRedirect(reverse('main.views.player'))
    except (KeyError):
        return HttpResponseRedirect(reverse('main.views.player'))

def enqueue(request, songFile):
    action = Action()
    action.command = "add_" + songFile.file.path
    action.save()
    return get_blank(request)

def artists(request):
    artists = SongFile.objects.all().values_list('artist', flat=True)
    artists = list(set(artists))
    artists.sort(key=ignore_case_and_the)
    return HttpResponse(get_json(artists))

def albums(request, artist=None):
    if artist:
        albums = SongFile.objects.filter(artist__icontains=artist.replace("_", " ")).values_list('album', flat=True)
    elif request.method == 'GET' and request.GET.has_key("artist"): 
        artist = request.GET["artist"].replace("&amp;", "&")
        print artist
        albums = SongFile.objects.filter(artist__icontains=artist.replace("_", " ")).values_list('album', flat=True)
    else:
        albums = SongFile.objects.all().values_list('album', flat=True)

    return HttpResponse(get_json(albums))

def songs(request, artist=None, album=None):
    if request.method == 'GET' and request.GET.has_key("artist") and request.GET.has_key("album"):
        artist = request.GET["artist"].replace("&amp;", "&")
        album = request.GET["album"].replace("&amp;", "&")
        songFiles = SongFile.objects.filter(artist__icontains=artist.replace("_", " "), album__icontains=album.replace("_", " ")).order_by('track_number','name')
    elif artist and album:
        songFiles = SongFile.objects.filter(artist__icontains=artist.replace("_", " "), album__icontains=album.replace("_", " ")).order_by('track_number','name')
    elif album:
        songFiles = SongFile.objects.filter(album__icontains=album.replace("_", " ")).order_by('track_number','name')
    elif artist:
        songFiles = SongFile.objects.filter(artist__icontains=artist.replace("_", " ")).order_by('track_number','name')
    else:
        songFiles = SongFile.objects.all()

    return HttpResponse(get_json(songFiles))

def generic_xml(request, category, item_name, items):
    xml_data = dict(category=category, item_name=item_name, items=items)
    return render_to_response('library/generic.xml', locals(), context_instance=RequestContext(request))

def library(request):
    artists = list(set(SongFile.objects.all().values_list('artist', flat=True)))
    artists.sort(key=ignore_case_and_the)
    return render_to_response('library/standalone.html', locals(), context_instance=RequestContext(request))

def add(request, song_id):
    songFile = SongFile.objects.get(id=song_id)
    return enqueue(request, songFile)

def add_random(request):
    songFile = SongFile.objects.order_by('?')[0]
    return enqueue(request, songFile)

def upload(request):
    if request.method == 'POST' and not request.POST.has_key("source"):
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']

            if zipfile.is_zipfile(uploaded_file.temporary_file_path()):
                zipped_songs = zipfile.ZipFile(uploaded_file)
                temp_dir = uploaded_file.file.name.rpartition('/')[0]

                for song_name in zipped_songs.namelist():
                    path = zipped_songs.extract(song_name,temp_dir)
                    try:
                        songFile = SongFile()
                        songFile.file = file(path)
                        songFile.save()
                        if request.POST['enqueue']:
                            enqueue(request, songFile)
                    except IOError:
                        pass
            else:
                songFile = SongFile()
                songFile.file = request.FILES['file']
                songFile.save()

                if request.POST['enqueue']:
                    enqueue(request, songFile)

            return HttpResponseRedirect(reverse('main.views.player'))
    else:
        form = UploadForm()

    html_template = "library/forms/upload.html" if is_ajax(request) else "library/upload.html"
    return render_to_response(html_template, locals(), context_instance=RequestContext(request))

def edit(request, song_id):
    songFile = SongFile.objects.get(id=int(song_id))
    if request.method == 'POST' and not request.POST.has_key("source"):
        form = EditForm(request.POST)
        if form.is_valid():
            songFile.name = form.cleaned_data['name']
            songFile.artist = form.cleaned_data['artist']
            songFile.album = form.cleaned_data['album']
            songFile.track_number = form.cleaned_data['track_number']
            songFile.save()
            return HttpResponseRedirect(reverse('main.views.player'))
    else:
        data = {'name': songFile.name,
                'artist': songFile.artist,
                'album': songFile.album,
                'track_number': songFile.track_number}
        form = EditForm(data)

    # Check for ajax
    html_template = "library/forms/edit.html" if is_ajax(request) else "library/edit.html"

    return render_to_response(html_template, locals(), context_instance=RequestContext(request))

def download(request, song_id):
    songFile = SongFile.objects.get(id=int(song_id))
    response = HttpResponse(content=songFile.file.chunks(), mimetype="audio/{0}".format(get_filetype(songFile.file.name)))
    response['Content-Disposition'] = "attachment; filename={0}".format(get_filename(songFile.file.name))
    return response

def search(request):
    if request.method == 'GET':
        try:
            artists = SongFile.objects.filter(artist__icontains=request.GET['search_input'])
            albums = SongFile.objects.filter(album__icontains=request.GET['search_input'])
            songs = SongFile.objects.filter(name__icontains=request.GET['search_input'])
            songFiles = set()
            songFiles.update(artists, albums, songs)
            return HttpResponse(get_json(songFiles))

        except KeyError:
            return get_blank(request)
    else:
        return get_blank(request)
