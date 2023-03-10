from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from ..models import Home
from ..serializers import HomeSerializer2
from ..factories import HomeFactory,BreedFactory,HumanFactory,CatFactory
import logging
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework.renderers import JSONRenderer

logger = logging.getLogger(__name__)

client = APIClient()

class HomeViewSetTests(APITestCase):
    
    def authenticate(self):
        self.user = User.objects.create_user(username='testuser', password='123')
        self.client.force_authenticate(self.user)

    def test_get_all_home(self):
        """
        Insert 10 homes and then test whether there are exactly
        10 homes in database
        """
        HomeFactory.create_batch(10)

        url = 'http://127.0.0.1:8000%s'%reverse('home-list')
        # get API response
        response = self.client.get(url, format='json')

        # get data from db
        experiments = Home.objects.all()
        serializer = HomeSerializer2(experiments, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], len(serializer.data))

        logger.debug('Test home get completed successfully')

    def test_create_home(self):
        """
        Create 1 home with detailed values and 
        then test whether there is 1 home in database
        and whether all the values are correct
        """
        self.authenticate()

        logger.debug('Starting test create person')
        url = 'http://127.0.0.1:8000%s'%reverse('home-list')
        data = {
            'home_name'     : 'testhome',
            'home_address'  : 'test 123',
            'house_type'    : 'landed'
        }

        logger.debug('Sending TEST data to url: %s, data: %s'%(url, data))
        response = self.client.post(url, data, format='json')
   
        logger.debug('Testing status code response: %s, code: %d'%(response.json(), response.status_code))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        logger.debug('Testing person count to make sure object was successfully added')
        self.assertEqual(Home.objects.count(), 1)

        logger.debug('Testing new person object details')
        p = Home.objects.get()
        self.assertEqual(p.home_name, 'testhome')
        self.assertEqual(p.home_address, 'test 123')
        self.assertEqual(p.house_type, 'landed')

        logger.debug('Test home create completed successfully')

    def test_delete_home(self):
        """
        Test to see if deleting home works
        """
        self.authenticate()

        logger.debug('Starting test delete homes')

        HomeFactory.create_batch(10)

        url = 'http://127.0.0.1:8000%s1/'%reverse('home-list')
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.delete(url, format='json')

        logger.debug('Testing to see if status code is correct')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_put_home(self):
        """
        Test to see if put/edit home works
        """
        self.authenticate()

        logger.debug('Starting test put home')

        HomeFactory.create_batch(1)

        url = 'http://127.0.0.1:8000%s1/'%reverse('home-list')
        logger.debug('Sending TEST data to url: %s'%url)
        data = {
            'home_name' : 'edited home name',
            'home_address'  : 'edited address',
            'house_type'        : 'condominium'
        }

        response = self.client.put(url, data, format='json')
        json = response.json()
        
        logger.debug('Testing to see if status code is correct')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        logger.debug('Testing modified home object details')
        h = Home.objects.get()
        self.assertEqual(h.home_name, 'edited home name')
        self.assertEqual(h.home_address, 'edited address')
        self.assertEqual(h.house_type, 'condominium')
    
        logger.debug('Test home put completed successfully')


class HomeSerializerTests(APITestCase):

    def test_serializer_get_home(self):
        """
        Insert 10 homes through serializer and then test whether 
        there are exactly 10 homes
        """
        HomeFactory.create_batch(10)

        experiments = Home.objects.all()
        serializer = HomeSerializer2(experiments, many=True)
        self.assertEqual(len(serializer.data), 10)

    def test_serializer_create_home(self):
        """
        Insert 1 home through serializer and then test whether 
        there the details are correct
        """
        home = Home.objects.create(
            home_name = "new home name",
            home_address = "new address",
            house_type = "condominium" ,
        )

        experiments = Home.objects.all()
        serializer = HomeSerializer2(experiments, many=True)
        self.assertEqual(len(serializer.data), 1)

        h = Home.objects.get()
        self.assertEqual(h.home_name, 'new home name')
        self.assertEqual(h.home_address, 'new address')
        self.assertEqual(h.house_type, 'condominium')
