from django.db import migrations
from account.groups import GROUP_ADMIN, GROUP_REDTEAM, GROUP_CLIENT


def get_permissions(apps, codenames):
    permission_objects = []
    Permission = apps.get_model("auth", "Permission")
    if codenames:
        for codename in codenames:
            try:
                permission = Permission.objects.get(codename=codename)
                permission_objects.append(permission.id)
            except Permission.DoesNotExist:
                pass
    return permission_objects


def add_admin_permissions(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    group_admin, _ = Group.objects.get_or_create(name=GROUP_ADMIN)
    admin_permissions = get_permissions(
        apps=apps,
        codenames=[
            "view_organization",
            "view_organizationmember",
            "add_organizationmember",
        ],
    )
    group_admin.permissions.set(admin_permissions)


def add_redteam_permissions(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    group_redteam, _ = Group.objects.get_or_create(name=GROUP_REDTEAM)
    redteam_permissions = get_permissions(
        apps=apps,
        codenames=[
            "can_scan_organization",
            "can_enable_disable_boefje",
            "can_set_clearance_level",
        ],
    )
    group_redteam.permissions.set(redteam_permissions)


def get_or_create_client_groups(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Group.objects.get_or_create(name=GROUP_CLIENT)


class Migration(migrations.Migration):

    dependencies = [
        ("organizations", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(add_admin_permissions),
        migrations.RunPython(add_redteam_permissions),
        migrations.RunPython(get_or_create_client_groups),
    ]
