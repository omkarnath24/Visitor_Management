# Generated by Django 2.1.1 on 2018-10-01 06:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Gate',
            fields=[
                ('uid', models.AutoField(primary_key=True, serialize=False)),
                ('uname', models.CharField(max_length=50)),
                ('pswrd', models.CharField(max_length=50)),
                ('contno', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('visitid', models.AutoField(primary_key=True, serialize=False)),
                ('purpose', models.CharField(max_length=100)),
                ('vehicleno', models.TextField(null=True)),
                ('checkin', models.TimeField(null=True)),
                ('checkout', models.TimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Visitee',
            fields=[
                ('visiteeid', models.AutoField(primary_key=True, serialize=False)),
                ('visiteename', models.CharField(max_length=50)),
                ('visiteecontact', models.CharField(max_length=10)),
                ('visiteeflatno', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Visitor',
            fields=[
                ('visitorid', models.AutoField(primary_key=True, serialize=False)),
                ('fullname', models.CharField(max_length=50)),
                ('dateofbirth', models.DateField()),
                ('address', models.CharField(max_length=200)),
                ('contactno', models.CharField(max_length=10)),
                ('gender', models.CharField(max_length=10)),
                ('person', models.TextField()),
                ('personid', models.TextField(null=True)),
            ],
        ),
        migrations.AddField(
            model_name='visit',
            name='visiteeid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vms.Visitee'),
        ),
        migrations.AddField(
            model_name='visit',
            name='visitorid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vms.Visitor'),
        ),
    ]
