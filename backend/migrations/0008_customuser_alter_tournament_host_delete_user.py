# Generated by Django 5.0.1 on 2024-02-09 09:40

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0007_rename_photo_url_user_photo_medium_url_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('name', models.CharField(max_length=50)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('join_date', models.DateField(auto_now_add=True)),
                ('photo_medium_url', models.URLField(blank=True, max_length=255)),
                ('photo_small_url', models.URLField(blank=True, max_length=255)),
                ('list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.userslist')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='tournament',
            name='host',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.customuser'),
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]