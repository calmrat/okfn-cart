#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
# Author: "Chris Ward" <cward@redhat.com>

'''
Standard 'shop discounts'. For example:
 * "buy one get one free" on ice cream
 * buy two punnets of strawberries, and get the third free
 * get 20% off a Snickers bar if you buy a Mars bar at the same time
 * other common retail offer types is easy.

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

NOTE: No unique product (id) in the cart can have more discount applied to it!
'''

import logging
logger = logging.getLogger(__name__)

from collections import Counter


def buy_1_get_y_pct_off_z(cart, product, discounted=None, pct_off=1.0):
    '''
    Buy X of a product and get some percent off of another product,
    if it's in your cart too.

    Default is to give percent off a second of the same product if
    the 'discounted' product is otherwise not defined.
    '''
    discounted = discounted if discounted else product

    ids = cart.keys()
    if product not in ids:
        # product isn't in the cart at all
        logger.warn('no {} in cart; discount is invalid if not in cart'.format(
            product))
        return None
    elif product == discounted:
        if Counter(ids)[product] == 1:
            # product is only in the cart once; invalid.
            logger.warn(
                'only 1 {} in cart; discount invalid unless 2+ in cart'.format(
                    product))
            return None
    elif discounted not in ids:
        # product and discounted aren't the same, both need to be in the cart
        # we know product is there; just check if discounted is there
        # product isn't in the cart at all
        logger.warn('no {} in cart; discount is invalid if not in cart'.format(
            product))
        return None
    else:
        # product,discounted are in the cart; continue validating the discount
        logger.info('Valid "buy 1 {} get {}% off {}" discount'.format(
            product, (pct_off * 100), discounted))

    # we know we have at least one of both and all prices are the same...
    # so we'll just take the first of the product as the template for id,price
    # same with the discounted product
    d_id, d_price = cart[discounted][0]['id'], cart[discounted][0]['price']
    discount_price = -1 * (d_price * pct_off)
    return [{'id': d_id, 'price': discount_price}]


def buy_x_get_y(cart, product, buy=1, get=1):
    '''
    Buy X Get Y Free (eg, Buy 1 get 1 free)

    Subtract the price of 1 price of product for every
    2 of product in the cart.
    '''

    min_k = float(buy + get)

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
    else:
        # product is in the cart; continue validating the discount
        logger.info('Valid "buy {} {} get {}" discount'.format(
            product, buy, get))

    # product is in the cart (buy + get) or more times
    # eg, buy 1 get 1 buy+get = 2; buy 2 get 1 == 3
    # eg, you must have buy+get items in your cart for the discount to be valid
    k = len(cart[product])
    if k < min_k:
        # we don't have enough of the products in the cart for the
        # discount to be considered valid
        logger.warn(
            'only {} of {} in cart; discount needs {} to be valid'.format(
                k, product, min_k))
        return None

    # figure out how many 'free' products this discount provides
    div = int(k / min_k)

    # use the first product,price case as canonical example
    eg_prod = cart[product][0]
    _id, discount_price = eg_prod['id'], -1 * eg_prod['price']

    return [{'id': _id, 'price': discount_price} for c in range(0, div)]
