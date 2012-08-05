from django.conf.urls import patterns, include, url
from markdownwiki import views as wikiviews
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       (r'^[^/]+/talk/edit$', wikiviews.edit, {'talk': True}),
                       (r'^[^/]+/talk$', wikiviews.show, {'talk': True}),
                       (r'^[^/]+/edit$', wikiviews.edit, {'talk': False}),
                       (r'^[^/]+$', wikiviews.show, {'talk': False}),
                       (r'^$', wikiviews.home)
    # Examples:
    # url(r'^$', 'programmingwiki.views.home', name='home'),
    # url(r'^foo/', include('foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
