携程网（<http://www.ctrip.com>）Python SDK
===

介绍
---

官方只提供了C#、Java、Php的接口：<http://open.ctrip.com/help/SDK.aspx>，这里是非官方版本的Python SDK，纯Python编写，绿色无污染～

详细API列表见：<http://open.ctrip.com/Hotel/OTA_Ping.aspx>。

SDK编写方式参考了廖雪峰老师的[sinaweibopy](https://github.com/michaelliao/sinaweibopy)。

使用
---

```
from pyctrip import CtripClient

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
```

License
---

MIT
