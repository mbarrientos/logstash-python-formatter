# -*- coding: utf-8 -*-
import json
import logging
from unittest import TestCase

from six import StringIO

from logstash_formatter import LogstashFormatter


class LogstashLoggingTestCase(TestCase):
    def setUp(self):
        self.stream = StringIO()
        self.logger = logging.getLogger()
        self.handler = logging.StreamHandler(self.stream)
        self.formatter = LogstashFormatter()
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)

    def test_logging_with_string(self):
        msg = 'foo_bar'

        self.logger.info(msg)

        logged = json.loads(self.stream.getvalue())

        self.assertEqual(msg, logged["msg"])
        for field in LogstashFormatter.DEFAULT_FIELDS:
            if field in LogstashFormatter.DEFAULT_MAPPING:
                field = LogstashFormatter.DEFAULT_MAPPING[field]
            self.assertIn(field, logged)

    def test_logging_with_extra_fields(self):
        msg = 'foo_bar'
        extras = {
            'foo_e': 'bar',
            'foo2_e': 'bar2'
        }

        self.logger.info(msg, extra=extras)
        logged = json.loads(self.stream.getvalue())

        self.assertEqual(msg, logged["msg"])
        for field in LogstashFormatter.DEFAULT_FIELDS:
            if field in LogstashFormatter.DEFAULT_MAPPING:
                field = LogstashFormatter.DEFAULT_MAPPING[field]
            self.assertIn(field, logged)

        for field, value in extras.items():
            self.assertEqual(logged[field], value)

    def test_logging_with_dict(self):
        msg_dict = {"foo": "bar", "foo2": "bar2"}

        self.logger.info(msg_dict)
        logged = json.loads(self.stream.getvalue())

        for k in msg_dict.keys():
            self.assertIn(k, logged)
        for k, v in msg_dict.items():
            self.assertEqual(logged[k], v)
        for field in LogstashFormatter.DEFAULT_FIELDS:
            if field in LogstashFormatter.DEFAULT_MAPPING:
                field = LogstashFormatter.DEFAULT_MAPPING[field]
            self.assertIn(field, logged)

    def test_logging_custom_fields(self):
        msg = 'foo_bar'
        self.handler.setFormatter(LogstashFormatter(['msg']))

        self.logger.info(msg)
        logged = json.loads(self.stream.getvalue())

        self.assertIn("msg", logged)
        self.assertDictEqual(logged, {"msg": "foo_bar", "@version": "1"})

    def test_logging_renaming(self):
        msg = 'foo_bar'
        self.handler.setFormatter(LogstashFormatter(rename={'asctime': 'timestamp'}))

        self.logger.info(msg)
        logged = self.stream.getvalue()

        print(logged)

        self.assertNotIn('asctime', logged)
        self.assertIn('timestamp', logged)
