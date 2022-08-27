from django.test import TestCase
from animals.models import Animal, OptionSex
from groups.models import Group
from traits.models import Trait


class AnimalTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.name = "name"
        cls.age = 1
        cls .weight = 1.5
        cls.sex = "Femea"
        cls.group = {"name": "group", "scientific_name": "scientific_name"}
        cls.traits = [{"name": "traits"}]

        group = {"name": "group", "scientific_name": "scientific_name"}

        cls.group_test = Group.objects.create(**group)

        cls.animal_test = Animal.objects.create(
            name = cls.name,
            age = cls.age,
            weight = cls.weight,
            sex = cls.sex,
            group = cls.group_test,
        )

        cls.animal_test_default_choice = Animal.objects.create(
            name = cls.name,
            age = cls.age,
            weight = cls.weight,
            group = cls.group_test,
        )

        traits = [{"name": "traits"}]
        for trait in traits:
            cls.traits_test = Trait.objects.create(**trait)
            cls.animal_test.traits.add(cls.traits_test)

    def test_animal_fields_and_relationships(self):
        self.assertEqual(self.animal_test.name, self.name)
        self.assertEqual(self.animal_test.age, self.age)
        self.assertEqual(self.animal_test.weight, self.weight)
        self.assertEqual(self.animal_test.sex, self.sex)
        self.assertEqual(self.animal_test.group, self.group_test)
        self.assertEqual(self.animal_test.traits.all()[0], self.traits_test)

    def test_max_length_name_animal(self):
        expected_max_length = 50
        result_max_length = self.animal_test._meta.get_field("name").max_length
        msg = "Vefique o max_length de 'name'"

        self.assertEqual(result_max_length, expected_max_length, msg)

    def test_max_length_sex_animal(self):
        expected_max_length = 15
        result_max_length = self.animal_test._meta.get_field("sex").max_length
        msg = "Verifique o max_length de 'sex'"

        self.assertEqual(result_max_length, expected_max_length, msg)

    def test_choices_sex_animal(self):
        expected_choices = OptionSex.choices
        result_choices = self.animal_test._meta.get_field("sex").choices
        msg = "Verifique as opções de 'sex'"

        self.assertEqual(result_choices, expected_choices, msg)

    def test_default_choices_sex_animal(self):
        expected_choices = OptionSex.choices
        result_choices = self.animal_test_default_choice._meta.get_field("sex").choices
        msg = "Default_choices de 'sex'"

        self.assertEqual(result_choices, expected_choices, msg)

    def test_max_length_name_group(self):
        expected_max_length = 20
        result_max_length = self.animal_test.group._meta.get_field("name").max_length
        msg = "Verifique o max_length de name do group"

        self.assertEqual(result_max_length, expected_max_length, msg)

    def test_max_length_scientific_name_group(self):
        expected_max_length = 50
        result_max_length = self.animal_test.group._meta.get_field("scientific_name").max_length
        msg = "Verifique o max_length de scientific_name do group"

        self.assertEqual(result_max_length, expected_max_length, msg)

    def test_unique_name_group(self):
        expected_unique = True

        result_unique = self.animal_test.group._meta.get_field("name").unique
        msg = "Name group unique"

        self.assertEqual(result_unique, expected_unique, msg)

    def test_unique_scientific_name_group(self):
        expected_unique = True

        result_unique = self.animal_test.group._meta.get_field("scientific_name").unique
        msg = "scientific_name group unique"

        self.assertEqual(result_unique, expected_unique, msg)

    def test_max_length_name_trait(self):
        expected_max_length = 20

        result_max_length = self.animal_test.traits.all()[0]._meta.get_field("name").max_length
        msg = "Verifique o max_length de name de trait"

        self.assertEqual(result_max_length, expected_max_length, msg)

    def test_unique_name_trait(self):
        expected_unique = True

        result_unique = self.animal_test.traits.all()[0]._meta.get_field("name").unique
        msg = "Name trait unique"

        self.assertEqual(result_unique, expected_unique, msg)


