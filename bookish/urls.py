from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
import bookish.views as v

urlpatterns = patterns('',
    url(r'^$', v.HomePageView.as_view(), name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^cash$', login_required(v.CashListView.as_view()), name='bookish-cash_list'),
    url(r'^cash/edit$', login_required(v.CashCreate.as_view())),
    url(r'^cash/revision/(?P<transaction_id>[^/]+)/$', login_required(v.CashItemRevisionView.as_view()), name='bookish-cash_revison_list'),
    url(r'^accountancy-firm$', login_required(v.AccountancyFirmListView.as_view()), name='bookish-accountancy-firm_list'),
    url(r'^company$', login_required(v.CompanyListView.as_view()), name='bookish-company_list'),
)
