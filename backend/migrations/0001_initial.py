# Generated by Django 5.0.1 on 2024-01-25 15:27

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UsersList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('join_date', models.DateField(auto_now_add=True)),
                ('list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.userslist')),
            ],
        ),
    ]
