# Generated by Django 5.0.6 on 2024-07-21 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True)),
                ('discount', models.PositiveIntegerField(help_text='Discount in Percentage')),
                ('active', models.BooleanField(default=True)),
                ('miniAmountToUseCoupon', models.PositiveBigIntegerField(default='100')),
                ('active_date', models.DateField()),
                ('expiry_date', models.DateField()),
                ('created_date', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
