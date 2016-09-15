import logging
from typing import Sequence, Dict


class LogstashFormatter(logging.Formatter):
    """
    Logging formatter for creating log entries in a Logstash native format.
    Example:
        {
            "msg" => ""GET / HTTP/1.1" 404 2327",
            "status_code" => "404",
            "message" => ""GET / HTTP/1.1" 404 2327",
            "server_time" => "14/Sep/2016 11:13:00",
            "asctime" => "2016-09-14 11:13:00,667"
        }
    """
    RESERVED_ATTRS = (
        'args', 'asctime', 'created', 'exc_info', 'exc_text', 'filename',
        'funcName', 'levelname', 'levelno', 'lineno', 'module',
        'msecs', 'message', 'msg', 'name', 'pathname', 'process',
        'processName', 'relativeCreated', 'stack_info', 'thread', 'threadName')

    DEFAULT_FIELDS = ('asctime', 'levelname', 'filename', 'funcName', 'msg', 'exc_info',)
    main_fmt = '{{\n{}\n}}'
    item_fmt = '"{}" => "{}"'

    def __init__(self, fmt: Sequence = None, datefmt=None, rename: dict = None, version: str = None, *args, **kwargs):
        super().__init__(fmt, datefmt, *args, **kwargs)

        if fmt:
            self.fields = [f for f in fmt if f in self.RESERVED_ATTRS]
        else:
            self.fields = self.DEFAULT_FIELDS

        self.datefmt = datefmt

        self.rename_map = rename or {}

        self.version = version

    def to_logstash(self, obj: Dict):
        return self.main_fmt.format(',\n'.join([self.item_fmt.format(k, v) for k, v in obj.items()]))

    def format(self, record):
        _msg = record.msg

        record.asctime = self.formatTime(record, self.datefmt)

        if isinstance(_msg, dict):
            msg_dict = _msg
        else:
            msg_dict = {'message': record.getMessage()}

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
            if v in fields_dict.keys():
                fields_dict[k] = fields_dict.pop(v)

        # Adding logging schema version if exists
        if self.version:
            fields_dict['@version'] = self.version

        return self.to_logstash(fields_dict)
