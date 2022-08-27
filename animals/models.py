from django.db import models


class OptionSex(models.TextChoices):
    FEMEA = "Femea"
    MACHO = "Macho"
    DEFAULT = "Não informado"


class Animal(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    weight = models.FloatField()
    sex = models.CharField(
        max_length=15, choices=OptionSex.choices, default=OptionSex.DEFAULT
    )

    group = models.ForeignKey(
        "groups.Group", on_delete=models.CASCADE, related_name="animals"
    )

    traits = models.ManyToManyField("traits.Trait", related_name="animals")
