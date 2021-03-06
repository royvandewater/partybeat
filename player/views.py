from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse

from models import *
from xmms_layer import Xmms_layer
from library.models import SongFile

def get_blank(request):
    try:
        return render_to_response('blank.html') if request.POST['source'] == "ajax" else HttpResponseRedirect('/')
    except (KeyError):
        return HttpResponseRedirect(reverse('main.views.player'))

# def player(request):
    # xmms2 = Xmms_layer()
    # return render_to_response('player.html', locals(), context_instance=RequestContext(request))

def run_action(request, action):
    xmms_layer = Xmms_layer()
    xmms_layer.store_action(action)
    return get_blank(request)

def main(request):
    xmms2 = Xmms_layer()
    xmms2.load_player_from_db()
    player = xmms2.player
    return render_to_response('player/standalone.html', locals(), context_instance=RequestContext(request))

def player(request):
    xmms2 = Xmms_layer()
    xmms2.load_player_from_db()
    player = xmms2.player
    return render_to_response('player/standalone_player.html', locals(), context_instance=RequestContext(request))

def get_info(request):
    xmms_layer = Xmms_layer()
    xmms_layer.load_player_from_db()
    player = xmms_layer.player
    return render_to_response('player/info.json', locals(), context_instance=RequestContext(request))

def playlist(request):
    xmms_layer = Xmms_layer()
    xmms_layer.load_player_from_db()
    player = xmms_layer.player
    return render_to_response('player/standalone_playlist.html', locals(), context_instance=RequestContext(request))

def delete(request, position):
    xmms_layer = Xmms_layer()
    xmms_layer.store_action("delete_{0}".format(int(position) - 1))
    return get_blank(request)

def seek(request, seek_time):
    xmms_layer = Xmms_layer()
    xmms_layer.store_action("seek_{0}".format(int(seek_time)))
    return get_blank(request)

def skip_to(request, position):
    xmms_layer = Xmms_layer()
    xmms_layer.store_action("skip_{0}".format(int(position)))
    return get_blank(request)

def volume(request, volume):
    xmms_layer = Xmms_layer()
    if int(volume) < 0:
        volume = 0
    elif int(volume) > 100:
        volume = 100
    xmms_layer.store_action("volume_{0}".format(int(volume)))
    return get_blank(request)

def move(request, start, end):
    xmms_layer = Xmms_layer()
    xmms_layer.store_action("move_{0}_{1}".format(start,end))
    return get_blank(request)
