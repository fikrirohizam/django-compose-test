from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from ..models import Breed
from ..serializers import BreedSerializer2
from ..factories import BreedFactory
import logging
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework.renderers import JSONRenderer

logger = logging.getLogger(__name__)

client = APIClient()


class BreedViewSetTests(APITestCase):
    
    def authenticate(self):
        self.user = User.objects.create_user(username='testuser', password='123')
        self.client.force_authenticate(self.user)

    def test_get_all_breed(self):
        """
        Insert 10 breeds and then test whether there are exactly
        10 breeds in database
        """
        BreedFactory.create_batch(10)

        url = 'http://127.0.0.1:8000%s'%reverse('breed-list')
        # get API response
        response = self.client.get(url, format='json')

        # get data from db
        experiments = Breed.objects.all()
        serializer = BreedSerializer2(experiments, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], len(serializer.data))

        logger.debug('Test breed get completed successfully')

    def test_create_breed(self):
        """
        Create 1 breed with detailed values and 
        then test whether there is 1 breed in database
        and whether all the values are correct
        """
        self.authenticate()

        logger.debug('Starting test create breed')
        url = 'http://127.0.0.1:8000%s'%reverse('breed-list')
        data = {
            'breed_name'     : 'Maine Coon',
            'breed_origin'  : 'Maine, United States',
            'breed_description'    : 'large, long coat'
        }

        logger.debug('Sending TEST data to url: %s, data: %s'%(url, data))
        response = self.client.post(url, data, format='json')
   
        logger.debug('Testing status code response: %s, code: %d'%(response.json(), response.status_code))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        logger.debug('Testing breed count to make sure object was successfully added')
        self.assertEqual(Breed.objects.count(), 1)

        logger.debug('Testing new breed object details')
        p = Breed.objects.get()
        self.assertEqual(p.breed_name, 'Maine Coon')
        self.assertEqual(p.breed_origin, 'Maine, United States')
        self.assertEqual(p.breed_description, 'large, long coat')

        logger.debug('Test breed create completed successfully')

    def test_delete_breed(self):
        """
        Test to see if deleting breed works
        """
        self.authenticate()

        logger.debug('Starting test delete breeds')

        BreedFactory.create_batch(10)

        url = 'http://127.0.0.1:8000%s1/'%reverse('breed-list')
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.delete(url, format='json')

        logger.debug('Testing to see if status code is correct')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_put_breed(self):
        """
        Test to see if put/edit breed works
        """
        self.authenticate()

        logger.debug('Starting test put breed')

        BreedFactory.create_batch(1)

        url = 'http://127.0.0.1:8000%s1/'%reverse('breed-list')
        logger.debug('Sending TEST data to url: %s'%url)
        data = {
            'breed_name'        : 'edited breed name',
            'breed_origin'      : 'edited origin',
            'breed_description' : 'edited description'
        }

        response = self.client.put(url, data, format='json')
        json = response.json()
        
        logger.debug('Testing to see if status code is correct')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        logger.debug('Testing modified breed object details')
        h = Breed.objects.get()
        self.assertEqual(h.breed_name, 'edited breed name')
        self.assertEqual(h.breed_origin, 'edited origin')
        self.assertEqual(h.breed_description, 'edited description')
    
        logger.debug('Test breed put completed successfully')


class BreedSerializerTests(APITestCase):

    def test_serializer_get_home(self):
        """
        Insert 10 homes through serializer and then test whether 
        there are exactly 10 homes
        """
        BreedFactory.create_batch(10)

        experiments = Breed.objects.all()
        serializer = BreedSerializer2(experiments, many=True)
        self.assertEqual(len(serializer.data), 10)

    def test_serializer_create_home(self):
        """
        Insert 1 breed through serializer and then test whether 
        there the details are correct
        """
        home = Breed.objects.create(
            breed_name = "new",
            breed_origin = "new2",
            breed_description = "new3" ,
        )

        experiments = Breed.objects.all()
        serializer = BreedSerializer2(experiments, many=True)
        self.assertEqual(len(serializer.data), 1)

        h = Breed.objects.get()
        self.assertEqual(h.breed_name, 'new')
        self.assertEqual(h.breed_origin, 'new2')
        self.assertEqual(h.breed_description, 'new3')
