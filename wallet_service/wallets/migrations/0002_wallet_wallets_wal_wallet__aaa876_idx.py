# Generated by Django 5.1.3 on 2024-11-23 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallets', '0001_initial'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='wallet',
            index=models.Index(fields=['wallet_id'], name='wallets_wal_wallet__aaa876_idx'),
        ),
    ]
