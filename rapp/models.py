from django.db import models
from django.utils import timezone
from django.core.mail import send_mail

#############################################
# STUDENT CLASSES #
#############################################
class StudentBase(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    id = models.PositiveIntegerField(primary_key=True, default=0, unique=True, help_text="Unique 900# ID for this particular student")
    student_email = models.EmailField(max_length=100, default='lattaeo@gmail.com')
    emergency_contact = models.CharField(max_length=40, default='none given', blank=True)
    contact_relationship = models.CharField(max_length=100, default='none given', blank=True)
    emergency_contact_phone = models.PositiveIntegerField(default='1234567890', blank=True)
    home_addr = models.TextField(max_length=100, default='none given', blank=True)
    car_plate = models.CharField(max_length=20, default='none given', blank=True)
    car_info = models.TextField(max_length=100, help_text="Make/model/description of car", default='none given', blank=True)

    class Meta:
        abstract = True

class Resident(StudentBase):
    hall = models.ForeignKey('ResidenceHall', null=True, on_delete=models.SET_NULL)
    room_number = models.CharField(max_length=10, null=True)
    RA = models.ForeignKey('RA', null=True, on_delete=models.SET_NULL)
    notes = models.TextField(max_length=1000, blank=True, default='No notes here!')

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

class RA(StudentBase):
    hall = models.ForeignKey('ResidenceHall', null=True, on_delete=models.SET_NULL)
    room_number = models.CharField(max_length=10, null=True)

    def __str__(self):
        return '%s %s: %s' % (self.first_name, self.last_name, self.hall)

class ResidenceHall(models.Model):
    name = models.CharField(max_length=100)
    rlc = models.ForeignKey('auth.user')
    id = models.PositiveIntegerField(primary_key=True, default=0, unique=True, help_text="Just an ID #")

    def __str__(self):
        return '%s' % (self.name)

#############################################
# FORM CLASSES #
#############################################

#base ABSTRACT form class
class FormBase(models.Model):
    author = models.ForeignKey('RA')
    hall = models.ForeignKey('ResidenceHall')
    room_number = models.TextField(max_length=10)
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True

class RoomEntryRequestForm(FormBase):
    student = models.ForeignKey('Resident', null=True, on_delete=models.SET_NULL, )
    student_sig = models.FileField()
    ra_sig = models.BooleanField(default=False)
    verification_method = models.TextField(max_length=40)

    def send_copy(self):
        send_mail('Hello!')

    def __str__(self):
        return '%d - %s %s Room Entry Request on %s' % (self.id, self.student.first_name, self.student.last_name, self.date)

class ProgramPacket(FormBase):
    program_title = models.TextField(max_length=100)
    program_date = models.DateField()
    program_time = models.TimeField()
    location1 = models.TextField(max_length=50)
    space_need_reservation1 = models.BooleanField()
    reservation_made1 = models.BooleanField()
    location2 = models.TextField(max_length=50)
    space_need_reservation2 = models.BooleanField()
    reservation_made2 = models.BooleanField()
    target_audience = models.TextField(max_length=200)
    advertising = models.TextField(max_length=200)
    coordinator_approval = models.BooleanField()
    coordinator_sig = models.FileField()
    sig_date = models.DateField()
    program_description = models.TextField(max_length=500)
    supplies = models.TextField(max_length=300)
    proposed_cost = models.PositiveIntegerField()

class SafetyInspectionViolation(FormBase):
    prohibited_appliances = models.BooleanField(default=False)
    candle_incense = models.BooleanField(default=False)
    extension_cords = models.BooleanField(default=False)
    lounge_furniture = models.BooleanField(default=False)
    trash_violation = models.BooleanField(default=False)
    animals = models.BooleanField(default=False)
    alcohol_drugs = models.BooleanField(default=False)
    fire_safety = models.BooleanField(default=False)
    other = models.TextField(max_length=200, blank=True)
    sig = models.FileField()
    additional_action = models.BooleanField(default=False)

class FireAlarm(FormBase):
    occurence_time = models.TimeField()
    specific_location = models.TextField(max_length=50)
    ALARM_CAUSES = (
        ('PULL_BOX', 'Pull Box'),
        ('HEAT', 'Heat Detector'),
        ('SMOKE', 'Smoke Detector'),
        ('MALFUNCTION', 'Malfunction'),
        ('DRILL', 'DRILL'),
        ('UNKNOWN', 'Unknown'),
        ('FIRE', 'Fire')
    )

    fire_explanation = models.TextField(max_length=200, blank=True, help_text="If there was an actual fire, please explain here")
    other_ras = models.ManyToManyField('RA', null=True, related_name='otherRAs')
    notes = models.TextField(max_length=500)
