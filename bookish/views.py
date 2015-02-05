from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
import bookish.models as m


class HomePageView(TemplateView):
    template_name = "bookish/index.html"


'''
    TransactionListView use the in built django Class Based Views system
    to show all transactions filtered by the type of transaction.

    The type is sent as a kwarg from urls.py, and then used to:
     * filter the transaction query
     * define the template that is called
     * provide a human readable form of the transaction type
'''


class TransactionListView(ListView):
    def get_queryset(self):
        # In urls.py we pass a value for transaction_type - C for cash, B for Bank etc
        transaction_type = self.kwargs["transaction_type"]
        # Return all transactions of the requested type
        queryset = m.Transaction.objects.filter(transaction_type=transaction_type)
        return queryset

    def get_template_names(self):
        transaction_type = self.kwargs["transaction_type"]
        names = ['bookish/' + 'transaction_{0}_list.html'.format(transaction_type)]
        return names

    def transaction_type_name(self):
        names = {'C': 'Cash',
                 'B': 'Bank',
                 'R': 'Receipt',
                 'I': 'Invoice',
                 'M': 'Mileage',
                 'CN': 'Credit note'}
        transaction_type_name = names[self.kwargs['transaction_type']]
        return transaction_type_name


class TransactionCreate(CreateView):
    model = m.TransactionRevision

    def dispatch(self, request, *args, **kwargs):
        # Do whatever you want here
        fields = {'C': ['name', 'business_year', 'date', 'originating_account', 'amount', 'nominal_code', 'notes'],
                  'B': ['name', 'business_year', 'date', 'originating_account', 'amount', 'nominal_code', 'notes', 'supplier_invoice', 'additional_information', 'my_ref'],
                  'R': ['name', 'business_year', 'date', 'amount', 'nominal_code', 'notes', 'customer_ref', 'my_ref', 'is_expense'],
                  'I': ['name', 'business_year', 'date', 'originating_account', 'amount', 'actual_amount', 'my_ref'],
                  'M': ['name', 'business_year', 'date', 'originating_account', 'amount', 'nominal_code', 'notes', 'customer_ref'],
                  'CN': ['name', 'business_year', 'date', 'originating_account', 'amount', 'my_ref', 'my_invoice']}
        names = {'C': 'Cash',
                 'B': 'Bank',
                 'R': 'Receipt',
                 'I': 'Invoice',
                 'M': 'Mileage',
                 'CN': 'Credit note'}
        transaction_type = self.kwargs["transaction_type"]
        self.title = names[transaction_type]
        self.fields = fields[transaction_type]
        self.success_url = reverse_lazy('bookish-{}_list'.format(self.title.lower()))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        transaction_type = self.kwargs["transaction_type"]
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.transaction = m.Transaction.objects.create(company=self.request.user.company_set.first(),
                                                               transaction_type=transaction_type)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

'''
    Still needs a bit of work....
'''


class TransactionItemRevisionView(ListView):

    def get_queryset(self):
        transaction_id = self.kwargs["transaction_id"]
        queryset = m.TransactionRevision.objects.order_by('-revision_datetime').filter(transaction_id=transaction_id)
        # Also want to make the transaction id usable in the view. Add it to the object_list that is returned.
        queryset.transaction_id = transaction_id[:8]  # How can we use mini_uuid here?
        return queryset


class AccountancyFirmListView(ListView):
    queryset = m.AccountancyFirm.objects.all()


class CompanyListView(ListView):
    queryset = m.Company.objects.all()
