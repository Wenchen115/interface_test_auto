# Generated by Django 3.1.3 on 2021-03-01 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TestTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100, verbose_name='名称')),
                ('describe', models.TextField(default='', verbose_name='描述')),
                ('status', models.IntegerField(default=0, verbose_name='状态')),
                ('cases', models.TextField(default='', verbose_name='关联用例')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
        ),
    ]
