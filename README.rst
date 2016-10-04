logstash-python-formatter
=========================

Python logging formatter for creating log entries in a JSON **logstash-friendly** format.

Supports renaming of python default logging fields to logstash friendly names (e.g: renaming **asctime** to **@timestamp**)

LogstashFormatter can receive the following arguments:

* **fmt**, list or tuple containing the fields to include in each entry. Defaults to ["asctime", "levelname", "filename", "funcName", "msg", "exc_info"].
* **datefmt**, date format string to be passed to formatTime(). Defaults to ISO8601 time format.
* **rename**, dictionary containing mapping of { key: new_key } to be renamed. Defaults to { "asctime": "@timestamp" }.
* **version**, version as for the @version attribute used in Logstash. Defaults to "1".

=============
Sample output
=============

.. code:: python

    {
      "@timestamp": "2016-09-28T16:24:24,799",
      "@version": "1",
      "exc_info": null,
      "filename": "<ipython-input-21-de248ad5b09c>",
      "funcName": "<module>",
      "levelname": "INFO",
      "message": "This is a normal message to be logged"
    }

=====
Usage
=====
Add **LogstashFormatter** as the formatter of your handler, as usual:

.. code:: python

    self.logger = logging.getLogger()
    self.handler = logging.StreamHandler()
    self.handler.setFormatter(LogstashFormatter())
    self.logger.addHandler(self.handler)

===============
Using in Django
===============

Include logstash formatter in your settings file:

.. code:: python
    
    LOGGING = {
        'formatters': {
            'logstash': {
                '()': 'logstash_formatter.LogstashFormatter',
                'format': ("asctime", "levelname", "name", "lineno", "message",
                           "pathname", "module", "funcName", "process",),
                'datefmt': '%Y-%m-%dT%H:%M:%S',
                'rename': {
                    'asctime': '@timestamp',
                },
                'version': '1'
            },
        }
    }
