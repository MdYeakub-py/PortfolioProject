# Generated by Django 4.1.6 on 2023-02-13 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yeakub', '0005_alter_post_body'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='github_link',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='project_link',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]