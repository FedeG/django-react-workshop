# Generated by Django 2.0.5 on 2020-03-29 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0004_auto_20200329_0653'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='status',
            field=models.CharField(choices=[('ON', 'Online'), ('OFF', 'Offline'), ('ERR', 'Error'), ('NEW', 'Check')], default='NEW', max_length=3),
        ),
    ]