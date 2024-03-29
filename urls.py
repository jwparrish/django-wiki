from django.conf.urls.defaults import patterns, include, url
import os.path

site_media = os.path.join(os.path.dirname(__file__), 'site_media')

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'djwiki.views.home', name='home'),
    # url(r'^djwiki/', include('djwiki.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    (r'^wiki/page/(?P<page_name>[^/]+)/edit/$', 'django-wiki.wiki.views.edit_page'),
     (r'^wiki/page/(?P<page_name>[^/]+)/save/$', 'django-wiki.wiki.views.save_page'),
     (r'^wiki/page/(?P<page_name>[^/]+)/$', 'django-wiki.wiki.views.view_page'),
     (r'^wiki/tag/(?P<tag_name>[^/]+)/$', 'django-wiki.wiki.views.view_tag'),
     (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': site_media }),
)