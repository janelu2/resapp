from django.contrib import admin
from .models import RoomInspectionForm, Student, RA, ResidenceHall

admin.site.register(RoomInspectionForm)
admin.site.register(Student)
admin.site.register(RA)
admin.site.register(ResidenceHall)