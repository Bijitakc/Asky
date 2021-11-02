from django.test import TestCase

# Create your tests here.

#sample test
class URLTests(TestCase):
    def test_testsignuppage(self):
        response = self.client.get('/user/signup/')
        # assertEqual forms a test class and checks
        self.assertEqual(response.status_code, 200)

    
    def test_loginpage(self):
        response = self.client.get('/user/login/')
        self.assertEqual(response.status_code, 200)
