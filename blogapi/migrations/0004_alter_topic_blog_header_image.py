# Generated by Django 4.2.1 on 2023-06-26 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapi', '0003_alter_topic_blog_header_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='blog_header_image',
            field=models.ImageField(blank=True, default='https://www.hindustantimes.com/ht-img/img/2023/06/25/550x309/WhatsApp_Image_2021-09-18_at_094218_1687737467635_1687737467830.jpeg', upload_to='image/'),
        ),
    ]