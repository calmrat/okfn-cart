#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
# Author: "Chris Ward" <cward@redhat.com>

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from cart import Cart, load_product_csv
