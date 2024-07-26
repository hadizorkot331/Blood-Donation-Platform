# Generated by Django 5.0.6 on 2024-06-28 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0006_alter_profile_caza"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="caza",
            field=models.CharField(
                choices=[
                    ("Rachaya", "Rachaya"),
                    ("Al Chouf", "Al Chouf"),
                    ("Saida", "Saida"),
                    ("El Nabatieh", "El Nabatieh"),
                    ("Baabda", "Baabda"),
                    ("Beirut", "Beirut"),
                    ("El Meten", "El Meten"),
                    ("El Koura", "El Koura"),
                    ("Zgharta", "Zgharta"),
                    ("Jbeil", "Jbeil"),
                    ("Tripoli", "Tripoli"),
                    ("Zahle", "Zahle"),
                    ("West Bekaa", "West Bekaa"),
                    ("El Minieh-Dennie", "El Minieh-Dennie"),
                    ("Kesseroune", "Kesseroune"),
                    ("Akkar", "Akkar"),
                    ("Aley", "Aley"),
                ],
                default="Beirut",
                max_length=25,
            ),
        ),
    ]
