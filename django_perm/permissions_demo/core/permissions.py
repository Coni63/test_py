from rest_framework.permissions import BasePermission, DjangoModelPermissions


class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to allow only owners of a document to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Allow read-only permissions for all users
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        # Write permissions are only allowed for the owner
        return obj.owner == request.user


class MyDjangoModelPermissions(DjangoModelPermissions):
    perms_map = {
        'GET':['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }

class CustomDjangoModelPermissions(DjangoModelPermissions):
    perms_map = {
        'POST': ['%(app_label)s.toggle_%(model_name)s'],
    }
 



#  Not working
class DocumentPermission(BasePermission):
    """
    Custom permission to check specific object-level permissions.
    """

    def has_permission(self, request, view):
        # Allow authenticated users to proceed to object-level checks
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Retrieve: Requires `view_document` permission
        if request.method in ['GET'] and request.user.has_perm('core.view_document', obj):
            return True

        # Update: Requires `add_document` permission
        if request.method in ['POST'] and request.user.has_perm('core.add_document', obj):
            return True

        # Update: Requires `change_document` permission
        if request.method in ['PUT', 'PATCH'] and request.user.has_perm('core.change_document', obj):
            return True

        # Delete: Requires `delete_document` permission
        if request.method == 'DELETE' and request.user.has_perm('core.delete_document', obj):
            return True

        return False