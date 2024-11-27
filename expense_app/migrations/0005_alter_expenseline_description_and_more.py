# Generated by Django 4.2.16 on 2024-11-26 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expense_app', '0004_alter_contributor_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expenseline',
            name='description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='expenseline',
            name='due_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='expensespace',
            name='description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]