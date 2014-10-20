from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
import bookish.views as v

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^cash$', login_required(v.CashListView.as_view()), name='bookish-cash_list'),
    url(r'^cash/edit$', login_required(v.CashCreate.as_view())),
)
