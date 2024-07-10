from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_alter_visit_purpose_delete_purpose'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visit',
            name='related_to',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
