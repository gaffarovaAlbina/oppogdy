# Generated by Django 3.1.7 on 2022-03-21 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionsApp', '0005_auto_20220320_2302'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ['createdQuestion']},
        ),
        migrations.RenameField(
            model_name='question',
            old_name='created',
            new_name='createdQuestion',
        ),
        migrations.AddField(
            model_name='question',
            name='answer',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='createdAnswer',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='public',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='Answer',
        ),
    ]
