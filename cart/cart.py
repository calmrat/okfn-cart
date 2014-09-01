#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
# Author: "Chris Ward" <cward@redhat.com>

'''
Specification
-------------

Products will be represented by simple strings like "apple" or "donut".
Prices of the different products are provided in a simple CSV file mapping
a product to a price (in some unspecified currency):

apple,0.15
ice cream,3.49
strawberries,2.00
snickers bar,0.70
...

The cart should support the following operations:
 * add some quantity of a product to the cart
 * calculate the total cost of the cart

NOTE: don't worry about handling the situation in which someone tries to add a
product to the cart for which the price hasn't been provided. Assume that's
been validated elsewhere.

The cart must also support applying certain "offers", affecting the resulting
cost. Examples of the kind of offer might be as follows:

 * "buy one get one free" on ice cream
 * buy two punnets of strawberries, and get the third free
 * get 20% off a Snickers bar if you buy a Mars bar at the same time
 * other common retail offer types is easy.
'''

from __future__ import unicode_literals, absolute_import

import logging
logger = logging.getLogger(__name__)

import csv
from itertools import groupby
import os


def load_product_csv(products_csv):
    '''
    Load csv from a string or file. CSV is "clean" and only/always
    contains 2 columns ("validated elsewhere"). CSV format is otherwise
    also expected to be default as python's csv module expects it.

    For example::

        id, price
        apple,0.15
        ice cream,3.49
        strawberries,2.00
        snickers bar,0.70

    Price column must be converted to python float type after loading.
    '''
    fnames = ['id', 'price']
    exists = os.path.exists
    as_file = isinstance(products_csv, basestring) and exists(products_csv)
    if as_file:
        # if this is a path to local file, open it
        with open(products_csv) as csv_file:
            products_csv = csv_file.readlines()

    # load the csv (as string) passed in into list of dicts
    products = list(csv.DictReader(products_csv, fieldnames=fnames))

    # convert 'price' column to float
    for i, product in enumerate(products):
        products[i]['price'] = float(product['price'])

    return products


class Cart(object):
    _contents = None
    _discounts = None

    def __init__(self):
        self._contents = []
        self._discounts = set()

    def add_products(self, products):
        '''
        Adds products, with original sale price to the cart.

        Accepts input only in the form of CSV string or file.

        Returns pointer to self :class:`Cart` object.

        :param products: string or file containing `product,price` csv to
                         add to cart

        Usage::
            >>> cart = Cart()
            >>> cart.add_products('sample_products.csv')

        '''
        products = products if isinstance(products, list) else [products]
        logger.debug(
            "Added the following products to the cart: {}".format(products))
        # products is expected to be a list; wrap it in one if not already
        self._contents.extend(products)
        logger.debug("Cart Contents: {}".format(self.contents))

    @property
    def contents(self):
        ''' Group cart contents by their id and return cart contents '''
        contents = sorted(self._contents, key=lambda x: x['id'])
        gby = groupby(contents, lambda x: x['id'])
        p_grouped = {k: list(g) for k, g in gby}
        return p_grouped

    def apply_discounts(self, discounts):
        '''
        discount is specified the same [product:price] list of dicts as
        used in cart.contents.

        Only one discount per product is permitted!
        '''
        logger.debug("Applying Discount to cart")
        if not discounts:
            return
        for discount in discounts:
            _id = discount['id']
            if _id in self._discounts:
                raise RuntimeError(
                    "Attempting to apply multiple discounts to {}!".format(
                        _id))
            self.add_products(discount)
            self._discounts.add(_id)

    def receipt(self):
        '''
        Analyse cart contents, summing products quantities, price and
        discounts and show a "receipt" that describes all transactions
        and final cost of cart contents.
        '''
        # Force cart contents to be sorted. Sorted cart is required to ensure
        # we properly groupby product id.
        # Then group all the products by their id into buckets.
        # Cart includes all discounts already, too.
        contents = self.contents
        # Then calculate the cart cost and print the transaction log 'receipt'.
        receipt = ''
        total, discounts = 0.0, 0.0
        for product, line_items in contents.iteritems():
            for line_item in sorted(line_items, key=lambda x: x['price'],
                                    reverse=True):
                _id, price = line_item['id'], line_item['price']
                if price < 0:
                    discounts += price
                else:
                    total += price
                receipt += '{:>20} {:>8,.2f}\n'.format(_id, price)
        receipt += '-' * 30
        receipt += '\nTotal {:>23}'.format(total)
        receipt += '\nDiscounts {:>19,.2f}\n'.format(discounts)
        receipt += '-' * 30
        grand_total = total + discounts
        receipt += '\nGrand Total  {:>16,.2f}'.format(grand_total)
        return receipt

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        '''
        Prepare the 'receipt' which shows all products in the cart,
        discounts and total price details
        '''
        return self.receipt()
