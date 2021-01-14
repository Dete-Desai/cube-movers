from django.http import HttpResponse
import hashlib
from datetime import datetime
from django.template import Context
from django.template.loader import get_template
from django.conf import settings
from .AfricasTalkingGateway import AfricasTalkingGateway
from .tasks import send_email_helper
from .models import (
    Move, MoveStatus, ChecklistItem, QuoteItem)


def filter_queryset(user, stage, perm):
    """
    A helper function to determine the queryset that will he returned
    This filters based on who should see all the records
    Or specific records assigned to them
    """
    if perm:
        if user.has_perm(perm):
            return Move.objects.filter(move_status=MoveStatus.objects.get(
                name=stage))

        elif stage == "quotation" or stage == "survey":
            return Move.objects.filter(
                move_status=MoveStatus.objects.get(name=stage),
                survey__surveyor=user)

        elif stage == "pre-move" or stage == "move" or stage == "post-move" \
                or stage == "complete":
            return Move.objects.filter(
                move_status=MoveStatus.objects.get(name=stage),
                move_team__moveteammember__user=user)

        return HttpResponse(status=404)


def send_email(body_tpl, context):
    plaintext = get_template(body_tpl)
    htmly = get_template('core/common/email.html')
    text_content = plaintext.render(Context(context))
    cxt = context
    cxt['body'] = text_content
    d = Context(cxt)
    html_content = htmly.render(d)
    send_email_helper.delay(
        context['subject'], text_content, html_content,
        settings.EMAIL_HOST_USER, cxt['recipients']
    )


def send_sms(to, message):
    username = settings.CUBEMOVERS['sms_username']
    apikey = settings.CUBEMOVERS['sms_apikey']
    sender = 'CubeMovers'

    gateway = AfricasTalkingGateway(username, apikey)
    gateway.sendMessage(str(to), message, sender)


def recompute_checklist_totals(checklist):
    items = ChecklistItem.objects.filter(checklist=checklist)
    total = 0.0
    for item in items:
        total += (item.vol * item.qty)

    checklist.total_vol = total
    checklist.save()


def recompute_quote_totals(quote):
    total = 0.0

    # total_cbm_cost = quote.checklist.total_cost
    # total += total_cbm_cost

    items = QuoteItem.objects.filter(quotation=quote)
    for item in items:
        total += (item.units * item.cost)

    quote.total_cost = total
    profit_margin = (quote.profit_margin / 100) * total
    commission = (quote.commission / 100) * profit_margin
    quote.selling_price = quote.total_cost + profit_margin + commission
    quote.charge_out_price = quote.selling_price + ((quote.vat / 100) * quote.selling_price)
    quote.charge_out_price = quote.charge_out_price - quote.discount
    quote.save()


def count_records(user, stage, perm):
    """
    Get the number of record that a user can be able to see.
    This is used to display the counts on the dashboard interface
    """

    if perm:
        if user.has_perm(perm):
            return Move.objects.filter(move_status=MoveStatus.objects.get(
                name=stage)).count()

        elif stage == "quotation" or stage == "survey":
            return Move.objects.filter(
                move_status=MoveStatus.objects.get(name=stage),
                survey__surveyor=user).count()

        elif stage == "pre-move" or stage == "move" or stage == "post-move" \
                or stage == "complete":
            return Move.objects.filter(
                move_status=MoveStatus.objects.get(name=stage),
                move_team__moveteammember__user=user).count()


def get_customer_emails(customer):
    recipients = [customer.user.email]
    if customer.secondary_email:
        recipients.append(customer.secondary_email)
    return recipients


def generate_quotation_number(move):
    date_hash = hashlib.sha256(str(datetime.now())).hexdigest()[:6]
    return "{}/{}/{}".format(move.customer.id, move.id, date_hash)
