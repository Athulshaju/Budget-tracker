# Generated by Django 4.2.16 on 2024-10-12 17:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Userprofile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("profession", models.CharField(choices=[], max_length=10)),
                ("savings", models.IntegerField(blank=True, null=True)),
                ("income", models.BigIntegerField(blank=True, null=True)),
                ("image", models.ImageField(blank=True, upload_to="pro_image")),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Addmoney_details",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("add_money", models.CharField(choices=[], max_length=10)),
                ("quantity", models.BigIntegerField()),
                ("date", models.DateField(default=django.utils.timezone.now)),
                (
                    "category",
                    models.CharField(choices=[], default="food", max_length=20),
                ),
                (
                    "user",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
