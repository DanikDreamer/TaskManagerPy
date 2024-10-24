# Generated by Django 5.1.1 on 2024-10-23 18:25

import task_manager.main.services.storage_backends
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0007_alter_user_phone"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="avatar_picture",
            field=models.ImageField(
                null=True,
                storage=task_manager.main.services.storage_backends.public_storage,
                upload_to="",
            ),
        ),
    ]
