# Generated by Django 3.2.4 on 2021-09-28 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='user_email',
            new_name='email',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='user_hobby',
            new_name='hobby',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='user_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='user_phone_num',
            new_name='phone_number',
        ),
        migrations.RemoveField(
            model_name='user',
            name='user_password',
        ),
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
