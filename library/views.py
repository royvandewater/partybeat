from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core import serializers

from models import *
from forms import *
from xmms2_django.daemon.models import Action

def get_filetype(filepath):
    return filepath.rpartition(".")[2]

def get_filename(filepath):
    return filepath.rpartition("/")[2]

def is_ajax(request):
    if request.POST.has_key('source') and request.POST['source'] == "ajax":
        return True
    else:
        return False

def get_json(queryset):
    JSONSerializer = serializers.get_serializer("json")
    json_serializer = JSONSerializer()
    return json_serializer.serialize(queryset)


def get_blank(request):
    try:
        return render_to_response('blank.html') if is_ajax(request) else HttpResponseRedirect('/')
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

    return HttpResponse(get_json(albums))
    # return generic_xml(request, "albums", "album", albums)

def songs(request, artist=None, album=None):
    if artist and album:
        songFiles = SongFile.objects.filter(artist__icontains=artist.replace("_", " "), album__icontains=album.replace("_", " "))
    elif album:
        songFiles = SongFile.objects.filter(album__icontains=album.replace("_", " "))
    elif artist:
        songFiles = SongFile.objects.filter(artist__icontains=artist.replace("_", " "))
    else:
        songFiles = SongFile.objects.all()

    return HttpResponse(get_json(songFiles))
    

def generic_xml(request, category, item_name, items):
    xml_data = dict(category=category, item_name=item_name, items=items)
    return render_to_response('library/generic.xml', locals(), context_instance=RequestContext(request))

def library(request):
    songFiles = SongFile.objects.all() 
    return render_to_response('library/standalone.html', locals(), context_instance=RequestContext(request))

def add(request, song_id):
    songFile = SongFile.objects.get(id=song_id)
    action = Action()
    action.command = "add_" + songFile.file.path
    action.save()
    return get_blank(request)

def upload(request):
    if request.method == 'POST' and not request.POST.has_key("source"):
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            songFile = SongFile()
            songFile.file = request.FILES['file']
            songFile.save()
            return HttpResponseRedirect('/')
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
            songFile.save()
            return HttpResponseRedirect('/')
    else:
        data = {'name': songFile.name,
                'artist': songFile.artist,
                'album': songFile.album}
        form = EditForm(data)

    # Check for ajax
    html_template = "library/forms/edit.html" if is_ajax(request) else "library/edit.html"

    return render_to_response(html_template, locals(), context_instance=RequestContext(request))

def download(request, song_id):
    songFile = SongFile.objects.get(id=int(song_id))
    response = HttpResponse(content=songFile.file.chunks(), mimetype="audio/{0}".format(get_filetype(songFile.file.name)))
    response['Content-Disposition'] = "attachment; filename={0}".format(get_filename(songFile.file.name))
    return response
