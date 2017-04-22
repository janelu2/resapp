from tastypie.resources import ModelResource
from tastypie.constants import ALL

from rapp.models import Student

class StudentResource(ModelResource):
    class Meta:
        queryset = Student.objects.all()
        resource_name = 'student'
        filtering = {'title': ALL}