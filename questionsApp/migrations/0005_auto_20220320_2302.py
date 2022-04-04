# Generated by Django 3.1.7 on 2022-03-20 23:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questionsApp', '0004_auto_20220320_1420'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='created',
        ),
        migrations.AlterField(
            model_name='comment',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='questionsApp.question'),
        ),
    ]
