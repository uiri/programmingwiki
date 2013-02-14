# Create your views here.
import markdown2
from forms import PageForm
from models import Page
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_protect

def show(request, talk):
    pagetitle = request.path[1:].rsplit('/')[0]
    data = getlatestdata(pagetitle)
    if not data:
        return render_to_response('create.html', {'title' : pagetitle})
    if data.redirect:
        return redirect(data.contents)
    return render_to_response('page.html', {'content' : markdown2.markdown(data.contents), 'title' : request.path[1:]})

def getlatestdata(title):
    try:
        revisions = Page.objects.filter(title=title)
        latest = revisions.count()
        if latest == 0:
            return False
        return revisions.get(revision=latest)
    except:
        return False
    
def home(request):
    return render_to_response('base.html', {'title': 'XQZ Programming Wiki'})

def search(request):
    q = request.path[1:].rsplit('/')[0]
    qset = Page.objects.extra(
        select={
            'snippet': "ts_headline(contents, to_tsquery(%s))",
            'rank': "ts_rank_cd(to_tsvector(contents, to_tsquery(%s))"
            },
        where=["to_tsvector(contents) @@ to_tsquery(%s)"],
        params=[q],
        select_params=[q, q],
        order_by=('-rank',)
        )
    return render_to_response('results.html')

@csrf_protect
def edit(request, talk):
    c = {}
    pagetitle = request.path[1:]
    pagetitle = pagetitle.rsplit('/')[0]
    pagedata = getlatestdata(pagetitle)
    if not pagedata:
        oldcontents = ""
    elif talk:
        oldcontents = pagedata.talkcontents
    else:
        oldcontents = pagedata.contents
    blankform = PageForm({'pagecontent': oldcontents})
    if request.method == "POST":
        form = PageForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['redirect']:
                if not Page.objects.filter(title=form.cleaned_data['pagecontent']).exists():
                    return render_to_response('edit.html', {'title' : 'Editting '+pagetitle, 'form' : blankform, 'oldcontents': oldcontents})
            newrev = Page(title=pagetitle)
            newestrev = Page.objects.filter(title=pagetitle).count()
            newrev.redirect = form.cleaned_data['redirect']
            if pagedata:
                talkorno = (form.cleaned_data['pagecontent'], pagedata.contents, pagedata.talkcontents)
            else:
                talkorno = (form.cleaned_data['pagecontent'], "", "")
            if talk:
                newrev.talkcontents = talkorno[0]
                newrev.contents = talkorno[1]
            else:
                newrev.contents = talkorno[0]
                newrev.talkcontents = talkorno[2]
            newrev.revision = newestrev + 1
            newrev.save()
            return render_to_response('base.html', {'title': 'XQZ Programming Wiki'})
    c.update({'title' : "Editting "+pagetitle, 'form' : blankform, 'oldcontents': oldcontents})
    return render_to_response('edit.html',  c, context_instance=RequestContext(request))
