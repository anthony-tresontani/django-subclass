"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django_subclass.models import RealClass, SubclassMapper
from django_subclass.site import Register
from django.db import models
from test_app.models import BaseClass, SubClassA, SubClassB, SubClassC, OtherSubClassA, OtherClass
from django_subclass import site

class TestSubclass(TestCase):

    def tearDown(self):
        Register.clean()
        SubclassMapper.objects.all().delete()
        RealClass.objects.all().delete()

    def test_register(self):
        site.register(SubClassA)
        self.assertTrue(SubClassA in site.Register._registry)
        self.assertTrue(BaseClass in site.Register._bases_registry)

    def test_manager(self):
        site.register(SubClassA)
        self.assertIsNotNone(RealClass.objects.get_for_class(SubClassA))

    def test_subclass(self):
        """
            Test the overall process and demonstrate how to use this.
        """
        # Register proxy subclasses
        site.register(SubClassA)
        site.register(SubClassB)
        
        A = SubClassA(key=1)
        A_initial_type = A.__class__.__name__
        A.save()
        
        B = SubClassB(key=2)
        B_initial_type = B.__class__.__name__
        B.save()

        C = SubClassC(key=3)
        C_initial_type = C.__class__.__name__
        C.save()

        # Registered class retrieve their original class
        self.assertEquals(BaseClass.objects.get(key=1).__class__.__name__,A_initial_type)
        self.assertEquals(BaseClass.objects.get(key=2).__class__.__name__,B_initial_type)

        # Unregistrered class do not retrieve their original class
        self.assertNotEquals(BaseClass.objects.get(key=3).__class__.__name__,C_initial_type)


    def test_multiple_class(self):
        """
            Test the subclass when multiple proxy are registered
        """
        site.register(SubClassA)
        site.register(SubClassB)
        site.register(OtherSubClassA)

        A = SubClassA(key=1)
        A_initial_type = A.__class__.__name__
        A.save()

        B = SubClassB(key=2)
        B_initial_type = B.__class__.__name__
        B.save()

        C = SubClassA(key=3)
        C_initial_type = C.__class__.__name__
        C.save()

        oA = OtherSubClassA(key=1)
        oA_initial_type = oA.__class__.__name__
        oA.save()

        # Registered class retrieve their original class
        self.assertEquals(BaseClass.objects.get(key=1).__class__.__name__,A_initial_type)
        self.assertEquals(BaseClass.objects.get(key=2).__class__.__name__,B_initial_type)
        self.assertEquals(BaseClass.objects.get(key=3).__class__.__name__,C_initial_type)
        self.assertEquals(OtherClass.objects.get(key=1).__class__.__name__,oA_initial_type)

