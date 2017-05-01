from django.db import models
from django import forms
from django.utils import timezone
from django.core.mail import send_mail

#############################################
# STUDENT CLASSES #
#############################################
class StudentBase(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    student_id = models.PositiveIntegerField(primary_key=True, unique=True, verbose_name="900 Number")
    student_email = models.EmailField(max_length=100, default="firstname.lastname@student.nmt.edu", verbose_name="NMT Email")
    emergency_contact = models.CharField(max_length=40, default='none given', blank=True)
    contact_relationship = models.CharField(max_length=100, default='none given', blank=True)
    emergency_contact_phone = models.CharField(default='(123) 456-7890', max_length=30, verbose_name="Emergency Contact Phone Number")
    home_addr = models.TextField(max_length=100, default='none given', blank=True, verbose_name="Home Address")
    car_plate = models.CharField(max_length=20, default='none given', blank=True)
    car_info = models.TextField(max_length=100, help_text="Make/model/description of car", default='none given', blank=True)

    class Meta:
        abstract = True

class Resident(StudentBase):
    hall = models.ForeignKey('ResidenceHall', null=True, on_delete=models.SET_NULL, verbose_name="Residence Hall")
    room_number = models.CharField(max_length=10, null=True)
    RA = models.ForeignKey('RA', null=True, on_delete=models.SET_NULL)
    notes = models.TextField(max_length=1000, blank=True, default='No notes here!', verbose_name="Additional notes on resident")

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

class RA(StudentBase):
    hall = models.ForeignKey('ResidenceHall', null=True, on_delete=models.SET_NULL, verbose_name="Residence Hall")
    room_number = models.CharField(max_length=10, null=True)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

class ResidenceHall(models.Model):
    name = models.CharField(null=True, max_length=100)
    rlc = models.ForeignKey('auth.user', verbose_name="Residential Life Coordinator")

    def __str__(self):
        return '%s' % (self.name)

#############################################
# FORM CLASSES #
#############################################

#base ABSTRACT form class
class FormBase(models.Model):
    author = models.ForeignKey('RA', null=True)
    hall = models.ForeignKey('ResidenceHall', null=True, verbose_name="Residence Hall")
    room_number = models.CharField(blank=True, null=True, max_length=10)
    date = models.DateTimeField(null=True)

    class Meta:
        abstract = True

class RoomEntryRequestForm(FormBase):
    student = models.ForeignKey('Resident', null=True, on_delete=models.SET_NULL, verbose_name="Resident name")
    student_sig = models.BooleanField(default=False, verbose_name="Resident signed")
    verification_method = models.TextField(null=True, max_length=40)

    def send_copy(self):
        send_mail('Hello!')

    def __str__(self):
        return '%s %s Room Entry Request on %s' % (self.student.first_name, self.student.last_name, self.date)

class ProgramPacket(FormBase):
    program_title = models.TextField(null=True, max_length=100)
    program_date = models.DateField(null=True)
    program_time = models.TimeField(null=True)
    location1 = models.TextField(max_length=50, null=True, verbose_name="First choice location")
    space_need_reservation1 = models.BooleanField(verbose_name="(First choice) reservation needed?")
    reservation_made1 = models.BooleanField(verbose_name="(First choice) reservation made")
    location2 = models.TextField(null=True, max_length=50, verbose_name="Second choice location")
    space_need_reservation2 = models.BooleanField(verbose_name="(Second choice) reservation needed?")
    reservation_made2 = models.BooleanField(verbose_name="(Second choice) reservation made")
    target_audience = models.TextField(null=True, max_length=200)
    advertising = models.TextField(null=True, max_length=200, verbose_name="Advertising method")
    coordinator_approval = models.BooleanField(default=False, verbose_name="Coordinator approval")
    coordinator_sig = models.ForeignKey('auth.user', blank=True, verbose_name="Signing RLC", null=True)
    sig_date = models.DateField(null=True, verbose_name="Signed date")
    program_description = models.TextField(null=True, max_length=500)
    supplies = models.TextField(null=True, max_length=300, verbose_name="Supplies needed")
    proposed_cost = models.PositiveIntegerField(null=True, verbose_name="Proposed cost (to the nearest dollar)")

    @property
    def approved(self):
        if self.coordinator_approval == True:
            return True
        return False

    def __str__(self):
        return '%s Program Packet from %s submitted on %s' % (self.program_title, self.author, self.date)

class SafetyInspectionViolation(FormBase):
    prohibited_appliances = models.BooleanField(default=False)
    candle_incense = models.BooleanField(default=False, verbose_name="Candles or incense")
    extension_cords = models.BooleanField(default=False)
    lounge_furniture = models.BooleanField(default=False, verbose_name="Lounge furniture in room")
    trash_violation = models.BooleanField(default=False)
    animals = models.BooleanField(default=False)
    alcohol_drugs = models.BooleanField(default=False, verbose_name="Alcohol or drugs")
    fire_safety = models.BooleanField(default=False)
    other = models.TextField(null=True, max_length=200, blank=True)
    sig = models.BooleanField(default=False, verbose_name="Signed")
    additional_action = models.BooleanField(default=False, verbose_name="Additional action required")

    def __str__(self):
        return 'Inspection Violation - %s %s' % (self.hall, self.room_number)

class FireAlarm(FormBase):
    occurence_time = models.TimeField(null=True, verbose_name="Time of the incident")
    specific_location = models.TextField(null=True, max_length=50, verbose_name="Specific location of the incident")
    ALARM_CAUSES = (
        ('PULL_BOX', 'Pull Box'),
        ('HEAT', 'Heat Detector'),
        ('SMOKE', 'Smoke Detector'),
        ('MALFUNCTION', 'Malfunction'),
        ('DRILL', 'Fire Drill'),
        ('UNKNOWN', 'Unknown'),
        ('FIRE', 'Fire')
    )
    cause = models.CharField(choices=ALARM_CAUSES, null=True, max_length=20)
    fire_explanation = models.TextField(max_length=200, null=True, blank=True, help_text="If there was an actual fire, please explain here")
    other_ras = models.TextField(max_length=500, null=True, default="none", verbose_name="Other RAs involved or present")
    notes = models.TextField(max_length=500, null=True, blank=True, verbose_name="Additional notes")

    def __str__(self):
        return '%s Fire Alarm on %s' % (self.hall, self.date)
