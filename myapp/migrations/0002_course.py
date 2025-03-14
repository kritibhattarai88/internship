# Generated by Django 5.0.7 on 2025-03-05 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('duration', models.CharField(choices=[('short-term', 'Short-term'), ('long-term', 'Long-term')], max_length=20)),
                ('fee', models.DecimalField(decimal_places=2, max_digits=10)),
                ('skill_level', models.CharField(choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')], max_length=20)),
                ('prerequisites', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='courses/')),
            ],
        ),
    ]
