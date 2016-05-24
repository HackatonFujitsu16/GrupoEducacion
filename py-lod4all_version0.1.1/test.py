#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2015 FUJITSU LABORATORIES OF EUROPE

import unittest
import lod4all

TEST_APP_ID = 'xawsaykmcb'
TEST_PROXY_HOST = '10.142.57.21'
TEST_PROXY_PORT = 3128
TEST_PROXY_USER = None
TEST_PROXY_PASS = None
TEST_QUERY = """
    SELECT DISTINCT * WHERE {
        <http://dbpedia.org/resource/Tokyo> ?p ?o .
    }
    LIMIT 2
"""

from nose.tools import nottest

class TestLod4All(unittest.TestCase):

    def test_create_instance(self):
        connection = lod4all.Connection(
            TEST_APP_ID,
            TEST_PROXY_HOST,
            TEST_PROXY_PORT,
            TEST_PROXY_USER,
            TEST_PROXY_PASS
        )

        self.assertEqual(connection.app_id, TEST_APP_ID)
        self.assertEqual(connection.proxy_host, TEST_PROXY_HOST)
        self.assertEqual(connection.proxy_port, TEST_PROXY_PORT)
        self.assertEqual(connection.proxy_user, TEST_PROXY_USER)
        self.assertEqual(connection.proxy_pass, TEST_PROXY_PASS)

    @nottest
    def test_invalid_app_id(self):
        connection = lod4all.Connection(
            '',
            TEST_PROXY_HOST,
            TEST_PROXY_PORT,
            TEST_PROXY_USER,
            TEST_PROXY_PASS
        )
        response = connection.execute_sparql(TEST_QUERY)
        self.assertFalse(response.success)
        self.assertIsNone(response.data)
        self.assertEqual(response.error_code, lod4all.EAPPID)

    def test_invalid_query(self):
        connection = lod4all.Connection(
            TEST_APP_ID,
            TEST_PROXY_HOST,
            TEST_PROXY_PORT,
            TEST_PROXY_USER,
            TEST_PROXY_PASS
        )
        response = connection.execute_sparql("BLA BLA BLA")
        self.assertFalse(response.success)
        self.assertIsNone(response.data)
        self.assertEqual(response.error_code, lod4all.ESYNTX)

    def test_execute_sparql(self):
        connection = lod4all.Connection(
            TEST_APP_ID,
            TEST_PROXY_HOST,
            TEST_PROXY_PORT,
            TEST_PROXY_USER,
            TEST_PROXY_PASS
        )

        response = connection.execute_sparql(TEST_QUERY)
        self.assertTrue(response.success)
        self.assertIsNotNone(response.data)
        self.assertIsNone(response.error_code)

        self.assertEqual(response.data['head'], {
            "vars": ["p", "o"]
        })
        
        for element in response.data["results"]["bindings"]:
            self.assertIsNotNone(element["p"])
            self.assertIsNotNone(element["o"])

if __name__ == '__main__':
    unittest.main()
