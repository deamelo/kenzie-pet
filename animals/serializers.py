from rest_framework import serializers
from groups.models import Group
from groups.serializers import GroupSerializer
from traits.models import Trait
from traits.serializers import TraitSerializer
from .models import Animal, OptionSex
from rest_framework.exceptions import APIException
import math


class ReadOnlyError(APIException):
    status_code = 422

class AnimalSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(
        choices=OptionSex.choices, default=OptionSex.DEFAULT
    )
    group = GroupSerializer()
    traits = TraitSerializer(many=True)

    age_in_human_years = serializers.ReadOnlyField()

    def create(self, validated_data: dict) -> Animal:
        group_data = validated_data.pop("group")
        traits_data = validated_data.pop("traits")

        group_animal, _ = Group.objects.get_or_create(**group_data)

        animal = Animal.objects.create(**validated_data, group=group_animal)

        for trait in traits_data:
            traits_animal, _ = Trait.objects.get_or_create(**trait)
            animal.traits.add(traits_animal)

        human_age = 16 * math.log(validated_data["age"]) + 31
        animal.age_in_human_years = human_age


        return animal

    def update(self, instance: Animal, validated_data: dict) -> Animal:
        instance.name = validated_data.get('name', instance.name)
        instance.age = validated_data.get('age', instance.age)
        instance.weight = validated_data.get('weight', instance.weight)

        keys = ("group", "traits", "sex")
        errors = []

        for key in keys:
            if key in validated_data:
                errors.append(f"{key}: You can not update {key} property.")

        if errors:
            raise ReadOnlyError(str(errors))

        instance.save()

        return instance
