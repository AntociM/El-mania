# Generated by Django 3.2 on 2022-04-24 09:11

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=10, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)])),
                ('user_id', models.IntegerField()),
                ('total', models.DecimalField(decimal_places=2, max_digits=6)),
                ('created_at', models.DateTimeField()),
                ('modified_at', models.DateTimeField()),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.item')),
            ],
        ),
    ]