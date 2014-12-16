from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
import bookish.models as m


class CashListView(ListView):
    queryset = m.Transaction.objects.filter(transaction_type='C')


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
        #transaction_id = self.kwargs.get("transaction_id")  #returns None if not exist
        transaction_id = self.kwargs["transaction_id"]  #returns an exception if it doesn't exist
        queryset = m.TransactionRevision.objects.order_by('-revision_datetime').filter(transaction_id=transaction_id)
        return queryset


class AccountancyFirmListView(ListView):
    queryset = m.AccountancyFirm.objects.all()


class CompanyListView(ListView):
    queryset = m.Company.objects.all()
