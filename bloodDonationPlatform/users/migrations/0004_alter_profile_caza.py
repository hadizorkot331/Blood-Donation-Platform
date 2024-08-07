# Generated by Django 5.0.6 on 2024-06-28 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_profile_caza"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="caza",
            field=models.CharField(
                choices=[
                    ("Al Chouf", "Al Chouf"),
                    ("Zahle", "Zahle"),
                    ("Tripoli", "Tripoli"),
                    ("El Minieh-Dennie", "El Minieh-Dennie"),
                    ("Zgharta", "Zgharta"),
                    ("Beirut", "Beirut"),
                    ("El Nabatieh", "El Nabatieh"),
                    ("Baabda", "Baabda"),
                    ("Saida", "Saida"),
                    ("El Koura", "El Koura"),
                    ("Jbeil", "Jbeil"),
                    ("Kesseroune", "Kesseroune"),
                    ("El Meten", "El Meten"),
                    ("Akkar", "Akkar"),
                    ("West Bekaa", "West Bekaa"),
                    ("Aley", "Aley"),
                    ("Rachaya", "Rachaya"),
                ],
                default="Beirut",
                max_length=25,
            ),
        ),
    ]
