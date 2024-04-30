# Generated by Django 5.0.2 on 2024-02-26 23:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("rides", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="ride",
            name="passengers",
            field=models.ManyToManyField(
                blank=True, related_name="rides_joined", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="ride",
            name="ride_status",
            field=models.CharField(default="Yet to Start", max_length=50),
        ),
        migrations.CreateModel(
            name="RideRequest",
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
                ("request_status", models.CharField(max_length=50)),
                ("seats_requested", models.PositiveIntegerField(default=1)),
                (
                    "requested_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ride_requests",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "ride",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="requests",
                        to="rides.ride",
                    ),
                ),
            ],
        ),
    ]