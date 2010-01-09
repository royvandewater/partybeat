from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from xmms2_django.player.xmms_layer import Xmms_layer
from xmms2_django.song_storage.models import SongFile
from xmms2_django.song_storage.forms import UploadForm

def get_blank(request):
    try:
        return render_to_response('blank.html') if request.POST['source'] == "ajax" else HttpResponseRedirect('/')
    except (KeyError):
        return HttpResponseRedirect('/')

def player(request):
    xmms2 = Xmms_layer()
    xmms2.load_player_from_db()
    player = xmms2.player
    songFiles = SongFile.objects.all()
    form = UploadForm()
    return render_to_response('player.html', locals(), context_instance=RequestContext(request))

def get_info(request):
    xmms_layer = Xmms_layer()
    player = xmms_layer.player
    return render_to_response('info.xml', locals(), context_instance=RequestContext(request))

# def playlist(request):
    # player = Xmms_layer().player
    # return render_to_response('playlist.html', locals(), context_instance=RequestContext(request))

# def delete(request, xmms_id):
    # xmms2 = Xmms_controller()
    # xmms2.delete(xmms_id)
    # return get_blank(request)
