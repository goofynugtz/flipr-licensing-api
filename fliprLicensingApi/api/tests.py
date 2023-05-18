from django.test import TestCase
import os
from .views import new_rsa

class GenerateLicense():
    def setUp(self):
        print("HEllo")
        new_rsa('public.pem', 'private.pem')

    def tearDown(self):
        os.remove('public.pem')
        os.remove('private.pem')

test1 = GenerateLicense()
test1.setUp()
test1.tearDown()