# Generated by Django 5.1.4 on 2025-01-09 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cv',
            old_name='persone',
            new_name='personne',
        ),
        migrations.RenameField(
            model_name='loisir',
            old_name='name',
            new_name='loisirs',
        ),
        migrations.RemoveField(
            model_name='loisir',
            name='description',
        ),
        migrations.AddField(
            model_name='cv',
            name='photo',
            field=models.ImageField(null=True, upload_to='cvPhoto/'),
        ),
        migrations.AddField(
            model_name='experienceprofessionnelle',
            name='localite',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
