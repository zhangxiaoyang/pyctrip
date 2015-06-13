#!/usr/bin/env python
# coding: utf-8

from pyctrip import CtripClient
import json

if __name__ == '__main__':
    aid = 'xxxx'
    sid = 'xxxx'
    key = 'xxxx'

    c = CtripClient(aid, sid, key)
    # 获得XML格式的结果
    xml = c.Hotel.OTA_Ping.getXML('''
        <HotelRequest>
            <RequestBody xmlns:ns="http://www.opentravel.org/OTA/2003/05" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
                <ns:OTA_PingRQ>
                    <ns:EchoData>阿什顿</ns:EchoData>
                </ns:OTA_PingRQ>
            </RequestBody>
        </HotelRequest>
    ''')

    # 获得Dict格式的结果
    o = c.Hotel.OTA_Ping.getJSON('''
        <HotelRequest>
            <RequestBody xmlns:ns="http://www.opentravel.org/OTA/2003/05" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
                <ns:OTA_PingRQ>
                    <ns:EchoData>阿什顿</ns:EchoData>
                </ns:OTA_PingRQ>
            </RequestBody>
        </HotelRequest>
    ''')
