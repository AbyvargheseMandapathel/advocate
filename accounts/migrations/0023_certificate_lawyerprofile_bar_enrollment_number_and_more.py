# Generated by Django 4.2.4 on 2023-09-06 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0022_student_is_approved_delete_studentuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, null=True, upload_to='certificates/')),
            ],
        ),
        migrations.AddField(
            model_name='lawyerprofile',
            name='bar_enrollment_number',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='lawyerprofile',
            name='specialization',
            field=models.CharField(choices=[('family', 'Family Lawyer'), ('criminal', 'Criminal Lawyer'), ('consumer', 'Consumer Lawyer')], max_length=20),
        ),
        migrations.AddField(
            model_name='lawyerprofile',
            name='certificates',
            field=models.ManyToManyField(blank=True, to='accounts.certificate'),
        ),
    ]
