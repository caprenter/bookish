from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
import bookish.views as v

urlpatterns = patterns('',
    url(r'^$', v.HomePageView.as_view(), name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),

    url(r'^cash$', login_required(v.TransactionListView.as_view()), {'transaction_type': 'C'}, name='bookish-cash_list'),
    url(r'^cash/edit/(?P<transaction_id>[^/]+)?/?$', login_required(v.TransactionEdit.as_view()), {'transaction_type': 'C'}, name='bookish-cash_edit'),
    url(r'^cash/edit-inline/(?P<transaction_id>[^/]+)?/?$', login_required(v.TransactionEditInline.as_view()), {'transaction_type': 'C'}, name='bookish-cash_edit-inline'),

    url(r'^revision/(?P<transaction_id>[^/]+)/$', login_required(v.TransactionItemRevisionView.as_view()), name='bookish-cash_revision_list'),
    url(r'^receipt$', login_required(v.TransactionListView.as_view()), {'transaction_type': 'R'}, name='bookish-receipt_list'),
    url(r'^receipt/edit/(?P<transaction_id>[^/]+)?/?$', login_required(v.TransactionEdit.as_view()), {'transaction_type': 'R'}, name='bookish-receipt_edit'),

    url(r'^bank/accounts$', login_required(v.BankAccountListView.as_view()), name='bookish-bank-account_list'),
    url(r'^bank/account/(?P<bank_account_id>[^/]+)?/?$', login_required(v.TransactionListView.as_view()), {'transaction_type': 'B'}, name='bookish-bank_list'),
    url(r'^bank/edit/(?P<transaction_id>[^/]+)?/?$', login_required(v.TransactionEdit.as_view()), {'transaction_type': 'B'}, name='bookish-bank_edit'),
    
    url(r'^invoice$', login_required(v.TransactionListView.as_view()), {'transaction_type': 'I'}, name='bookish-invoice_list'),
    url(r'^invoices/edit/(?P<transaction_id>[^/]+)?/?$', login_required(v.TransactionEdit.as_view()), {'transaction_type': 'I'}, name='bookish-invoice_edit'),

    url(r'^mileage$', login_required(v.TransactionListView.as_view()), {'transaction_type': 'M'}, name='bookish-mileage_list'),
    url(r'^mileage/edit/(?P<transaction_id>[^/]+)?/?$', login_required(v.TransactionEdit.as_view()), {'transaction_type': 'M'}, name='bookish-mileage_edit'),

    url(r'^report/detail/', v.detail_report, name='bookish-report-detail'),
    url(r'^accountancy-firm$', login_required(v.AccountancyFirmListView.as_view()), name='bookish-accountancy-firm_list'),
    url(r'^company$', login_required(v.CompanyListView.as_view()), name='bookish-company_list'),
    url(r'^vehicle$', login_required(v.VehicleListView.as_view()), name='bookish-vehicle_list'),
    url(r'^test500$', lambda: None),
)
