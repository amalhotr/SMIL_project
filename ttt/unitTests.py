#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 antoni <antoni@antoni>
#
# Distributed under terms of the MIT license.

from StockData import *
import unittest

class TestStockDataClass(unittest.TestCase):
    '''
    Test harness for StockData class
    '''
    
        
    def test_basic_stock_query(self):
        '''  make sure method works with a real symbol MSFT
        x and y should be not None '''
        x,y = StockData.getValues('MSFT')
        self.assertTrue(x is not None)
        self.assertTrue(y is not None)

    def test_negative_stock_query(self):
        ''' test behavior when symbol does not exist '''
        x,y = StockData.getValues('not_a_stock')
        self.assertTrue(x is None)
        self.assertTrue(y is  None)
        
    def test_basic_crypto_query(self):
        '''  make sure method works with a real symbol BTC
        x and y should be not None '''
        x,y = StockData.getValues('BTC', currency='crypto')
        self.assertTrue(x is not None)
        self.assertTrue(y is not None)

    def test_negative_crypto_query(self):
        ''' test behavior when symbol does not exist '''
        x,y = StockData.getValues('not_a_stock', currency='crypto')
        self.assertTrue(x is None)
        self.assertTrue(y is  None)

    def test_get_current_price_stock(self):
        ''' test getCurrentPrice static method '''
        x,y = StockData.getCurrentPrice('MSFT') 
        self.assertTrue(x is not None)
        self.assertTrue(y is not None)

    def test_negative_get_current_price_stock(self):
        ''' test getCurrentPrice static method '''
        x,y = StockData.getCurrentPrice('not_a_stock') 
        self.assertTrue(x is None)
        self.assertTrue(y is None)
        
    def test_get_current_price_crypto(self):
        ''' test getCurrentPrice static method '''
        x,y = StockData.getCurrentPrice('BTC', currency='crypto') 
        self.assertTrue(x is not None)
        self.assertTrue(y is not None)

    def test_negative_get_current_price_crypto(self):
        ''' test getCurrentPrice static method '''
        x,y = StockData.getCurrentPrice('not_a_stock', currency='crypto') 
        self.assertTrue(x is None)
        self.assertTrue(y is None)
        

if __name__ == '__main__':
    unittest.main()
        
