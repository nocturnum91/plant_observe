import django.contrib.sites.models
from django.contrib.sites.models import _simple__name_validator
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Site",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "",
                    models.CharField(
                        max_length=100,
                        verbose_name=" name",
                        validators=[_simple__name_validator],
                    ),
                ),
                ("name", models.CharField(max_length=50, verbose_name="display name")),
            ],
            options={
                "ordering": ("",),
                "db_table": "django_site",
                "verbose_name": "site",
                "verbose_name_plural": "sites",
            },
            bases=(models.Model,),
            managers=[("objects", django.contrib.sites.models.SiteManager())],
        )
    ]
