# Generated by Django 4.1.9 on 2023-06-18 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_app', '0003_job_hiring_alter_bookmark_userid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmark',
            name='userId',
            field=models.CharField(max_length=255),
        ),
    ]
