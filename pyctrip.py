#!/usr/bin/env python
# coding: utf-8

__author__ = 'zhangxiaoyang (zhangxiaoyang.hit@gmail.com)'
__version__ = '0.0.1'

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import logging
import urllib2
import time
import md5
import gzip
from xml.sax.saxutils import escape
from xml.sax.saxutils import unescape
import xmltodict

class CtripError(StandardError):
    def __init__(self, error):
        self._error = error
        StandardError.__init__(self, self._error)

    def __str__(self):
        return 'CtripError: %s' % str(self._error)


class CtripClient(object):
    def __init__(self, aid, sid, key, domain='http://openapi.ctrip.com'):
        self._aid = str(aid)
        self._sid = str(sid)
        self._key = str(key)
        self._domain = str(domain)

    def __getattr__(self, attr):
        if attr.startswith('_'):
            return getattr(self.get, attr)
        return _Callable(self, attr)

    def _gen_signature(self, timestamp, api):
        key_md5 = md5.new(self._key).hexdigest().upper()
        return md5.new(str(timestamp) + self._aid + key_md5 + self._sid + api).hexdigest().upper()


class _HttpMan(object):
    _ENVELOPE_XML = '''<?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
        <soap:Body>
            <Request xmlns="http://ctrip.com/">
            <requestXML>%s</requestXML>
            </Request>
        </soap:Body>
    </soap:Envelope>'''

    def __init__(self, client, path, request):
        self._client = client
        self._path = path
        self._request = request
    
    def send(self):
        url = '/'.join([self._client._domain, self._path]) + '.asmx' 
        package = self._pack()
        envelope = self._send(url, package)
        return unescape(xmltodict.parse(envelope)['soap:Envelope']['soap:Body']['RequestResponse']['RequestResult'])

    def _pack(self):
        timestamp = int(time.time())
        api = self._path.split('/')[-1]
        data = '''
        <Request>
            <Header AllianceID="%s" SID="%s" TimeStamp="%d" RequestType="%s" Signature="%s" />
            %s
        </Request>''' % (
            self._client._aid,
            self._client._sid,
            timestamp,
            api,
            self._client._gen_signature(timestamp, api),
            self._request
        )
        package = self._ENVELOPE_XML % escape(data)
        return package

    def _send(self, url, package):
        req = urllib2.Request(url, package)
        req.add_header('Accept-Encoding', 'gzip, deflate')
        req.add_header('Content-Type', 'text/xml; charset=UTF-8;')
        try:
            res = urllib2.urlopen(req, timeout=5)
            body = self._read_body(res)
        except urllib2.HTTPError, e:
            raise CtripError('HTTPError')
        except Exception, e:
            raise CtripError('Unknown error')

        logging.info('POST %s' % (url))
        return body

    def _read_body(self, obj):
        using_gzip = obj.headers.get('Content-Encoding', '') == 'gzip'
        body = obj.read()
        if using_gzip:
            gzipper = gzip.GzipFile(fileobj=StringIO(body))
            fcontent = gzipper.read()
            gzipper.close()
            return fcontent
        return body


class _Callable(object):
    def __init__(self, client, name):
        self._client = client
        self._name = name

    def __getattr__(self, attr):
        if attr == 'getXML':
            return _Executable(self._client, self._name, 'XML')
        if attr == 'getJSON':
            return _Executable(self._client, self._name, 'JSON')
        return _Callable(self._client, '%s/%s' %(self._name, attr))


class _Executable(object):
    def __init__(self, client, path, fmt):
        self._client = client
        self._path = path
        self._fmt = fmt

    def __call__(self, request=''):
        xml = _HttpMan(self._client, self._path, request).send()
        if self._fmt == 'JSON':
            return xmltodict.parse(xml)
        return xml


if __name__ == '__main__':
    #logging.basicConfig(filename='ctrip.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    aid = 'xxxx'
    sid = 'xxxx'
    key = 'xxxx'

    c = CtripClient(aid, sid, key)
    o = c.Hotel.OTA_Ping.getJSON('''
        <HotelRequest>
            <RequestBody xmlns:ns="http://www.opentravel.org/OTA/2003/05" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
                <ns:OTA_PingRQ>
                    <ns:EchoData>阿什顿</ns:EchoData>
                </ns:OTA_PingRQ>
            </RequestBody>
        </HotelRequest>
    ''')

    import json
    print json.dumps(o, indent=4)
