from django.conf.urls import patterns, include, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mahjong.views.home', name='home'),
    # url(r'^mahjong/', include('mahjong.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # page urls
    url(r'^$', 'pages.views.index'),
    url(r'^login$', 'pages.views.login'),

    # auth proc urls
    url(r'^login_proc$', 'auths.views.login_proc'),
    url(r'^logout_proc$', 'auths.views.logout_proc'),

    # record proc urls
    url(r'^submit_record_proc$', 'records.views.submit_record_proc'),
    url(r'^modify_record_proc$', 'records.views.modify_record_proc'),
)
