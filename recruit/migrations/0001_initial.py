# Generated by Django 2.2.4 on 2019-09-01 08:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RecruitPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=254, verbose_name='标题')),
                ('content', models.TextField(max_length=4000, verbose_name='帖子内容')),
                ('time_lab', models.DateTimeField(auto_now_add=True)),
                ('like_count', models.BigIntegerField(default=0, verbose_name='点赞数')),
                ('detail_url', models.CharField(blank=True, max_length=254, null=True, verbose_name='公司链接')),
                ('description', models.TextField(default='', max_length=2000, verbose_name='职位描述')),
                ('salary_low', models.CharField(blank=True, default='', max_length=300, null=True, verbose_name='最低薪水')),
                ('salary_high', models.CharField(blank=True, default='', max_length=300, null=True, verbose_name='最高薪水')),
                ('edu_require', models.TextField(blank=True, default='', max_length=2000, null=True, verbose_name='学历要求')),
                ('exp_require', models.TextField(blank=True, default='', max_length=2000, null=True, verbose_name='经历要求')),
                ('place', models.CharField(default='', max_length=300, verbose_name='地点')),
                ('want_num', models.CharField(default='', max_length=300, verbose_name='招聘人数')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='myrecruitpost', to=settings.AUTH_USER_MODEL, verbose_name='创建人')),
            ],
            options={
                'verbose_name': '招聘帖子',
                'verbose_name_plural': '招聘帖子',
            },
        ),
    ]
