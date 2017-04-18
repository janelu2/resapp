import datetime
import hashlib
import base64
from django.db import models
from django.utils import timezone
from django.contrib import postgres
import django.contrib.postgres.fields #force the module to load

class Resident(models.Model):
    id = models.PositiveIntegerField(primary_key=True, default=0, unique=True, help_text="Unique 900# ID for this particular student")
    dob = models.DateField(null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    hall = models.ForeignKey("ResidenceHall")
    room = models.ForeignKey("Room")
    email = models.EmailField(null=True, blank=True)
    # photo = "" #URL to static storage (binary blob is bad idea)
    emergency_contact = models.CharField(max_length=100)
    emergency_contact_relationship = models.CharField(max_length=100)
    emergency_contact_phone = models.CharField(max_length=100)  # TODO get PROPER phone validator
    home_addr = models.TextField(max_length=100)
    car_plate = models.CharField(max_length=20)
    car_info = models.TextField(max_length=100, help_text="Make/model/description of car")

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)


class ResidenceHall(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    rlc = models.ForeignKey('User', null=True, on_delete=models.SET_NULL)
    #rooms = postgres.fields.ArrayField(base_field=models.CharField(max_length=10)) # access through backrelation

    def __str__(self):
        return '%s' % (self.name)


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


class User(models.Model):

    RA = "RA"
    PRO_STAFF = "PS"
    DIRECTOR = "DR"
    ACCESS_LEVLES = (
        ('RA', "RA"),
        ('PS', "Pro Staff"),
        ('DR', "Director")
    )

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=40, db_index=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    hashpass = models.CharField(max_length=256)
    access = models.CharField(max_length=2, choices=ACCESS_LEVLES, default=RA)
    resident = models.ForeignKey('Resident', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)


def now_add_hours_lambda(h):
    return lambda: timezone.now + datetime.timedelta(hours=h)


class AuthToken(models.Model):
    token = models.CharField(primary_key=True, max_length=64, unique=True, db_index=True)
    user = models.ForeignKey('User')
    issued = models.DateTimeField(auto_now_add=True)
    expires = models.DateTimeField(default=now_add_hours_lambda(4))
    valid = models.BooleanField(default=False)

    def generate(username, issued):
        mac = hashlib.sha256(username + issued) # TODO proget combine for hash
        token = hashlib.sha256(config.secret_key + mac) # TODO proper get key
        digest = base64.b64encode(token.digest())
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
    access_level = models.CharField(max_length=2, choices=User.ACCESS_LEVLES, default=User.RA)


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
    access_level = models.CharField(max_length=2, choices=User.ACCESS_LEVLES, default=User.RA)
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


class Image:
    id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=400)


class LogAction(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User')
    action = models.CharField(max_length=100)  # quick action summery, 2-4 words
    timestamp = models.DateTimeField(auto_now_add=True)
    detail = models.TextField(max_length=1000)
    type = models.CharField(max_length=100)  # the object type affected

