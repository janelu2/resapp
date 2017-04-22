from django.contrib import admin
from .models import Resident, RA, ResidenceHall, RoomEntryRequestForm, ProgramPacket, SafetyInspectionViolation, FireAlarm

admin.site.register(Resident)
admin.site.register(RoomEntryRequestForm)
admin.site.register(RA)
admin.site.register(ResidenceHall)
admin.site.register(ProgramPacket)
admin.site.register(SafetyInspectionViolation)
admin.site.register(FireAlarm)