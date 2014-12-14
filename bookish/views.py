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
    """How do I pass the transaction ID to this class?"""
    queryset = m.TransactionRevision.objects.order_by('-revision_datetime').filter(transaction_id="0a5bcc1a-87e4-4257-9206-7432eaf7fb60")
    """And really we want to sort these. Does the below work?"""
    #queryset = m.TransactionRevision.objects.filter(transaction_id="0a5bcc1a-87e4-4257-9206-7432eaf7fb60")
    #def ordered_revision(self):
    #    return self.queryset_set.order_by('-revision_datetime')


class AccountancyFirmListView(ListView):
    queryset = m.AccountancyFirm.objects.all()


class CompanyListView(ListView):
    queryset = m.Company.objects.all()
