from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "courses",
            "0004_alter_enrollment_options_enrollment_completed_at_and_more",
        ),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.DeleteModel(
                    name="Enrollment",
                ),
            ],
        ),
    ]
