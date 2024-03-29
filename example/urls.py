from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'socialsharing.views.home', name='home'),
    # url(r'^socialsharing/', include('socialsharing.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$','views.home', name='home'),
    url(r'^upload', 'views.upload', name='upload'),
    url(r'^accounts/profile/', 'views.profile'),
    url(r'^social/', include('langkawi.urls', namespace = 'langkawi'))
)
