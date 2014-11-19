#!/usr/bin/env python
#This file is part account_es_ca module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.
import unittest
import doctest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import test_view, test_depends
from trytond.tests.test_tryton import doctest_setup, doctest_teardown


class AccountEsCaTestCase(unittest.TestCase):
    '''Test Account ES CA module'''

    def setUp(self):
        trytond.tests.test_tryton.install_module('account_es_ca')

    def test0005views(self):
        '''Test views'''
        test_view('account_es_ca')

    def test0006depends(self):
        '''Test depends'''
        test_depends()


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        AccountEsCaTestCase))
    return suite
