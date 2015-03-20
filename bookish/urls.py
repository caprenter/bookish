from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
import bookish.views as v

urlpatterns = patterns('',
    url(r'^$', v.HomePageView.as_view(), name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^cash$', login_required(v.TransactionListView.as_view()), {'transaction_type': 'C'}, name='bookish-cash_list'),
    url(r'^cash/edit/(?P<transaction_id>[^/]+)?/?$', login_required(v.TransactionEdit.as_view()), {'transaction_type': 'C'}, name='bookish-cash_edit'),
    url(r'^revision/(?P<transaction_id>[^/]+)/$', login_required(v.TransactionItemRevisionView.as_view()), name='bookish-cash_revision_list'),
    url(r'^receipt$', login_required(v.TransactionListView.as_view()), {'transaction_type': 'R'}, name='bookish-receipt_list'),
    url(r'^receipt/edit$', login_required(v.TransactionEdit.as_view()), {'transaction_type': 'R'}, name='bookish-receipt_edit'),
    url(r'^bank$', login_required(v.TransactionListView.as_view()), {'transaction_type': 'B'}, name='bookish-bank_list'),
    url(r'^bank/edit$', login_required(v.TransactionEdit.as_view()), {'transaction_type': 'B'}, name='bookish-bank_edit'),
    url(r'^invoice$', login_required(v.TransactionListView.as_view()), {'transaction_type': 'I'}, name='bookish-invoice_list'),
    url(r'^invoices/edit$', login_required(v.TransactionEdit.as_view()), {'transaction_type': 'I'}, name='bookish-invoice_edit'),
    url(r'^mileage$', login_required(v.TransactionListView.as_view()), {'transaction_type': 'M'}, name='bookish-mileage_list'),
    url(r'^mileage/edit$', login_required(v.TransactionEdit.as_view()), {'transaction_type': 'M'}, name='bookish-mileage_edit'),
    url(r'^accountancy-firm$', login_required(v.AccountancyFirmListView.as_view()), name='bookish-accountancy-firm_list'),
    url(r'^company$', login_required(v.CompanyListView.as_view()), name='bookish-company_list'),
    url(r'^test500$', lambda: None),
)
