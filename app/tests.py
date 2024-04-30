from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from .models import *
from django.utils.timezone import now

class SignUpViewTestCase(APITestCase):
    def test_signup_success(self):
        url = reverse('signup')
        data = {
            'email': 'test@example.com',
            'password': 'testpassword',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_signup_invalid_data(self):
        url = reverse('signup')
        data = {
            'email': '',  # Invalid email
            'password': 'testpassword',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Add more test cases for signup view as needed

class SignInViewTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email='test@example.com', password='testpassword')
    
    def test_signin_success(self):
        url = reverse('signin')
        data = {
            'email': 'test@example.com',
            'password': 'testpassword',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_signin_invalid_credentials(self):
        url = reverse('signin')
        data = {
            'email': 'test@example.com',
            'password': 'invalidpassword',  # Invalid password
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Add more test cases for signin view as needed

class AccountViewTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email='test@example.com', password='testpassword')
        self.client.force_authenticate(user=self.user)
    
    def test_create_account_success(self):
        url = reverse('account')
        data = {
            'account_no': 1234567890,
            'balance': 1000.00,
            'bank_name': 'Test Bank'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Add more test cases for account view as needed

class TransactionViewTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email='test@example.com', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.account = Account.objects.create(user=self.user, account_no=1234567890, balance=1000.00, bank_name='Test Bank')
    
    def test_create_transaction_success(self):
        url = reverse('transaction')
        data = {
            'account_no': self.account.account_no,
            'amount': 100.00,
            'timestamp': now(),
            'category': 'Test Category',
            'transaction_type': 'expense',
            'mode_of_payment': 'Cash',
            'description': 'Test Description',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Add more test cases for transaction view as needed

class AnalyticsDataViewTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email='test@example.com', password='testpassword')
        self.client.force_authenticate(user=self.user)
    
    def test_get_analytics_data(self):
        url = reverse('analytics')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Add more test cases for analytics view as needed
