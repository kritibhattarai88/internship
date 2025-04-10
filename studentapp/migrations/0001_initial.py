# Generated by Django 5.0.7 on 2025-03-31 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='JobAnnouncement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('company', models.CharField(max_length=255)),
                ('category', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('job_type', models.CharField(choices=[('fulltime', 'Full-Time'), ('shorttime', 'Short-Time')], default='fulltime', max_length=10)),
                ('posted_at', models.DateTimeField(auto_now_add=True)),
                ('application_deadline', models.DateField()),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
    ]
