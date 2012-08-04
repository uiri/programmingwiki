# Create your views here.
import markdown2
from forms import PageForm
from models import Page
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_protect

def showpage(request):
    try:
        revisions = Page.objects.filter(title=request.path[1:])
        latest = revisions.count()
        data = revisions.get(revision=latest)
    except:
        return render_to_response('create.html', {'title' : request.path[1:]})
    if data.redirect:
        return redirect(data.content)
    return render_to_response('page.html', {'content' : markdown2.markdown(data.content), 'title' : request.path[1:]})

def home(request):
    return render_to_response('base.html', {'title': 'XQZ Programming Wiki'})

@csrf_protect
def edit(request):
    c = {}
    pagetitle = request.path[1:]
    pagetitle = pagetitle.rsplit('/')[0]
    if request.method == "POST":
        form = PageForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['redirect']:
                if not Page.objects.filter(title=form.cleaned_data['pagecontent']).exists():
                    return render_to_response('edit.html', {'title' : 'Editting '+pagetitle, 'form' : PageForm()})
            newrev = Page(title=pagetitle)
            newestrev = Page.objects.filter(title=pagetitle).count()
            newrev.redirect = form.cleaned_data['redirect']
            newrev.contents = form.cleaned_data['pagecontent']
            if newestrev:
                newrev.talkcontents = Page.objects.filter(title=pagetitle, revision=newestrev).talkcontents
            else:
                newrev.talkcontents = ""
            newrev.revision = newestrev + 1
            newrev.save()
            return render_to_response('base.html', {'title': 'XQZ Programming Wiki'})
    c.update({'title' : "Editting "+pagetitle, 'form' : PageForm()})
    return render_to_response('edit.html',  c, context_instance=RequestContext(request))
