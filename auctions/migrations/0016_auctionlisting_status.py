# Generated by Django 4.1.5 on 2023-01-11 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0015_auctionlisting_winner'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlisting',
            name='status',
            field=models.CharField(default='open', max_length=64),
        ),
    ]