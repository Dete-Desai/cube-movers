from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import localtime

from phonenumber_field.modelfields import PhoneNumberField


ROOM_CHOICE = (
    ('office', 'office'),
    ('house', 'house')
)


class Source(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __unicode__(self):
        return self.name


class StaffProfile(models.Model):
    user = models.OneToOneField(User)
    phone_number = PhoneNumberField(max_length=50, null=True)
    code = models.CharField(max_length=10, null=True)
    signature = models.ImageField(
        upload_to='signatures', null=True, blank=True)


class Customer(models.Model):
    user = models.OneToOneField(User)
    source = models.ForeignKey(Source)
    full_name = models.CharField(max_length=50)
    secondary_name = models.CharField(max_length=50, blank=True, null=True)
    phone_number = PhoneNumberField(max_length=30)
    secondary_phone_number = PhoneNumberField(
        max_length=30, blank=True, null=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    secondary_email = models.EmailField(blank=True, null=True)

    def get_formatted_datetime(self):
        return self.created_time.strftime('%d-%m-%Y %H:%M')

    def get_absolute_url(self):
        return "{pk}".format(pk=self.pk)

    def __unicode__(self):
        return "{} - {} ".format(self.full_name, self.user.email)


class MoveStatus(models.Model):
    name = models.CharField(max_length=30, unique=True)


class Vehicle(models.Model):
    make = models.CharField(max_length=30)
    model = models.CharField(max_length=30)
    registration = models.CharField(max_length=30)
    cbm = models.CharField(max_length=30)

    def __unicode__(self):
        return self.registration


class PropertyDetails(models.Model):
    primary_area_name = models.CharField(max_length=30, null=True)
    secondary_area_name = models.CharField(max_length=30, null=True)
    street_name = models.CharField(max_length=30, null=True)
    secondary_street_name = models.CharField(max_length=30, null=True)
    gate_color = models.CharField(max_length=30, null=True)
    compound_name = models.CharField(max_length=30, null=True)
    house_no = models.CharField(max_length=30, null=True)
    floor = models.CharField(max_length=30, null=True)
    land_marks = models.CharField(max_length=30, null=True)
    side_of_road = models.CharField(max_length=30, null=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)


class PropertyDestinationDetails(models.Model):
    primary_area_name = models.CharField(max_length=30, null=True)
    secondary_area_name = models.CharField(max_length=30, null=True)
    street_name = models.CharField(max_length=30, null=True)
    secondary_street_name = models.CharField(max_length=30, null=True)
    gate_color = models.CharField(max_length=30, null=True)
    compound_name = models.CharField(max_length=30, null=True)
    house_no = models.CharField(max_length=30, null=True)
    floor = models.CharField(max_length=30, null=True)
    land_marks = models.CharField(max_length=30, null=True)
    side_of_road = models.CharField(max_length=30, null=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)


class Survey(models.Model):
    surveyor = models.ForeignKey(User, null=True)
    vehicle = models.ForeignKey(Vehicle, null=True)
    survey_time = models.DateTimeField(null=True)
    move_time = models.DateTimeField(null=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def get_formatted_survey_date(self):
        if self.survey_time:
            local_time = localtime(self.survey_time)
            return local_time.strftime('%b %-d, %Y %-I:%M %p')
        else:
            return self.survey_time

    @property
    def get_surveyor_full_name(self):
        if self.surveyor:
            return self.surveyor.get_full_name()
        return ""


class MoveTeam(models.Model):
    pass


class MoveTeamMember(models.Model):
    move_team = models.ForeignKey(MoveTeam)
    user = models.ForeignKey(User)
    is_lead = models.BooleanField(default=False)


class TraineeTeam(models.Model):
    pass


class TraineeTeamMember(models.Model):
    trainee_team = models.ForeignKey(TraineeTeam)
    user = models.ForeignKey(User)


class MoveType(models.Model):
    name = models.CharField(max_length=30, unique=True)
    currency = models.CharField(max_length=10, default='KES')
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name


class MoveTypeDetails(models.Model):
    name = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name


class Delight(models.Model):
    smartness = models.IntegerField(null=True)
    time = models.IntegerField(null=True)
    courtesy = models.IntegerField(null=True)
    creativity = models.IntegerField(null=True)
    explanation = models.IntegerField(null=True)
    willingness = models.IntegerField(null=True)
    leader_competence = models.IntegerField(null=True)
    team_competence = models.IntegerField(null=True)
    care_attention = models.IntegerField(null=True)
    satisfaction = models.IntegerField(null=True)
    total = models.IntegerField(null=True)
    comments = models.TextField(null=True)


class Branch(models.Model):
    branch_name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.branch_name


class Move(models.Model):

    customer = models.ForeignKey(Customer)
    move_status = models.ForeignKey(MoveStatus)
    move_type = models.ForeignKey(MoveType, null=True)
    move_type_details = models.ForeignKey(MoveTypeDetails, null=True)
    hash = models.TextField(null=True)
    property_details = models.OneToOneField(PropertyDetails)
    property_destination_details = models.OneToOneField(
        PropertyDestinationDetails, null=True)
    survey = models.OneToOneField(Survey)
    move_team = models.ForeignKey(MoveTeam, null=True)
    trainee_team = models.ForeignKey(TraineeTeam, null=True)
    move_vehicles = models.ManyToManyField(Vehicle)
    token = models.CharField(max_length=10, null=True)
    is_credit = models.BooleanField(default=False)
    delight = models.OneToOneField(Delight, null=True)
    move_date = models.DateTimeField(null=True)
    move_rep = models.ForeignKey(User, related_name="move_rep")
    special_instructions = models.TextField(null=True)
    accessibility_instructions = models.TextField(null=True)
    branch = models.ForeignKey(Branch, null=True)

    departure_from_office = models.DateTimeField(null=True)
    arrival_at_client = models.DateTimeField(null=True)
    departure_from_client = models.DateTimeField(null=True)
    arrival_at_office = models.DateTimeField(null=True)
    speedometer_in = models.FloatField(null=True, default=0.0)
    speedometer_out = models.FloatField(null=True, default=0.0)
    fuel_intake = models.FloatField(null=True, default=0.0)

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta(object):
        permissions = (
            ("can_view_unassigned_move", "Can view unassigned move"),)

    @property
    def kms_run(self):
        return self.speedometer_in - self.speedometer_out

    def get_formatted_datetime(self):
        return self.created_time.strftime('%d-%m-%Y %H:%M')

    def get_absolute_url(self):
        return "/inquiry/{pk}".format(pk=self.pk)

    def get_formatted_move_date(self):
        move_time = self.survey.move_time if self.survey.move_time else self.move_date
        if move_time:
            local_time = localtime(move_time)
            return local_time.strftime('%b %-d, %Y %-I:%M %p')
        else:
            return move_time


class MoveLogs(models.Model):
    move_status = models.ForeignKey(MoveStatus, null=True)
    move = models.ForeignKey(Move, null=True)
    move_rep = models.ForeignKey(User, null=True)
    timestamp = models.DateField(auto_now_add=True)


class Item(models.Model):
    name = models.CharField(max_length=30)
    vol = models.FloatField()

    def __str__(self):
        return self.name


class Room(models.Model):
    name = models.CharField(max_length=30, unique=True)
    room_type = models.CharField(
        choices=ROOM_CHOICE, max_length=50, default='house')
    items = models.ManyToManyField(Item)

    def __str__(self):
        return self.name


class QuoteItemType(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class QuoteItemDefault(models.Model):
    quote_item_type = models.ForeignKey(QuoteItemType, null=True)
    item = models.CharField(max_length=30, unique=True)
    cost = models.FloatField()


class Quotation(models.Model):
    total_cost = models.FloatField(default=0.0, null=True)
    profit_margin = models.FloatField(default=0.0, null=True)
    quote_number = models.CharField(max_length=50, default="")
    commission = models.FloatField(default=0.0, null=True)
    selling_price = models.FloatField(default=0.0, null=True)
    vat = models.FloatField(default=16.0, null=True)
    charge_out_price = models.FloatField(default=0.0, null=True)
    hash = models.TextField(null=True)
    status = models.CharField(max_length=30, default="not sent")
    reject_reason = models.TextField(null=True)
    move_rep = models.ForeignKey(User, null=True)
    created_time = models.DateTimeField(auto_now_add=True)
    sent_time = models.DateTimeField(null=True)
    reply_time = models.DateTimeField(null=True)
    discount = models.FloatField(default=0.0)

    class Meta(object):
        permissions = (
            ("can_view_unassigned_quote", "Can view unassigned quote"),)

    def get_turnaround_time(self):
        t = self.reply_time - self.sent_time
        return str(t)


class QuoteItem(models.Model):
    quotation = models.ForeignKey(Quotation)
    quote_item_type = models.ForeignKey(QuoteItemType, null=True)
    item = models.CharField(max_length=30)
    cost = models.FloatField()
    units = models.IntegerField()


class Checklist(models.Model):
    quotation = models.OneToOneField(Quotation, null=True)
    move = models.OneToOneField(Move)
    total_vol = models.FloatField(default=0.0, null=True)
    total_cost = models.FloatField(default=0.0, null=True)


class Office(models.Model):
    """
    This decribes a type of an office.

    The concept is easily explained where a buliding can
    have multiple offices that require a move to occur
    """
    office_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.office_name


class ChecklistItem(models.Model):
    checklist = models.ForeignKey(Checklist)
    room = models.ForeignKey(Room)
    office = models.ForeignKey(Office, null=True)
    item_backup = models.CharField(max_length=30)
    item = models.ForeignKey(Item, null=True, blank=True)
    vol = models.FloatField()
    qty = models.IntegerField(default=0, null=True)
    box_ref = models.CharField(max_length=50, null=True)
    is_packed = models.BooleanField(default=False)
    is_unpacked = models.BooleanField(default=False)


class Settings(models.Model):
    name = models.CharField(max_length=255, unique=True)
    value = models.CharField(max_length=255, unique=True)


class QuoteDocument(models.Model):
    """
    Keep a record of edited quotation documents
    """

    move = models.OneToOneField(Move)
    quote_content = models.TextField()
