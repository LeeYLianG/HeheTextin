# Generated by Django 4.1.1 on 2023-02-20 00:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hehe', '0002_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='consume',
            name='picture',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='hehe.image', verbose_name='上传图片'),
            preserve_default=False,
        ),
    ]
