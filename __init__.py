#This file is part of account_es_ca module for Tryton.
#The COPYRIGHT file at the top level of this repository contains
#the full copyright notices and license terms.

from .account_es_ca import *
from trytond.pool import Pool


def register():
    Pool.register(
        ChartOfAccountEs2CaStart,
        module='account_es_ca', type_='model')
    Pool.register(
        ChartOfAccountEs2Ca,
        module='account_es_ca', type_='wizard')
