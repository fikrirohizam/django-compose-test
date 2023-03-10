from django.forms import DateInput
from .models import Home, Human, Breed, Cat
from rest_framework import serializers

class HomeSerializer(serializers.HyperlinkedModelSerializer):
    highlight = serializers.HyperlinkedIdentityField(view_name='home-highlight', format='html')

    class Meta:
        model = Home
        fields = ('id','url','highlight','home_name', 'home_address', 'house_type')


# Multiple home serializers used to learn more about 
# different types of serializers.
class HomeSerializer2(serializers.ModelSerializer):

    class Meta:
        model = Home
        fields = ('home_name', 'home_address', 'house_type')

class HumanSerializer(serializers.HyperlinkedModelSerializer):    

    class Meta:
        model = Human
        fields = ('url','id','human_name','human_gender', 'human_date_of_birth','human_description', 'human_home', 'owned_cats')
        widgets = {
            'human_date_of_birth': DateInput(attrs={'type':'date'})
        }

# Multiple human serializers used to learn more about 
# different types of serializers.        
class HumanSerializer2(serializers.ModelSerializer):    

    class Meta:
        model = Human
        fields = ('human_name','human_gender', 'human_date_of_birth','human_description', 'human_home')
        widgets = {
            'human_date_of_birth': DateInput(attrs={'type':'date'})
        }

class CatSerializer(serializers.ModelSerializer):
    cat_home = serializers.CharField(read_only=True,source='cat_owner.human_home')

    
    class Meta:
        model = Cat
        fields = ('id','cat_name','cat_gender', 'cat_date_of_birth','cat_description', 'cat_breed', 'cat_owner','cat_home')
        widgets = {
            'cat_date_of_birth': DateInput(attrs={'type':'date'}),
        }

# Multiple cat serializers used to learn more about 
# different types of serializers.
class CatSerializer2(serializers.ModelSerializer):
    
    class Meta:
        model = Cat
        fields = ('cat_name','cat_gender', 'cat_date_of_birth','cat_description', 'cat_breed')
        widgets = {
            'cat_date_of_birth': DateInput(attrs={'type':'date'}),
        }

# Serializer to get all homes from cat and human 
# to be used by breed serializer
class CatHomeSerializer(serializers.Serializer):
    home = serializers.SerializerMethodField()

    def get_home(self, book):
        homedata = Home.objects.filter(home_name=book.cat_owner.human_home).values()
        return homedata

class BreedSerializer(serializers.HyperlinkedModelSerializer):
    cats = serializers.StringRelatedField(read_only=True, many=True)
    homes = CatHomeSerializer(many=True,read_only=True, source='cats')

    class Meta:
        model = Breed
        fields = ('url','id','breed_name','breed_origin', 'breed_description', 'cats', 'homes',)

# Multiple breed serializers used to learn more about 
# different types of serializers.
class BreedSerializer2(serializers.ModelSerializer):

    class Meta:
        model = Breed
        fields = ('breed_name','breed_origin', 'breed_description')

class UserSigninSerializer(serializers.Serializer):
    username = serializers.CharField(required = True)
    password = serializers.CharField(required = True)

