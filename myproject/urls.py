from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'myproject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.STATIC_URL}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^(.*)$', 'cms_templates.views.main'),
)
