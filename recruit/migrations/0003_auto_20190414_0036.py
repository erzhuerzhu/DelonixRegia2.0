# Generated by Django 2.1 on 2019-04-13 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruit', '0002_auto_20190414_0036'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='companylink',
        ),
        migrations.AddField(
            model_name='recruit',
            name='companylink',
            field=models.CharField(blank=True, max_length=254, null=True, verbose_name='公司链接'),
        ),
    ]
