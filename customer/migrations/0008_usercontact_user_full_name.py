# Generated by Django 3.2 on 2022-04-29 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0007_usercontact_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercontact',
            name='user_full_name',
            field=models.CharField(default='No name', max_length=254),
            preserve_default=False,
        ),
    ]
