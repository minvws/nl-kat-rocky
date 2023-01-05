# Generated by Django 3.2.16 on 2022-12-12 23:19

from django.db import migrations, models
import django.db.models.deletion
import tagulous.models.fields
import tagulous.models.models
import tools.fields


class Migration(migrations.Migration):

    dependencies = [
        ("tools", "0026_auto_20221031_1344"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="organization",
            name="signal_group_id",
        ),
        migrations.RemoveField(
            model_name="organization",
            name="signal_username",
        ),
        migrations.AlterField(
            model_name="organization",
            name="code",
            field=tools.fields.LowerCaseSlugField(
                allow_unicode=True,
                help_text="A slug containing only lower-case unicode letters, numbers, hyphens or underscores that will be used in URLs and paths",
                max_length=32,
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name="organization",
            name="name",
            field=models.CharField(help_text="The name of the organisation", max_length=126, unique=True),
        ),
        migrations.CreateModel(
            name="Tagulous_Organization_tags",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255, unique=True)),
                ("slug", models.SlugField()),
                (
                    "count",
                    models.IntegerField(default=0, help_text="Internal counter of how many times this tag is in use"),
                ),
                (
                    "protected",
                    models.BooleanField(default=False, help_text="Will not be deleted when the count reaches 0"),
                ),
                ("path", models.TextField()),
                ("label", models.CharField(help_text="The name of the tag, without ancestors", max_length=255)),
                ("level", models.IntegerField(default=1, help_text="The level of the tag in the tree")),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="children",
                        to="tools.tagulous_organization_tags",
                    ),
                ),
            ],
            options={
                "ordering": ("name",),
                "abstract": False,
                "unique_together": {("slug", "parent")},
            },
            bases=(tagulous.models.models.BaseTagTreeModel, models.Model),
        ),
        migrations.AddField(
            model_name="organization",
            name="tags",
            field=tagulous.models.fields.TagField(
                _set_tag_meta=True,
                force_lowercase=True,
                help_text="Enter a comma-separated tag string",
                protect_all=True,
                to="tools.Tagulous_Organization_tags",
                tree=True,
                blank=True,
            ),
        ),
    ]