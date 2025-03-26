from django.db import models

# Create your models here.
from django_tenants.models import TenantMixin, DomainMixin

class Tenant(TenantMixin):
    name = models.CharField(max_length=100)
    created_on = models.DateField(auto_now_add=True)
    
    # True for schema that will be publicly available (e.g. landing page)
    is_public = models.BooleanField(default=False)

    auto_create_schema = True

class Domain(DomainMixin):
    pass