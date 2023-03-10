import datetime
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from ..models import Home, Human
from ..serializers import HumanSerializer2
from ..factories import HumanFactory
import logging
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)

client = APIClient()

class HumanViewSetTests(APITestCase):

    def setUp(self):

       self.home = Home.objects.create(
        home_name = "new home name",
        home_address = "new address",
        house_type = "condominium" ,
        )
        
    def authenticate(self):
        self.user = User.objects.create_user(username='testuser', password='123')
        self.client.force_authenticate(self.user)

    def test_get_all_human(self):
        """
        Insert 10 humans and then test whether there are exactly
        10 humans in database
        """
        HumanFactory.create_batch(10)

        url = 'http://127.0.0.1:8000%s'%reverse('human-list')
        # get API response
        response = self.client.get(url, format='json')

        # get data from db
        humans = Human.objects.all()
        serializer = HumanSerializer2(humans, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), len(serializer.data))

        logger.debug('Test human get completed successfully')

    def test_create_human(self):
        """
        Create 1 human with detailed values and 
        then test whether there is 1 human in database
        and whether all the values are correct
        """
        self.authenticate()

        print(self.home.pk)
        logger.debug('Starting test create human')
        url = 'http://127.0.0.1:8000%s'%reverse('human-list')
        data = {
            'human_name'             : 'newhuman',
            'human_gender'           : 'M',
            'human_date_of_birth'    : '2000-02-05',
            'human_description'      : 'dsasad',
            'human_home'             : self.home.pk
        }
        logger.debug('Sending TEST data to url: %s, data: %s'%(url, data))
        response = self.client.post(url, data, format='json')

        logger.debug('Testing status code response: %s, code: %d'%(response.json(), response.status_code))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        logger.debug('Testing human count to make sure object was successfully added')
        self.assertEqual(Human.objects.count(), 1)

        logger.debug('Testing new human object details')
        p = Human.objects.get()
        self.assertEqual(p.human_name, 'newhuman')
        self.assertEqual(p.human_gender, 'M')
        self.assertEqual(p.human_date_of_birth, datetime.date(2000,2,5))
        self.assertEqual(p.human_description, 'dsasad')
        self.assertEqual(p.human_home.home_name, self.home.home_name)

        logger.debug('Test human create completed successfully')


    def test_delete_home(self):
        """
        Test to see if deleting human works
        """
        self.authenticate()

        logger.debug('Starting test delete human')

        HumanFactory.create_batch(10)

        url = 'http://127.0.0.1:8000%s1/'%reverse('human-list')
        logger.debug('Sending TEST data to url: %s'%url)
        response = self.client.delete(url, format='json')

        logger.debug('Testing to see if status code is correct')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_put_human(self):
        """
        Test to see if put/edit human works
        """
        self.authenticate()

        logger.debug('Starting test put home')

        HumanFactory.create_batch(1)

        url = 'http://127.0.0.1:8000%s1/'%reverse('human-list')
        logger.debug('Sending TEST data to url: %s'%url)
        data = {
            'human_name'             : 'editedhuman',
            'human_gender'           : 'O',
            'human_date_of_birth'    : '2000-02-05',
            'human_description'      : 'editeddesc',
            'human_home'             : self.home.pk
        }

        response = self.client.put(url, data, format='json')
        json = response.json()
        
        logger.debug('Testing to see if status code is correct')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        logger.debug('Testing modified human object details')
        p = Human.objects.get()
        self.assertEqual(p.human_name, 'editedhuman')
        self.assertEqual(p.human_gender, 'O')
        self.assertEqual(p.human_date_of_birth, datetime.date(2000,2,5))
        self.assertEqual(p.human_description, 'editeddesc')
        self.assertEqual(p.human_home.home_name, self.home.home_name)
    
        logger.debug('Test human put completed successfully')
