from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from core.models import (
    QuoteItem, QuoteItemDefault, Quotation)
from core.permissions import (
    can_view_quotes,
)


class QuotationDetailViewMixin(object):

    def get_context_data(self, **kwargs):
        cxt = super(QuotationDetailViewMixin, self).get_context_data(**kwargs)
        quote = self.get_object()
        quote_items = QuoteItem.objects.filter(quotation=quote)
        items = QuoteItemDefault.objects.all()

        profit_margin_value = (quote.profit_margin / 100) * quote.total_cost
        commission_value = (quote.commission / 100) * profit_margin_value
        move_date = quote.checklist.move.move_date
        payload = {
            'move': quote.checklist.move,
            'quote': quote,
            'move_date': move_date.strftime('%m/%d/%Y %I:%M %p') if move_date else " ",
            'quote_items': quote_items,
            'items': items,
            'profit_margin_value': profit_margin_value,
            'commission_value': commission_value
        }
        cxt.update(payload)
        return cxt

    @method_decorator(login_required)
    @method_decorator(user_passes_test(can_view_quotes))
    def dispatch(self, *args, **kwargs):
        return super(QuotationDetailViewMixin, self).dispatch(*args, **kwargs)

    def get_object(self):
        quotation_id = self.kwargs.get(self.pk_url_kwarg)
        return Quotation.objects.get(id=quotation_id)
