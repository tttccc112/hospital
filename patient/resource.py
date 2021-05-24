from import_export import resources
from .models import *
 
class FeeResource(resources.ModelResource):
    class Meta:
        model = Fee