logstash-python-formatter
=========================

Formatter for Python logging that outputs "native" logstash entries,
using logstash-JSON format.

###### Sample output:
```javascript
{
"@version" => "1"
"levelname" => "WARNING",
"status_code" => "404",
"process" => "654",
"lineno" => "152",
"message" => "Not Found: /",
"@timestamp" => "2016-09-14 13:33:39,672",
"name" => "django.request",
"funcName" => "get_response",
"request" => "<WSGIRequest: GET '/'>",
"module" => "base"
}
```

### Usage

Add `LogstashFormatter` as the formatter of your handler, as usual:
```python
self.logger = logging.getLogger()
self.handler = logging.StreamHandler()
self.handler.setFormatter(LogstashFormatter())
self.logger.addHandler(self.handler)
```

### Using in Django

Include logstash formatter in your settings file:
```python
LOGGING = {
        'version': 1,
        'formatters': {
            'logstash': {
                '()': 'core.logging.LogstashFormatter',
                'format': ("asctime", "levelname", "name", "lineno", "message", 
                           "pathname", "module", "funcName", "process",),
                'rename': {
                    '@timestamp': 'asctime',
                },
                'version': '1'
            },
            ...
        }        
...
}
```


