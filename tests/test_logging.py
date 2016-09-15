import logging
from io import StringIO
from unittest import TestCase

from logstash import LogstashFormatter


class LogstashLoggingTestCase(TestCase):
    def setUp(self):
        self.stream = StringIO()
        self.logger = logging.getLogger()
        self.handler = logging.StreamHandler(self.stream)
        self.handler.setFormatter(LogstashFormatter())
        self.logger.addHandler(self.handler)

    def test_logging_with_string(self):
        msg = 'foo_bar'

        self.logger.info(msg)
        logged = self.stream.getvalue()

        self.assertIn('"msg" => "{}"'.format(msg), logged)
        for field in LogstashFormatter.DEFAULT_FIELDS:
            self.assertIn('"{}" =>'.format(field), logged)

    def test_logging_with_extra_fields(self):
        msg = 'foo_bar'
        extras = {
            'foo_e': 'bar',
            'foo2_e': 'bar2'
        }

        self.logger.info(msg, extra=extras)
        logged = self.stream.getvalue()

        self.assertIn('"msg" => "{}"'.format(msg), logged)
        for field in LogstashFormatter.DEFAULT_FIELDS:
            self.assertIn('"{}" =>'.format(field), logged)
        for field, value in extras.items():
            self.assertIn('"{}" => "{}"'.format(field, value), logged)

    def test_logging_with_dict(self):
        msg_dict = {"foo": "bar", "foo2": "bar2"}

        self.logger.info(msg_dict)
        logged = self.stream.getvalue()

        self.assertIn(str(msg_dict), logged)
        for k, v in msg_dict.items():
            self.assertIn('"{}" => "{}"'.format(k, v), logged)
        for field in LogstashFormatter.DEFAULT_FIELDS:
            self.assertIn('"{}" =>'.format(field), logged)

    def test_logging_custom_fields(self):
        msg = 'foo_bar'
        self.handler.setFormatter(LogstashFormatter(['msg']))

        self.logger.info(msg)
        logged = self.stream.getvalue()

        self.assertIn('"msg" =>', logged)
        self.assertEqual(logged.count('=>'), 1)

    def test_logging_renaming(self):
        msg = 'foo_bar'
        self.handler.setFormatter(LogstashFormatter(rename={'asctime': 'timestamp'}))

        self.logger.info(msg)
        logged = self.stream.getvalue()

        self.assertNotIn('asctime', logged)
        self.assertIn('timestamp', logged)


