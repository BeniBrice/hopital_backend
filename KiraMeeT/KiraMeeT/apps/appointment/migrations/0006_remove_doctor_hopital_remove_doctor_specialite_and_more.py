# Generated by Django 5.1.6 on 2025-03-27 08:34

import datetime
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0005_alter_doctor_latitude_alter_doctor_longitude'),
        ('core', '0005_alter_profil_user_doctor'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor',
            name='hopital',
        ),
        migrations.RemoveField(
            model_name='doctor',
            name='specialite',
        ),
        migrations.RemoveField(
            model_name='doctor',
            name='user',
        ),
        migrations.AlterField(
            model_name='appointment',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.doctor'),
        ),
        migrations.RemoveField(
            model_name='worktimetable',
            name='doctor',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='appointment_time',
        ),
        migrations.AlterModelOptions(
            name='appointment',
            options={'verbose_name': 'Appointment', 'verbose_name_plural': 'Appointments'},
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='action_time',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='appointment_number',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='description',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='patient',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='reason',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='status',
        ),
        migrations.AddField(
            model_name='appointment',
            name='end_at',
            field=models.TimeField(default=datetime.time(8, 0)),
        ),
        migrations.AddField(
            model_name='appointment',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='patient_limit',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='appointment',
            name='start_at',
            field=models.TimeField(default=datetime.time(8, 0)),
        ),
        migrations.AlterModelTable(
            name='appointment',
            table='appointment',
        ),
        migrations.CreateModel(
            name='ApppointnmentUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appointment_reason', models.TextField()),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('refused', 'Refused')], default='pending', max_length=250)),
                ('appointment_status_info', models.TextField(blank=True, default='', null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointment_user', to='core.doctor')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointment_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Appointment_user',
                'verbose_name_plural': 'Appointment_users',
                'db_table': 'ApppointnmentUser',
            },
        ),
        migrations.DeleteModel(
            name='Hopital',
        ),
        migrations.DeleteModel(
            name='Specialty',
        ),
        migrations.DeleteModel(
            name='Doctor',
        ),
        migrations.DeleteModel(
            name='WorkTimeTable',
        ),
    ]
