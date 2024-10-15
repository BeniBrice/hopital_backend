# Generated by Django 5.1.1 on 2024-10-15 03:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Specialty",
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
                ("name", models.CharField(max_length=100)),
                (
                    "description",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
            ],
        ),
        migrations.CreateModel(
            name="WorkTimeTable",
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
                ("date", models.DateField()),
                ("start_at", models.TimeField()),
                ("end_at", models.TimeField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Doctor",
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
                ("longitude", models.CharField(max_length=30)),
                ("latitude", models.CharField(max_length=30)),
                ("appointment_price", models.IntegerField()),
                ("address", models.CharField(max_length=100)),
                ("cabinet", models.CharField(blank=True, max_length=100, null=True)),
                ("joined_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "specialite",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="appointment.specialty",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="AppointMent",
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
                ("appointment_number", models.CharField(max_length=20, unique=True)),
                ("reason", models.CharField(max_length=100)),
                (
                    "description",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("action_time", models.DateTimeField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("AA", "Accepted"),
                            ("RE", "Refused"),
                            ("CA", "Canceled"),
                            ("WA", "Waiting"),
                        ],
                        default="WA",
                        max_length=10,
                    ),
                ),
                (
                    "patient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "doctor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="appointment.doctor",
                    ),
                ),
                (
                    "appointment_time",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="appointment.worktimetable",
                    ),
                ),
            ],
        ),
    ]