from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from celery import shared_task


@shared_task(name="send_email_helper")
def send_email_helper(subject, text_content, html_content, from_email, to):

    try:
        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    except Exception as e:
        send_email_helper.retry(countdown=60, exc=e, max_retries=5)


@shared_task(name="send_email")
def send_email(**kwargs):
    # email surveyor
    try:
        plaintext = get_template(kwargs['plaintext'])
        htmly = get_template(kwargs['html'])

        d = kwargs['context']

        subject, from_email, to = kwargs['subject'], kwargs['from'], kwargs['to']
        text_content = plaintext.render(d)
        html_content = htmly.render(d)
        recipients = to if isinstance(to, list) else [to]
        msg = EmailMultiAlternatives(subject, text_content, from_email, recipients)
        msg.attach_alternative(html_content, "text/html")

        if 'file' in kwargs:
            msg.attach(kwargs['file'].name, kwargs['file'].read())

        if 'cc' in kwargs:
            msg.cc = kwargs['cc'] if isinstance(kwargs['cc'], list) else [kwargs['cc']]

        if 'inventory' in kwargs:
            msg.attach('Inventory.pdf', kwargs['inventory'])

        if 'delight' in kwargs:
            msg.attach('Delight_Form.pdf', kwargs['delight'])

        if 'booking_order' in kwargs:
            msg.attach('Booking_Order.pdf', kwargs['booking_order'])

        if 'important_notice' in kwargs:
            msg.attach_file('core/templates/attachments/important_notice.pdf')

        if 'local_quote' in kwargs:
            msg.attach('local_Removal_Quote.pdf', kwargs['local_quote'])

        msg.send()
    except Exception as e:
        send_email.retry(countdown=60, exc=e, max_retries=5)
