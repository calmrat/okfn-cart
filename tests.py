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
    from cart.discounts import buy_x_get_y, buy_1_get_y_pct_off_z

    products_csv = 'sample_products.csv'
    products = load_product_csv(products_csv)

    cart = Cart()

    # add the same contents several times to fill up the cart with
    # enough product to verify all spec'd discounts.
    cart.add_products(products)
    cart.add_products(products)
    cart.add_products(products)

    # should be 15 items in the cart at this point
    assert len(cart._contents) == 15

    # discounts that should work according to spec
    # * "buy one get one free" on ice cream
    discounts = buy_x_get_y(cart.contents, 'snickers bar', buy=1, get=1)

    # buy 1 snickers bar 0.70 and get one free at -0.70
    assert round(discounts[0]['price'], 2) == -0.70

    cart.apply_discounts(discounts)

    # should be 16 items in the cart (+1 discount)
    assert len(cart._contents) == 16

    # shouldn't be possible to apply the same discount twice
    assert 'snickers bar' in cart._discounts
    try:
        cart.apply_discounts(discounts)
    except RuntimeError:
        pass
    else:
        assert False, "shouldn't be able to apply same discount twice"

    # should still be 16 items in the cart (+1 discount)
    assert len(cart._contents) == 16

    # * buy two punnets of strawberries, and get the third free
    discounts = buy_x_get_y(cart.contents, 'strawberries', buy=2, get=1)

    # buy 2 straberries at 2.00 each and get 2.00 off
    assert round(discounts[0]['price'], 2) == -2.00

    cart.apply_discounts(discounts)
    assert 'strawberries' in cart._discounts

    # should be 17 items in the cart (+2 discounts)
    assert len(cart._contents) == 17

    # * get 20% off a Snickers bar if you buy a Mars bar at the same time
    discounts = buy_1_get_y_pct_off_z(
        cart.contents, 'mars bar', discounted='snickers bar', pct_off=0.2)
    try:
        # should fail since we've already applied discount to 'snickers bar' in
        # cart
        cart.apply_discounts(discounts)
    except RuntimeError:
        pass
    else:
        assert False, ("shouldn't be able to apply multiple discounts "
                       "to same product type!")

    # should still be 17 items in the cart (+2 discounts)
    assert len(cart._contents) == 17

    # we shouldn't have a receipt yet
    assert cart._receipt == []
    # we shouldn't have 'checkedout' yet
    assert cart._checkout is False

    receipt = cart.checkout()
    # now we should have a receipt
    assert cart._receipt is not None
    # now we should have 'checkedout'
    assert cart._checkout is True

    # cart will hold onto the receipt and return a copy
    assert cart.receipt == receipt

    # round due to floating point resolution issues (eg, might be 18.880000002)
    assert receipt[-1]['id'] == 'grand_total'
    assert round(receipt[-1]['price'], 2) == 19.02
    # discounts...
    assert receipt[-2]['id'] == 'discounts'
    assert round(receipt[-2]['price'], 2) == -2.7
    # total
    assert receipt[-3]['id'] == 'total'
    assert round(receipt[-3]['price'], 2) == 21.72

    try:
        cart.checkout()
    except RuntimeError:
        pass
    else:
        assert False, "shouldn't be able to checkout more than once!"

    print str(cart)


def test_buy_1_get_y_pct_off_z():
    from cart import Cart, load_product_csv
    from cart.discounts import buy_1_get_y_pct_off_z

    products_csv = 'sample_products.csv'
    products = load_product_csv(products_csv)

    cart = Cart()

    # add the same contents several times to fill up the cart with
    # enough product to verify all spec'd discounts.
    cart.add_products(products)
    # * get 20% off a Snickers bar if you buy a Mars bar at the same time
    discounts = buy_1_get_y_pct_off_z(cart.contents, 'mars bar',
                                      discounted='snickers bar', pct_off=0.2)
    # 20% of .70 (snickers bar) is discount of -0.14
    assert round(discounts[0]['price'], 2) == -0.14

    cart.apply_discounts(discounts)

    # should still be 17 items in the cart (+2 discounts)
    assert len(cart._contents) == 6

    receipt = cart.checkout()

    # round due to floating point resolution issues (eg, might be 18.880000002)
    assert receipt[-1]['id'] == 'grand_total'
    assert round(receipt[-1]['price'], 2) == 7.1
    # discounts...
    assert receipt[-2]['id'] == 'discounts'
    assert round(receipt[-2]['price'], 2) == -0.14
    # total
    assert receipt[-3]['id'] == 'total'
    assert round(receipt[-3]['price'], 2) == 7.24

    print str(cart)
