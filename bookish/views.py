from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
import bookish.models as m


class HomePageView(TemplateView):
    template_name = "bookish/index.html"


class CashListView(ListView):
    def get_queryset(self):
        # In urls.py we pass a value for transaction_type - C for cash, B for Bank etc
        transaction_type = self.kwargs["transaction_type"]
        # Return all transactions of the requested type
        queryset = m.Transaction.objects.filter(transaction_type=transaction_type)
        return queryset


class CashCreate(CreateView):
    model = m.TransactionRevision
    fields = ['name', 'business_year', 'date', 'originating_account', 'amount', 'nominal_code', 'notes']
    success_url = reverse_lazy('bookish-cash_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.transaction = m.Transaction.objects.create(company=self.request.user.company_set.first(),
                                                               transaction_type='C')
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class CashItemRevisionView(ListView):
    
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
