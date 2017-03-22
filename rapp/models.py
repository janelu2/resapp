from django.db import models
from django.utils import timezone

class RoomInspectionForm(models.Model):
    author = models.ForeignKey('RA')
    text = models.TextField()
    student = models.ForeignKey('Student', null=True, on_delete=models.SET_NULL)
    id = models.AutoField(primary_key=True)
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return '%d - %s %s Room Inspection on %s' % (self.id, self.student.first_name, self.student.last_name, self.published_date)

class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    id = models.PositiveIntegerField(primary_key=True, default=0, unique=True, help_text="Unique 900# ID for this particular student")
    status = models.ForeignKey('ResidenceHall', null=True, on_delete=models.SET_NULL)
    room_number = models.CharField(max_length=10, null=True)
    #add RA at some point

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

class RA(models.Model):
    student_info = models.ForeignKey('Student', null=True, on_delete=models.SET_NULL)
    student_email = models.CharField(max_length=100)
    emergency_contact = models.CharField(max_length=40)
    contact_relationship = models.CharField(max_length=100)
    emergency_contact_phone = models.PositiveIntegerField()
    home_addr = models.TextField(max_length=100)
    car_plate = models.CharField(max_length=20)
    car_info = models.TextField(max_length=100, help_text="Make/model/description of car")
    hall = models.ForeignKey('ResidenceHall', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return '%s %s: %s' % (self.student_info.first_name, self.student_info.last_name, self.hall)

class ResidenceHall(models.Model):
    name = models.CharField(max_length=100)
    rlc = models.ForeignKey('auth.user')
    id = models.PositiveIntegerField(primary_key=True, default=0, unique=True, help_text="Unique 900# ID for this particular student")

    def __str__(self):
        return '%s' % (self.name)