# Generated by Django 3.2 on 2022-04-26 19:01

from django.db import migrations
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0009_auto_20220426_1535'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=model_utils.fields.StatusField(choices=[(0, 'dummy')], default='processing', max_length=100, no_check_for_status=True),
        ),
    ]
