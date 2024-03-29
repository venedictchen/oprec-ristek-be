# Generated by Django 5.0.2 on 2024-03-02 10:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('food', 'Food'), ('transportation', 'Transportation'), ('living', 'Living'), ('communications', 'Communications'), ('clothes', 'Clothes'), ('health', 'Health'), ('toiletry', 'Toiletry'), ('gifts', 'Gifts'), ('entertainments', 'Entertainments'), ('other', 'Other')], max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Items',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=200)),
                ('amount', models.IntegerField()),
                ('date', models.DateField(auto_now=True)),
                ('itemType', models.CharField(choices=[('expense', 'Expense'), ('income', 'Income')], max_length=10)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='money_app.category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
