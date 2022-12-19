from django.contrib import admin
from organizations.models import Organization, OrganizationMember
import tagulous.admin


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ["name", "code", "tags"]

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def get_readonly_fields(self, request, obj=None):
        # Obj is None when adding an organization and in that case we don't make
        # code read only so it is possible to specify the code when creating an
        # organization, but code must be read only after the organization
        # objecht has been created.
        if obj:
            return ["code"]
        else:
            return []


class OrganizationMemberAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


tagulous.admin.register(Organization, OrganizationAdmin)
admin.site.register(OrganizationMember, OrganizationMemberAdmin)
