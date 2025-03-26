from django_tenants.middleware import TenantMainMiddleware

class CustomTenantMiddleware(TenantMainMiddleware):
    def get_tenant(self, model, hostname, request):
        # Example: Get tenant from subdomain
        tenant = super().get_tenant(model, hostname.split('.')[0], request)
        return tenant