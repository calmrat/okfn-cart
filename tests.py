#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
# Author: "Chris Ward" <cward@redhat.com>

'''
Units tests for cart.py
'''

from __future__ import unicode_literals, absolute_import

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


def test_spec():
    from cart import Cart, load_product_csv
    from cart.discounts import buy_x_get_y

    products_csv = 'sample_products.csv'
    products = load_product_csv(products_csv)

    cart = Cart()

    cart.add_products(products)
    cart.add_products(products)

    discounts = buy_x_get_y(cart.contents, 'snickers bar')
    cart.apply_discounts(discounts)

    try:
        cart.apply_discounts(discounts)
    except RuntimeError:
        pass
    else:
        assert False, "shouldn't be able to apply same discount twice"

    print cart
