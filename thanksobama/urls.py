from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from django.views.generic import TemplateView
from thanksobama.main.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'thanksobama.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
	url(r'^$', TemplateView.as_view(template_name='index.html')),
	url(r'^new-question/$', NewQuestion.as_view())
)
