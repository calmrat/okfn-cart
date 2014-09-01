"Online store shopping cart" excersize for okfn.org

Author: Chris Ward <cward@redhat.com>

Specification: https://gist.github.com/adamamyl/5cc6396c8029e8776a17

.. image:: https://travis-ci.org/kejbaly2/okfn-cart.png
   :target: https://travis-ci.org/kejbaly2/okfn-cart


Installation::

    virtualenv ~/virtenv-okfn-cart
    source ~/virtenv-okfn-cart/bin/activate
    # cd into the okfn-cart git repo
    # eg, `cd okfn-cart`
    python setup.py develop


Testing::

    pip install pytest
    py.test tests.py


Example Usage::
    from cart import Cart, load_product_csv
    from cart.discounts import buy_1_get_y_pct_off_z

    # load the sample products,price 'cart' from disk
    products_csv = 'sample_products.csv'
    products = load_product_csv(products_csv)

    cart = Cart()

    # add the product,price contents to fill up the cart
    cart.add_products(products)

    # manually add additional products...
    cart.add_products([{'id': 'oreos', 'price': 1.20}])

    # apply discount:
    # get 20% off a Snickers bar if you buy a Mars bar at the same time
    discounts = buy_1_get_y_pct_off_z(cart.contents, 'mars bar',
                                      discounted='snickers bar', pct_off=0.2)
    cart.apply_discounts(discounts)

    # checkout/prepare final receipt
    receipt = cart.checkout()

    print str(cart)
