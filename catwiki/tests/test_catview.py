import datetime
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from ..models import Cat, Breed, Human, Home
from ..serializers import CatSerializer2
from ..factories import CatFactory, HomeFactory
import logging
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework.renderers import JSONRenderer

logger = logging.getLogger(__name__)

client = APIClient()


class CatViewSetTests(APITestCase):

    def setUp(self):
       
       HomeFactory.create_batch(1)

       self.breed = Breed.objects.create(
        breed_name = "newbreed",
        breed_origin = "somewhere",
        breed_description = "breeddesc" ,
        )
       
       self.human = Human.objects.create(
        human_name = "newhuman",
        human_gender = "F",
        human_date_of_birth = '2000-01-01' ,
        human_description = "humandesc" ,
        human_home =  Home.objects.all()[0],        
        )
       
    def authenticate(self):
        self.user = User.objects.create_user(username='testuser', password='123')
        self.client.force_authenticate(self.user)

    def test_get_all_cat(self):
        """
        Insert 10 cats and then test whether there are exactly
        10 cats in database
        """
        CatFactory.create_batch(10)

        url = 'http://127.0.0.1:8000%s'%reverse('cat-list')
        # get API response
        response = self.client.get(url, format='json')

        # get data from db
        experiments = Cat.objects.all()
        serializer = CatSerializer2(experiments, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], len(serializer.data))

        logger.debug('Test cat get completed successfully')

    def test_create_cat(self):
        """
        Create 1 cat with detailed values and 
        then test whether there is 1 cat in database
        and whether all the values are correct
        """
        self.authenticate()

        logger.debug('Starting test create cat')
        url = 'http://127.0.0.1:8000%s'%reverse('cat-list')
        data = {
            'cat_name'          : 'meower',
            'cat_gender'        : 'M',
            'cat_date_of_birth' : '2000-02-05',
            'cat_description'   : 'somewhat shy. White coat',
            'cat_breed'         : self.breed.pk,
            'cat_owner'         : self.human.pk,
        }


        logger.debug('Sending TEST data to url: %s, data: %s'%(url, data))
        response = self.client.post(url, data, format='json')

        logger.debug('Testing status code response: %s, code: %d'%(response.json(), response.status_code))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        logger.debug('Testing cat count to make sure object was successfully added')
        self.assertEqual(Cat.objects.count(), 1)

        logger.debug('Testing new cat object details')
        p = Cat.objects.get()
        self.assertEqual(p.cat_name, 'meower')
        self.assertEqual(p.cat_gender, 'M')
        self.assertEqual(p.cat_date_of_birth, datetime.date(2000,2,5))
        self.assertEqual(p.cat_description, 'somewhat shy. White coat')
        self.assertEqual(p.cat_breed.breed_name, self.breed.breed_name)
        self.assertEqual(p.cat_owner.human_name, self.human.human_name)

        logger.debug('Test cat create completed successfully')

    def test_delete_cat(self):
        """
        Test to see if deleting cat works
        """
        self.authenticate()

        logger.debug('Starting test delete cats')

        CatFactory.create_batch(10)

        url = 'http://127.0.0.1:8000%s1/'%reverse('cat-list')
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.delete(url, format='json')

        logger.debug('Testing to see if status code is correct')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_put_cat(self):
        """
        Test to see if put/edit cat works
        """
        self.authenticate()

        logger.debug('Starting test put cat')

        CatFactory.create_batch(1)

        url = 'http://127.0.0.1:8000%s1/'%reverse('cat-list')
        logger.debug('Sending TEST data to url: %s'%url)
        data = {
            'cat_name'          : 'editedname',
            'cat_gender'        : 'F',
            'cat_date_of_birth' : '1999-01-05',
            'cat_description'   : 'editeddesc',
            'cat_breed'         : self.breed.pk,
            'cat_owner'         : self.human.pk,
        }

        response = self.client.put(url, data, format='json')
        json = response.json()
        
        logger.debug('Testing to see if status code is correct')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        logger.debug('Testing modified cat object details')
        p = Cat.objects.get()
        self.assertEqual(p.cat_name, 'editedname')
        self.assertEqual(p.cat_gender, 'F')
        self.assertEqual(p.cat_date_of_birth, datetime.date(1999,1,5))
        self.assertEqual(p.cat_description, 'editeddesc')
        self.assertEqual(p.cat_breed.breed_name, self.breed.breed_name)
        self.assertEqual(p.cat_owner.human_name, self.human.human_name)
    
        logger.debug('Test cat put completed successfully')

