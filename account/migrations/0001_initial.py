# Generated by Django 3.0.3 on 2020-02-28 05:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('phone', models.CharField(max_length=15, null=True)),
                ('email', models.CharField(max_length=50, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('price', models.FloatField(null=True)),
                ('category', models.CharField(choices=[('router', 'router'), ('access point', 'access point'), ('switch', 'switch'), ('pc', 'pc'), ('laptop', 'laptop')], max_length=100, null=True)),
                ('description', models.CharField(max_length=1000, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('tags', models.ManyToManyField(to='account.Tags')),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('status', models.CharField(choices=[('pending', 'pending'), ('on process', 'on process'), ('delivered', 'delivered')], max_length=100, null=True)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.Customers')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.Products')),
            ],
        ),
    ]
