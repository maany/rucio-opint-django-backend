# Generated by Django 2.1.2 on 2019-08-26 08:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=128, unique=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=512)),
                ('src_site', models.CharField(max_length=128)),
                ('dst_site', models.CharField(max_length=128)),
                ('amount', models.IntegerField(default=0, null=True)),
                ('type', models.CharField(max_length=128)),
                ('status', models.CharField(choices=[('New', 'New'), ('Ongoing', 'Ongoing'), ('Resolved', 'Resolved')], default='New', max_length=12)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='IssueCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=0, null=True)),
                ('regex', models.CharField(max_length=512)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='IssueCause',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cause', models.CharField(max_length=128, unique=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Solution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('propability', models.FloatField(blank=True, default=0)),
                ('score', models.BooleanField(default=False)),
                ('affected_site', models.CharField(choices=[('src_site', 'src_site'), ('dst_site', 'dst_site'), ('unknown', 'unknown')], default='unknown', max_length=12)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.IssueCategory')),
                ('proposed_action', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='proposed_action', to='core.Action')),
                ('real_cause', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='core.IssueCause')),
                ('solution', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='solution_action', to='core.Action')),
            ],
        ),
        migrations.AddField(
            model_name='issuecategory',
            name='cause',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='core.IssueCause'),
        ),
        migrations.AddField(
            model_name='issue',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='core.IssueCategory'),
        ),
        migrations.AlterUniqueTogether(
            name='solution',
            unique_together={('category', 'solution', 'real_cause', 'affected_site')},
        ),
        migrations.AlterUniqueTogether(
            name='issuecategory',
            unique_together={('regex', 'cause')},
        ),
        migrations.AlterUniqueTogether(
            name='issue',
            unique_together={('message', 'src_site', 'dst_site', 'type')},
        ),
    ]
