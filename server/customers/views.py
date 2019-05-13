import hashlib
import urllib
from django.contrib import messages
from django.http.response import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.admin.models import LogEntry, ADDITION
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from datatableview.views import DatatableView
from datetime import datetime
from django.views import generic
from datatableview import helpers
from core.models import (
    Customer, Move, MoveStatus, PropertyDetails, PropertyDestinationDetails,
    MoveLogs, Survey, Settings, Quotation, Checklist, MoveTeam, TraineeTeam,
    Delight, Source, MoveType)
from core.utils import send_email, generate_quotation_number
from core.permissions import (
    can_view_inquiry
)
from inquiries.forms import NewCustomerInquiryForm
from .forms import CustomerForm, CustomerEditForm


class ListCustomersView(DatatableView):
    model = Customer
    template_name = 'customers/list.html'

    datatable_options = {
        'columns': [
            ("Customer ID", 'id', helpers.link_to_model),
            ("Customer Name", 'full_name'),
            ("Created Time", 'get_formatted_datetime'),
        ],
    }


class CreateCustomersView(generic.edit.FormView):
    template_name = 'customers/create.html'
    form_class = CustomerForm
    success_url = '/inquiry/'

    @method_decorator(login_required)
    @method_decorator(user_passes_test(can_view_inquiry))
    def dispatch(self, *args, **kwargs):
        return super(CreateCustomersView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        # create a new User account
        user = User()
        # in order to overcome Django's nuances, email is repeated in
        # both the username and email field
        user.username = form.cleaned_data['email']
        user.email = form.cleaned_data['email']
        user.is_active = False
        user.save()

        # create a Customer profile and associate with above User account
        customer = Customer()
        customer.user = user
        customer.source = form.cleaned_data['source']
        customer.full_name = form.cleaned_data['full_name']
        customer.phone_number = form.cleaned_data['phone_number']
        customer.secondary_email = form.cleaned_data['secondary_email']

        # optionals
        customer.secondary_name = form.cleaned_data['secondary_name']
        customer.secondary_phone_number = form.cleaned_data['secondary_phone_number']
        customer.save()

        LogEntry.objects.log_action(
            user_id=self.request.user.pk,
            content_type_id=ContentType.objects.get_for_model(customer).pk,
            object_id=customer.pk,
            object_repr=force_unicode(customer),
            action_flag=ADDITION
        )

        # create a move record in the inquiry stage
        move = Move()
        move.customer = customer
        move.branch = form.cleaned_data['branch']
        move.move_status = MoveStatus.objects.get(name="inquiry")
        move.move_type = form.cleaned_data['move_type']
        move.move_type_details = form.cleaned_data['move_type_details']
        # generate hash using django's password maker
        hash = str(datetime.now()) + user.email
        hash = make_password(password=hash, salt=None, hasher='default')
        hash = urllib.quote_plus(hash)
        move.hash = hash

        # create property and survey objects
        property_details = PropertyDetails()
        property_details.save()

        property_destination = PropertyDestinationDetails()
        property_destination.save()

        survey = Survey()
        survey.save()

        move.property_details = property_details
        move.property_destination_details = property_destination
        move.survey = survey
        # assign current user as move_rep
        move.move_rep = self.request.user
        move.save()

        LogEntry.objects.log_action(
            user_id=self.request.user.pk,
            content_type_id=ContentType.objects.get_for_model(move).pk,
            object_id=move.pk,
            object_repr=force_unicode(move),
            action_flag=ADDITION
        )

        # create checklist with empty quotation
        quote = Quotation()
        quote.quote_number = generate_quotation_number(customer)
        quote.profit_margin = float(
            Settings.objects.get(name='profit_margin').value)
        quote.commission = float(
            Settings.objects.get(name='commission').value)
        quote.vat = float(Settings.objects.get(name='vat').value)
        quote.save()

        checklist = Checklist()
        checklist.move = move
        checklist.quotation = quote
        checklist.save()

        # create MoveTeam, TraineeTeam, MoveVehicle, Packlist
        move.move_team = MoveTeam.objects.create()
        move.trainee_team = TraineeTeam.objects.create()
        move.delight = Delight.objects.create()

        move.save()

        # log the inquiry
        log = MoveLogs()
        log.move_status = MoveStatus.objects.get(name="inquiry")
        log.move = move
        log.move_rep = self.request.user
        log.save()

        # email the customer with a hashed callback url containing
        # move_id to finish the details
        email_ctx = {
            'full_name': customer.full_name,
            'move_id': move.id,
            'hash': hash,
            'host': self.request.get_host(),
            'subject': 'Cubemovers Move Inquiry',
            'title': 'Inquiry details',
            'recipients': [user.email]
        }

        send_email('inquiries/email.txt', email_ctx)

        text = "Inquiry and Customer account successfully created"
        messages.add_message(self.request, messages.INFO, text)

        return HttpResponseRedirect(self.success_url)


class CustomerDetailView(generic.DetailView):
    model = Customer
    template_name = 'customers/details.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CustomerDetailView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        cxt = super(CustomerDetailView, self).get_context_data(**kwargs)
        customer = self.get_object()
        moves = Move.objects.filter(customer=customer)
        payload = {
            'customer': customer,
            'moves': moves,
            'form': CustomerEditForm(instance=customer),
            'inquiry_form': NewCustomerInquiryForm()
        }
        cxt.update(payload)
        return cxt


class CustomerUpdateView(generic.UpdateView):
    model = Customer
    form_class = CustomerEditForm
    template_name = 'customers/edit-modal.html'

    def get_success_url(self):
        obj = self.get_object()
        return '/customers/{}/'.format(obj.id)
