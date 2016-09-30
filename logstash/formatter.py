# -*- coding: utf-8 -*-

import json
import logging


class LogstashFormatter(logging.Formatter):
    """
    Logging formatter for creating log entries in a JSON logstash-friendly format.
    Example:
        {
            "msg": ""GET / HTTP/1.1" 404 2327",
            "status_code": "404",
            "message": ""GET / HTTP/1.1" 404 2327",
            "server_time": "14/Sep/2016 11:13:00",
            "@timestamp": "2016-09-14 11:13:00,667"
        }
    """
    RESERVED_ATTRS = (
        'args', 'asctime', 'created', 'exc_info', 'exc_text', 'filename',
        'funcName', 'levelname', 'levelno', 'lineno', 'module',
        'msecs', 'message', 'msg', 'name', 'pathname', 'process',
        'processName', 'relativeCreated', 'stack_info', 'thread', 'threadName')

    DEFAULT_FIELDS = ('asctime', 'levelname', 'filename', 'funcName', 'msg', 'exc_info',)

    DEFAULT_MAPPING = {
        'asctime': '@timestamp',
    }

    def __init__(self, fmt=None, datefmt=None, rename=None, version="1", *args, **kwargs):
        """
        Builds the formatter.
        :param fmt: list or tuple containing default fields to include in every entry
        :param datefmt: date format as a string to be passed to formatTime(). Defaults to ISO8601 format.
        :param rename: dictionary with {old_key: new_key} to be renamed in the log entries. Defaults to {'asctime':
        '@timestamp'}.
        :param version: version as for @version field in logging, always included. Defaults to "1".
        """
        super(LogstashFormatter, self).__init__(fmt, datefmt, *args, **kwargs)

        if isinstance(fmt, (list, tuple)):
            self.fields = [f for f in fmt if f in self.RESERVED_ATTRS]
        else:
            self.fields = self.DEFAULT_FIELDS

        self.datefmt = datefmt
        self.rename_map = rename or self.DEFAULT_MAPPING
        self.version = version

    def format(self, record):
        _msg = record.msg

        record.asctime = self.formatTime(record, self.datefmt)

        if isinstance(_msg, dict):
            msg_dict = _msg
        else:
            msg_dict = {}
            record.message = record.getMessage()

        extra_dict = {k: v for k, v in record.__dict__.items()
                      if k not in self.RESERVED_ATTRS and not k.startswith('_')}

        # Fields specified at "fmt"
        fields_dict = {k: v for k, v in record.__dict__.items() if k in self.fields}

        # Adding fields coming from base message
        fields_dict.update(msg_dict)

        # Adding extra fields
        fields_dict.update(extra_dict)

        # Replacing fields names if rename mapping exists
        for k, v in self.rename_map.items():
            if k in fields_dict.keys():
                fields_dict[v] = fields_dict.pop(k)

        # Adding logging schema version if exists
        if self.version:
            fields_dict['@version'] = self.version

        return json.dumps(fields_dict, default=str)
