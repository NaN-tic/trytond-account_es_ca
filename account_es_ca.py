#This file is part of account_es_ca module for Tryton.
#The COPYRIGHT file at the top level of this repository contains
#the full copyright notices and license terms.
from trytond.model import ModelView
from trytond.pool import Pool
from trytond.transaction import Transaction
from trytond.wizard import Wizard, StateTransition, StateView, Button
import logging
import csv
import os

__all__ = [
    'ChartOfAccountEs2CaStart',
    'ChartOfAccountEs2Ca',
    ]


def get_csv_reader(file_name):
    try:
        reader = csv.reader(open(file_name, 'rU'), delimiter=str(','),
                            quotechar=str('"'))
    except:
        logger = logging.getLogger(__name__)
        message = 'Error reading file %s' % file_name
        logger.error(message)
        return []
    return reader


class ChartOfAccountEs2CaStart(ModelView):
    'Chart of Account Spanish to Catalan'
    __name__ = 'chart.of.account.es.ca.start'

    @staticmethod
    def default_model():
        model = Transaction().context.get('active_id')
        return model


class ChartOfAccountEs2Ca(Wizard):
    """Chart of Account Spanish to Catalan"""
    __name__ = "chart.of.account.es.ca"

    start = StateView('chart.of.account.es.ca.start',
        'account_es_ca.chart_of_account_es_ca_start_view_form', [
            Button('Cancel', 'end', 'tryton-cancel'),
            Button('Translate', 'translate', 'tryton-ok', default=True),
            ])
    translate = StateTransition()

    def transition_translate(self):
        Module = Pool().get('ir.module.module')
        modules = Module.search([
                ('name', 'in', ('account_es', 'account_es_pyme')),
                ('state', '=', 'installed'),
            ])
        if modules:
            with Transaction().set_context(language='ca_ES'):
                with Transaction().set_user(0):
                    csvmap = {
                        'account.account.template': '/account.csv',
                        'account.account.type.template': '/account_type.csv',
                        'account.tax.group': '/tax_group.csv',
                        'account.tax.template': '/tax.csv',
                        'account.tax.code.template': '/tax_code.csv',
                        'account.tax.rule.template': '/tax_rule.csv',
                    }
                    for module, archive in csvmap.iteritems():
                        Module = Pool().get(module)
                        file_name = os.path.dirname(__file__) + archive
                        reader = get_csv_reader(file_name)
                        for row in reader:
                            fields = Module.search([('name', '=', row[0])])
                            Module.write(fields, {'name': row[1]})
        else:
            Wizard = Pool().get('ir.action.wizard')
            wizard = Wizard.search([
                ('wiz_name', '=', 'chart.of.account.es.ca')
                ])[0]
            ConfigWizard = Pool().get('ir.module.module.config_wizard.item')
            config_wizard = ConfigWizard.search([('action', '=', wizard.id)])
            ConfigWizard.write(config_wizard, {'state': 'open'})
        return 'end'
