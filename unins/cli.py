#!/usr/bin/env python3

import os
import sys
import argparse
from insales import InSalesApi
from unins import unleashed
from unins.unleashed import UnleashedApi
from logbook import StderrHandler
from commands.import_products import ProductImporter

# Fallback to environment variables when not specified
# See https://stackoverflow.com/a/10551190
class EnvDefault(argparse.Action):
    def __init__(self, envvar, required=True, default=None, help='', **kwargs):
        if not default and envvar:
            if envvar in os.environ:
                default = os.environ[envvar]

        if required and default:
            required = False

        ext_help = '{0}{1}(can be specified with ${2} environment variable)' \
                .format(help, ' ' if help else '', envvar)

        super(EnvDefault, self).__init__(
                default=default, required=required, help=ext_help, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)

def import_products(args):
    insales_api = InSalesApi.from_credentials(
            args.insales_account, args.insales_key, args.insales_password)

    pi = ProductImporter(insales_api, None, None)
    pi.import_all()

def import_so(args):
    unleashed_api = UnleashedApi(args.unleashed_id, args.unleashed_key)
    unleashed.create_sales_order(unleashed_api)

def main():
    parser = argparse.ArgumentParser(prog='unins')

    parser.add_argument(
        "--insales-account", action=EnvDefault, envvar='UNINS_INSALES_ACCOUNT',
        help="InSales account name, i.e., the part before .myinsales.ru")

    parser.add_argument(
        "--insales-key", action=EnvDefault, envvar='UNINS_INSALES_KEY',
        help="InSales API key")

    parser.add_argument(
        "--insales-password", action=EnvDefault, envvar='UNINS_INSALES_PASSWORD',
        help="InSales API password")

    parser.add_argument(
        "--unleashed-id", action=EnvDefault, envvar='UNINS_UNLEASHED_ID',
        help="Unleashed API ID")

    parser.add_argument(
        "--unleashed-key", action=EnvDefault, envvar='UNINS_UNLEASHED_KEY',
        help="Unleashed private key")

    subparsers = parser.add_subparsers()

    parser_import_products = subparsers.add_parser('import-products')
    parser_import_products.set_defaults(func=import_products)

    parser_import_so = subparsers.add_parser('import-so')
    parser_import_so.set_defaults(func=import_so)

    args = parser.parse_args()

    with StderrHandler():
        try:
            args.func(args)
        except KeyboardInterrupt:
            pass

if __name__ == '__main__':
    main()
