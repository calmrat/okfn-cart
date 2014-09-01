#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
# Author: "Chris Ward" <cward@redhat.com>

'''
Standard 'shop discounts'

All functions accept a list of product,price dicts grouped by product
and are expected to return an additional product,price dict which
acts as the discount 'product' that can be added to a cart.

The functions define the conditions which must exist in the cart
for the discount to be 'valid' and the (assumed) 'negative' discount
'price' which will be applied to the cart in the case the
discount is deemed valid.

If discount is invalid, return None

cart product:price are assumed to be consistent
and guarenteed ("validated elsewhere").

Also, product:prices are assumed to be positive (>0).
'''

import logging
logger = logging.getLogger(__name__)


def buy_x_get_y(cart, product, x=1, y=1):
    '''
    Buy One Get One Free

    subtract the price of 1 price of product for every
    2 of product in the cart.
    '''

    min_k = float(x + y)

    if product not in cart.keys():
        # product isn't in the cart at all
        logger.warn('no {} in cart; discount needs {} to be valid'.format(
            product, min_k))
        return None
    elif len(cart[product]) == 1:
        # product is only in the cart one time
        # not going to force anyone to take a discount...
        logger.warn('only 1 {} in cart; discount needs {} to be valid'.format(
            product, min_k))
        return None

    # product is in the cart (x + y) or more times
    # eg, buy 1 get 1 x+y = 2; buy 2 get 1 == 3
    # eg, you must have x+y items in your cart for the discount to be valid
    k = len(cart[product])
    if k < min_k:
        # we don't have enough of the products in the cart for the
        # discount to be considered valid
        logger.warn(
            'only {} of {} in cart; discount needs {} to be valid'.format(
                k, product, min_k))
        return None

    # figure out how many discounts to apply
    div = int(k / min_k)

    # use the first product,price case as canonical example
    eg_prod = cart[product][0]
    prod, discount_price = eg_prod['id'], -1 * eg_prod['price']

    return [{'id': prod, 'price': discount_price} for c in range(0, div)]
