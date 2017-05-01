import datetime
import hashlib
import hmac
import base64
from django.db import models
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib import postgres
from django.core.signing import Signer
import django.contrib.postgres.fields #force the module to load

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
    user = models.OneToOneField('auth.user', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

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
    verification_method = models.TextField(max_length=40)

    def send_copy(self):
        send_mail('Hello!')

    def __str__(self):
        return '%d - %s %s Room Entry Request on %s' % (self.id, self.student.first_name, self.student.last_name, self.date)

    def name(self):
        return 'Room Entry Requests'

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

    @property
    def approved(self):
        if self.coordinator_approval == True:
            return True
        return False

    def __str__(self):
        return 'Program Packets'

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

    def __str__(self):
        return 'Safety Inspection Violation Reports'

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
    other_ras = models.TextField(max_length=500, default="none")
    notes = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return 'Fire Alarm Reports'

#############################################
# API
#############################################

class Room(models.Model):
    id = models.AutoField(primary_key=True)
    hall = models.ForeignKey("ResidenceHall")
    max_residents = models.IntegerField()
    name = models.CharField(max_length=100)

    def is_full(self):
        # return via it's back relation if the room is full
        pass

    def free(self):
        # return via back relation and max_residents the number of free slots
        pass

    def valid(self):
        # if there are free slots or the room is full the room is valid, if the room is OVER full it's is invalid
        pass


class ConditionReport(models.Model):
    id = models.AutoField(primary_key=True)
    room = models.ForeignKey("Room")
    resident = models.ForeignKey("Resident")
    author = models.ForeignKey('User')
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    editedby = models.ForeignKey('User')
    images = postgres.fields.ArrayField(base_field=models.IntegerField)

    def empty(self):
        # return via back relation if no residents are assigned to the room
        pass


def now_add_hours_lambda(h):
    return lambda: timezone.now + datetime.timedelta(hours=h)


class AuthToken(models.Model):
    token = models.CharField(primary_key=True, max_length=64, unique=True, db_index=True)
    user = models.ForeignKey('auth.user')
    issued = models.DateTimeField(auto_now_add=True)
    expires = models.DateTimeField(default=now_add_hours_lambda(4))
    valid = models.BooleanField(default=True)

    def generate_token(self):
        '''issued = isoformat timestamp'''
        signer = Signer()
        mac = self.user.username + self.issued.isoformat()
        signed_mac = signer.sign(mac)
        token = hashlib.sha256(signed_mac.encode('utf-8'))
        digest = base64.urlsafe_b64encode(token.digest())
        self.token = digest
        return digest


class Note(models.Model):
    id = models.AutoField(primary_key=True)
    top = models.BooleanField(default=False)
    resident = models.ForeignKey('Resident')
    author = models.ForeignKey('User')
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    content = models.TextField(max_length=1000)  # TODO perhaos be json field
    # comments = postgres.fields.ArrayField(base_field=models.IntegerField)  # Access through back related set
    access = models.ManyToManyField("User")
    access_level = models.CharField(max_length=2, choices=User.ACCESS_LEVELS, default=User.RA)



#############################################
# UNUSED For later Template system
#############################################
class FormTemplate(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    author = models.ForeignKey('User')
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    editedby = models.ForeignKey('User')
    templatedata = models.ForeignKey('FromTemplateData')
    # versions = postgres.fields.ArrayField(base_field=models.IntegerField) # Access through back related set

    def __str__(self):
        return '%s' % (self.name)


class FromTemplateData(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('User')
    from_template = models.ForeignKey('FormTemplate')
    template = models.TextField(max_length=1000)
    pairs = postgres.fields.JSONField()  # JSON pairs of names to types


class FormData(models.Model):

    INCOMPLEATE = "IN"
    COMPLEATE = "CO"

    STATUSES = (
        ("IN", "Incompleate"),
        ("CO", "Compleate")
    )

    id = models.AutoField(primary_key=True)
    author = models.ForeignKey('User')
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    editedby = models.ForeignKey('User')
    template = models.ForeignKey('FromTemplateData')
    status = models.CharField(max_length=2, choices=STATUSES)
    data = postgres.fields.JSONField()  # json keyvalue pairs
    images = postgres.fields.ArrayField(base_field=models.IntegerField)

#############################################
# Round and Issue system
#############################################

class BuildingZone(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    vectors = postgres.fields.ArrayField(
                base_field=postgres.fields.ArrayField(
                    base_field=postgres.fields.ArrayField(
                        base_field=models.IntegerField
                    )
                )
            )
    parent = models.ForeignKey('BuildingZone', null=True,)
    # children = [areaid, areaid areaid, ...]
    gps = postgres.fields.ArrayField(base_field=models.IntegerField)

    def __str__(self):
        return '%s' % (self.name)

    def get_check_nodes(self):
        #return list of nodes with check flag. (for determining round data compleateness)
        pass

    def get_issue_nodes(self, resolved=false, limit=None):
        #return list of nodes without check flag that have current issues
        #include resolved issues if "resolved" is true
        #limit search to issues newer than "limit" date
        pass


class BuildingZoneNode(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    zone = models.ForeignKey('BuildingZone')
    location = postgres.fields.ArrayField(base_field=models.IntegerField)
    check = models.BooleanField()

    def __str__(self):
        return '%s' % (self.name)


class BuildingZoneLabel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    zone = models.ForeignKey('BuildingZone')
    link = models.ForeignKey('BuildingZone')
    location = postgres.fields.ArrayField(base_field=models.IntegerField)

    def __str__(self):
        return '%s' % (self.name)


class RoundArea(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    zones = models.ManyToManyField('BuildingZone') # TODO does it need to include all areas or just toplevels?

    def __str__(self):
        return '%s' % (self.name)

    def get_check_nodes(self):
        #return list of nodes with check flag. (for determining round data compleateness)
        pass

    def get_issue_nodes(self, resolved=false, limit=None):
        #return list of nodes without check flag that have current issues
        #include resolved issues if "resolved" is true
        #limit search to issues newer than "limit" date
        pass


class Issue(models.Model):

    OPEN = "OP"
    CLOSED = "CL"
    INVALID = "IN"
    NO_FIX = "NO"

    STATUSES = (
        ("OP", "Open"),
        ("CL", "Closed"),
        ("IN", "Invalid"),
        ("NO", "No Fix")
    )

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    author = models.ForeignKey('User')
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    editedby = models.ForeignKey('User')
    content = models.TextField(max_length=1000)
    node = models.ForeignKey('RoundAreaNode')
    status = models.CharField(max_length=2, choices=STATUSES)
    # comments = postgres.fields.ArrayField(base_field=models.IntegerField) # Access through back related set
    images = postgres.fields.ArrayField(base_field=models.IntegerField)

    def __str__(self):
        return '%s' % (self.name)


class IssueComment(models.Model):
    id = models.AutoField(primary_key=True)
    issue = models.ForeignKey('Issue')
    author = models.ForeignKey('User')
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    editedby = models.ForeignKey('User')
    content = models.TextField(max_length=1000)
    # comments = postgres.fields.ArrayField(base_field=models.IntegerField) # Access through back related set
    access = models.ManyToManyField("User")
    access_level = models.CharField(max_length=2, choices=User.ACCESS_LEVELS, default=User.RA)
    images = postgres.fields.ArrayField(base_field=models.IntegerField)


class RoundData(models.Model):

    INCOMPLEATE = "IN"
    COMPLEATE = "CO"

    STATUSES = (
        ("IN", "Incompleate"),
        ("CO", "Compleate")
    )

    id = models.AutoField(primary_key=True)
    author = models.ForeignKey('User')
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    editedby = models.ForeignKey('User')
    area = models.ForeignKey('RoundArea')
    status = models.CharField(max_length=2, choices=STATUSES)
    data = postgres.fields.JSONField()  # json keyvalue pairs
    images = postgres.fields.ArrayField(base_field=models.IntegerField)


#############################################
# Store image path
#############################################

class Image:
    id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=400)


#############################################
# LogAction
#############################################
class LogAction(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User')
    action = models.CharField(max_length=100)  # quick action summery, 2-4 words
    timestamp = models.DateTimeField(auto_now_add=True)
    detail = models.TextField(max_length=1000)
    type = models.CharField(max_length=100)  # the object type affected
