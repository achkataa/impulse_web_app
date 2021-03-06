# Generated by Django 4.0.3 on 2022-03-26 14:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0002_userdocument_alter_projectuser_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('document', models.FileField(upload_to='user_files/')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='UserDocument',
        ),
    ]
