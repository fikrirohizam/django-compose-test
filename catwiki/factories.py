import datetime
from factory.django import DjangoModelFactory
from . import models
from .models import Home, Cat, Human, Breed
from factory import Faker
from factory import SubFactory, Iterator, Sequence, fuzzy

class HomeFactory(DjangoModelFactory):
    class Meta:
        model = Home
    home_name = Faker('name')
    home_address = Faker('address')
    house_type = Faker(
        'random_element', elements=[x[0] for x in Home.HOME_TYPES]
    )

class CatFactory(DjangoModelFactory):
    class Meta:
        model = Cat
    cat_name = Faker('name')
    cat_gender = Faker(
        'random_element', elements=[x[0] for x in Cat.GENDER_CHOICES]
    )
    cat_date_of_birth = fuzzy.FuzzyNaiveDateTime(datetime.datetime(2008, 1, 1))
    cat_breed = Iterator(models.Breed.objects.all())
    cat_owner = Iterator(models.Human.objects.all())

class BreedFactory(DjangoModelFactory):
    class Meta:
        model = Breed
    breed_name = Sequence(lambda n: 'example breed {0}'.format(n))
    breed_origin = Faker('country')
    breed_description = '123 the description of a cat.'

class HumanFactory(DjangoModelFactory):
    class Meta:
        model = Human
    human_name = Faker('name')
    human_gender = Faker(
        'random_element', elements=[x[0] for x in Human.GENDER_CHOICES]
    )
    human_date_of_birth = fuzzy.FuzzyNaiveDateTime(datetime.datetime(2008, 1, 1))
    human_description = 'sdaw'
    human_home = Iterator(models.Home.objects.all())