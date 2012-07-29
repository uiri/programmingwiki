# Create your views here.
import markdown2
from forms import PageForm
from models import Page
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response

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

def edit(request):
    pagetitle = request.path[1:]
    pagetitle = pagetitle.rsplit('/')[0]
    if request.method == "POST":
        form = PageForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['redirect']:
                if not Page.objects.filter(title=form.cleaned_data['pagecontent']).exists():
                    return render_to_response('edit.html', {'title' 'Editting '+pagetitle, 'form' : PageForm()})
            newrevdata = {}
            newrevdata['title'] = pagetitle
            newestrev = Page.objects.filter(title=pagetitle).count()
            newrevdata['redirect'] = form.cleaned_data['redirect']
            newrevdata['content'] = form.cleaned_data['pagecontent']
            if newestrev:
                newrevdata['talkcontents'] = Page.objects.filter(title=pagetitle, revision=newestrev).talkcontents
            else:
                newrevdata['talkcontents'] = ""
            newrevdata['revision'] = newestrev + 1
            newrev = Page(newrevdata)
            newrev.save()
            return render_to_response('base.html', {'title': 'XQZ Programming Wiki'})
    return render_to_response('edit.html', {'title': 'Editting '+pagetitle, 'form' : PageForm()})
