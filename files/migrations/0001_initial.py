# Generated by Django 5.0.6 on 2024-05-24 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=255)),
                ('file_size', models.BigIntegerField()),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
                ('last_download_date', models.DateTimeField(blank=True, null=True)),
                ('comment', models.TextField(blank=True, max_length=255)),
                ('file_path', models.CharField(max_length=255)),
                ('special_link', models.CharField(max_length=255)),
            ],
        ),
    ]