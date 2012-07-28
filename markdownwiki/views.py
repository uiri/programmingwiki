# Create your views here.
import markdown2
from models import Page
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.db.models import Max

def showpage(request):
    try:
        revisions = Page.objects.filter(title=request.path[1:])
        latest = revisions.aggregate(Max('revision'))
        data = revisions.get(latest)
    except:
        return render_to_response('create.html', {'title' : request.path[1:]})
    if data.redirect:
        return redirect(data.content)
    return render_to_response('page.html', {'content' : markdown2.markdown(data.content), 'title' : request.path[1:]})

def home(request):
    return render_to_response('base.html', {'title': 'XQZ Programming Wiki'})

def edit(request):
    if request.method == "GET":
        pagetitle = request.path[1:]
        pagetitle = pagetitle.rsplit('/')[0]
        return render_to_response('edit.html', {'title': 'Editting '+pagetitle})
    else:
        return render_to_response('base.html', {'title': 'XQZ Programming Wiki'})
