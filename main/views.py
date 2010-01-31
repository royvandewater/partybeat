from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from player.xmms_layer import Xmms_layer
from library.models import SongFile
from library.forms import UploadForm

def ignore_case_and_the(name):
    name = name.lower()
    if name.startswith("the "):
        try:
            name = name[4:]
        except KeyError:
            name = "the "
    return name

def get_blank(request):
    try:
        return render_to_response('blank.html') if request.POST['source'] == "ajax" else HttpResponseRedirect('/')
    except (KeyError):
        return HttpResponseRedirect('/')

def player(request):
    xmms2 = Xmms_layer()
    xmms2.load_player_from_db()
    player = xmms2.player
    artists = list(set(SongFile.objects.all().values_list('artist', flat=True)))
    artists.sort(key=ignore_case_and_the)
    form = UploadForm()
    popout = True
    return render_to_response('main.html', locals(), context_instance=RequestContext(request))

def get_info(request):
    xmms_layer = Xmms_layer()
    player = xmms_layer.player
    return render_to_response('info.xml', locals(), context_instance=RequestContext(request))
