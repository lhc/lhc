from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'lhc.views.home', name='home'),
    # url(r'^lhc/', include('lhc.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^', include(admin.site.urls)),

    url(r'^notificacao/', include('notificacoes.urls')),

    url(r'^static/(.*)$', 'django.views.static.serve',
             {'document_root': settings.STATIC_ROOT}),

)
