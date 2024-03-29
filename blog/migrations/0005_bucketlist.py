# Generated by Django 3.2.18 on 2023-03-15 16:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0004_comment_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='BucketList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('post', models.ManyToManyField(blank=True, related_name='bucketlist_post', to='blog.Post')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
