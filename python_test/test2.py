import datetime

stt='''	Строка 1495025: 19.02.25 10:22:39.410,https-jsse-nio-8443-exec-10,DEBUG,IDBankUnifoServiceImpl,Принят запрос на экспорт начислений (msgID:1003).
	Строка 1531291: 19.02.25 10:22:46.387,https-jsse-nio-8443-exec-10,DEBUG,WebServiceUtils,Stopping application finished ms:0
	Строка 1629462: 19.02.25 10:22:58.432,https-jsse-nio-8443-exec-10,DEBUG,IDBankUnifoServiceImpl,Принят запрос на экспорт начислений (msgID:null).
	Строка 1630596: 19.02.25 10:22:58.482,https-jsse-nio-8443-exec-10,DEBUG,WebServiceUtils,Stopping application finished ms:0
	Строка 1672112: 19.02.25 10:23:03.841,https-jsse-nio-8443-exec-10,DEBUG,IDBankUnifoServiceImpl,Принят запрос на экспорт начислений (msgID:null).
	Строка 1673028: 19.02.25 10:23:03.900,https-jsse-nio-8443-exec-10,DEBUG,WebServiceUtils,Stopping application finished ms:1
	Строка 1723654: 19.02.25 10:23:10.636,https-jsse-nio-8443-exec-10,DEBUG,IDBankUnifoServiceImpl,Принят запрос на экспорт начислений (msgID:1003).
	Строка 1726429: 19.02.25 10:23:11.085,https-jsse-nio-8443-exec-10,DEBUG,WebServiceUtils,Stopping application finished ms:1
	Строка 1735712: 19.02.25 10:23:12.607,https-jsse-nio-8443-exec-10,DEBUG,IDBankUnifoServiceImpl,Принят запрос на экспорт начислений (msgID:null).
	Строка 1735843: 19.02.25 10:23:12.631,https-jsse-nio-8443-exec-10,DEBUG,WebServiceUtils,Stopping application finished ms:0
	Строка 1742228: 19.02.25 10:23:14.074,https-jsse-nio-8443-exec-10,DEBUG,IDBankUnifoServiceImpl,Принят запрос на экспорт начислений (msgID:null).
	Строка 1742490: 19.02.25 10:23:14.101,https-jsse-nio-8443-exec-10,DEBUG,WebServiceUtils,Stopping application finished ms:0
	Строка 1791129: 19.02.25 10:23:20.784,https-jsse-nio-8443-exec-10,DEBUG,IDBankUnifoServiceImpl,Принят запрос на экспорт начислений (msgID:null).
	Строка 1791992: 19.02.25 10:23:20.857,https-jsse-nio-8443-exec-10,DEBUG,WebServiceUtils,Stopping application finished ms:0
	Строка 1812850: 19.02.25 10:23:23.539,https-jsse-nio-8443-exec-10,DEBUG,IDBankUnifoServiceImpl,Принят запрос на экспорт начислений (msgID:null).
	Строка 1813036: 19.02.25 10:23:23.570,https-jsse-nio-8443-exec-10,DEBUG,WebServiceUtils,Stopping application finished ms:1
	Строка 1819489: 19.02.25 10:23:24.995,https-jsse-nio-8443-exec-10,DEBUG,IDBankUnifoServiceImpl,Принят запрос на экспорт начислений (msgID:1003).
	Строка 1821122: 19.02.25 10:23:25.337,https-jsse-nio-8443-exec-10,DEBUG,WebServiceUtils,Stopping application finished ms:1
	Строка 1854658: 19.02.25 10:23:29.303,https-jsse-nio-8443-exec-10,DEBUG,IDBankUnifoServiceImpl,Принят запрос на экспорт начислений (msgID:1003).
	Строка 1856325: 19.02.25 10:23:29.624,https-jsse-nio-8443-exec-10,DEBUG,WebServiceUtils,Stopping application finished ms:0
	Строка 1899536: 19.02.25 10:23:36.557,https-jsse-nio-8443-exec-10,DEBUG,IDBankUnifoServiceImpl,Принят запрос на экспорт начислений (msgID:1003).
	Строка 1902687: 19.02.25 10:23:36.934,https-jsse-nio-8443-exec-10,DEBUG,WebServiceUtils,Stopping application finished ms:1
	Строка 1943278: 19.02.25 10:23:40.082,https-jsse-nio-8443-exec-10,DEBUG,IDBankUnifoServiceImpl,Принят запрос на экспорт начислений (msgID:1003).
	Строка 1946571: 19.02.25 10:23:40.618,https-jsse-nio-8443-exec-10,DEBUG,WebServiceUtils,Stopping application finished ms:0
	Строка 1971526: 19.02.25 10:23:43.317,https-jsse-nio-8443-exec-10,DEBUG,IDBankUnifoServiceImpl,Принят запрос на экспорт начислений (msgID:1003).
	Строка 1985115: 19.02.25 10:23:44.299,https-jsse-nio-8443-exec-10,DEBUG,WebServiceUtils,Stopping application finished ms:1
	Строка 2005241: 19.02.25 10:23:45.758,https-jsse-nio-8443-exec-10,DEBUG,IDBankUnifoServiceImpl,Принят запрос на экспорт начислений (msgID:null).
	Строка 2006791: 19.02.25 10:23:45.836,https-jsse-nio-8443-exec-10,DEBUG,WebServiceUtils,Stopping application finished ms:1
	Строка 2038181: 19.02.25 10:23:47.538,https-jsse-nio-8443-exec-10,DEBUG,IDBankUnifoServiceImpl,Принят запрос на экспорт начислений (msgID:null).
	Строка 2038678: 19.02.25 10:23:47.576,https-jsse-nio-8443-exec-10,DEBUG,WebServiceUtils,Stopping application finished ms:0
	Строка 2066807: 19.02.25 10:23:50.111,https-jsse-nio-8443-exec-10,DEBUG,IDBankUnifoServiceImpl,Принят запрос на экспорт начислений (msgID:null).
	Строка 2067025: 19.02.25 10:23:50.136,https-jsse-nio-8443-exec-10,DEBUG,WebServiceUtils,Stopping application finished ms:0
	Строка 2114184: 19.02.25 10:23:54.282,https-jsse-nio-8443-exec-10,DEBUG,IDBankUnifoServiceImpl,Принят запрос на экспорт начислений (msgID:null).
	Строка 2118313: 19.02.25 10:23:54.442,https-jsse-nio-8443-exec-10,DEBUG,WebServiceUtils,Stopping application finished ms:0
	Строка 2153494: 19.02.25 10:23:56.537,https-jsse-nio-8443-exec-10,DEBUG,IDBankUnifoServiceImpl,Принят запрос на экспорт начислений (msgID:null).
	Строка 2154077: 19.02.25 10:23:56.592,https-jsse-nio-8443-exec-10,DEBUG,WebServiceUtils,Stopping application finished ms:0
	Строка 2198008: 19.02.25 10:24:00.594,https-jsse-nio-8443-exec-10,DEBUG,IDBankUnifoServiceImpl,Принят запрос на экспорт начислений (msgID:null).
	Строка 2199382: 19.02.25 10:24:00.691,https-jsse-nio-8443-exec-10,DEBUG,WebServiceUtils,Stopping application finished ms:0
	Строка 2226227: 19.02.25 10:24:03.232,https-jsse-nio-8443-exec-10,DEBUG,IDBankUnifoServiceImpl,Принят запрос на экспорт начислений (msgID:null).
	Строка 2226755: 19.02.25 10:24:03.298,https-jsse-nio-8443-exec-10,DEBUG,WebServiceUtils,Stopping application finished ms:0
	Строка 2251634: 19.02.25 10:24:05.733,https-jsse-nio-8443-exec-10,DEBUG,IDBankUnifoServiceImpl,Принят запрос на экспорт начислений (msgID:1003).
	Строка 2257836: 19.02.25 10:24:06.209,https-jsse-nio-8443-exec-10,DEBUG,WebServiceUtils,Stopping application finished ms:0
	Строка 2292703: 19.02.25 10:24:09.678,https-jsse-nio-8443-exec-10,DEBUG,IDBankUnifoServiceImpl,Принят запрос на экспорт начислений (msgID:1003).
	Строка 2300329: 19.02.25 10:24:10.377,https-jsse-nio-8443-exec-10,DEBUG,WebServiceUtils,Stopping application finished ms:0
	Строка 2317658: 19.02.25 10:24:12.203,https-jsse-nio-8443-exec-10,DEBUG,IDBankUnifoServiceImpl,Принят запрос на экспорт начислений (msgID:1003).
	Строка 2322839: 19.02.25 10:24:12.622,https-jsse-nio-8443-exec-10,DEBUG,WebServiceUtils,Stopping application finished ms:0
	Строка 2356313: 19.02.25 10:24:16.012,https-jsse-nio-8443-exec-10,DEBUG,IDBankUnifoServiceImpl,Принят запрос на экспорт начислений (msgID:null).
	Строка 2357101: 19.02.25 10:24:16.122,https-jsse-nio-8443-exec-10,DEBUG,WebServiceUtils,Stopping application finished ms:0
	Строка 2373597: 19.02.25 10:24:17.766,https-jsse-nio-8443-exec-10,DEBUG,IDBankUnifoServiceImpl,Принят запрос на экспорт начислений (msgID:1003).
	Строка 2380859: 19.02.25 10:24:18.253,https-jsse-nio-8443-exec-10,DEBUG,WebServiceUtils,Stopping application finished ms:1
	Строка 2389702: 19.02.25 10:24:19.891,https-jsse-nio-8443-exec-10,DEBUG,IDBankUnifoServiceImpl,Принят запрос на экспорт начислений (msgID:null).
	Строка 2394429: 19.02.25 10:24:20.299,https-jsse-nio-8443-exec-10,DEBUG,WebServiceUtils,Stopping application finished ms:0
	Строка 2408343: 19.02.25 10:24:20.930,https-jsse-nio-8443-exec-10,DEBUG,IDBankUnifoServiceImpl,Принят запрос на экспорт начислений (msgID:null).
	Строка 2415396: 19.02.25 10:24:21.388,https-jsse-nio-8443-exec-10,DEBUG,WebServiceUtils,Stopping application finished ms:168
	Строка 2419812: 19.02.25 10:24:21.735,https-jsse-nio-8443-exec-10,DEBUG,IDBankUnifoServiceImpl,Принят запрос на экспорт начислений (msgID:null).
	Строка 2425332: 19.02.25 10:24:22.547,https-jsse-nio-8443-exec-10,DEBUG,WebServiceUtils,Stopping application finished ms:0
	Строка 2433836: 19.02.25 10:24:23.183,https-jsse-nio-8443-exec-10,DEBUG,IDBankUnifoServiceImpl,Принят запрос на экспорт начислений (msgID:1003).
	Строка 2506971: 19.02.25 10:24:27.314,https-jsse-nio-8443-exec-10,DEBUG,WebServiceUtils,Stopping application finished ms:4
	Строка 2520860: 19.02.25 10:24:27.910,https-jsse-nio-8443-exec-10,DEBUG,IDBankUnifoServiceImpl,Принят запрос на экспорт начислений (msgID:null).
	Строка 2524229: 19.02.25 10:24:28.079,https-jsse-nio-8443-exec-10,DEBUG,WebServiceUtils,Stopping application finished ms:1
	Строка 2541898: 19.02.25 10:24:29.623,https-jsse-nio-8443-exec-10,DEBUG,IDBankUnifoServiceImpl,Принят запрос на экспорт начислений (msgID:null).
	Строка 2546219: 19.02.25 10:24:29.917,https-jsse-nio-8443-exec-10,DEBUG,WebServiceUtils,Stopping application finished ms:1
	Строка 2548420: 19.02.25 10:24:30.146,https-jsse-nio-8443-exec-10,DEBUG,IDBankUnifoServiceImpl,Принят запрос на экспорт начислений (msgID:1003).
	Строка 2569927: 19.02.25 10:24:31.521,https-jsse-nio-8443-exec-10,DEBUG,WebServiceUtils,Stopping application finished ms:0
	Строка 2571038: 19.02.25 10:24:31.563,https-jsse-nio-8443-exec-10,DEBUG,IDBankUnifoServiceImpl,Принят запрос на экспорт начислений (msgID:null).
	Строка 2588785: 19.02.25 10:24:33.078,https-jsse-nio-8443-exec-10,DEBUG,WebServiceUtils,Stopping application finished ms:129
	Строка 2595060: 19.02.25 10:24:33.566,https-jsse-nio-8443-exec-10,DEBUG,IDBankUnifoServiceImpl,Принят запрос на экспорт начислений (msgID:null).
	Строка 2600281: 19.02.25 10:24:33.946,https-jsse-nio-8443-exec-10,DEBUG,WebServiceUtils,Stopping application finished ms:5
	Строка 2614765: 19.02.25 10:24:34.804,https-jsse-nio-8443-exec-10,DEBUG,IDBankUnifoServiceImpl,Принят запрос на экспорт начислений (msgID:1003).
	Строка 2620031: 19.02.25 10:24:35.218,https-jsse-nio-8443-exec-10,DEBUG,WebServiceUtils,Stopping application finished ms:1
	Строка 2625950: 19.02.25 10:24:35.784,https-jsse-nio-8443-exec-10,DEBUG,IDBankUnifoServiceImpl,Принят запрос на экспорт начислений (msgID:null).
	Строка 2627595: 19.02.25 10:24:35.889,https-jsse-nio-8443-exec-10,DEBUG,WebServiceUtils,Stopping application finished ms:0
	Строка 2631290: 19.02.25 10:24:36.271,https-jsse-nio-8443-exec-10,DEBUG,IDBankUnifoServiceImpl,Принят запрос на экспорт начислений (msgID:null).
	Строка 2633037: 19.02.25 10:24:36.403,https-jsse-nio-8443-exec-10,DEBUG,WebServiceUtils,Stopping application finished ms:1
	Строка 2656171: 19.02.25 10:24:38.227,https-jsse-nio-8443-exec-10,DEBUG,IDBankUnifoServiceImpl,Принят запрос на экспорт начислений (msgID:1003).
	Строка 2683994: 19.02.25 10:24:39.686,https-jsse-nio-8443-exec-10,DEBUG,WebServiceUtils,Stopping application finished ms:214
	Строка 2712370: 19.02.25 10:24:42.159,https-jsse-nio-8443-exec-10,DEBUG,IDBankUnifoServiceImpl,Принят запрос на экспорт начислений (msgID:null).
	Строка 2738889: 19.02.25 10:24:44.674,https-jsse-nio-8443-exec-10,DEBUG,WebServiceUtils,Stopping application finished ms:1
	Строка 2739835: 19.02.25 10:24:44.776,https-jsse-nio-8443-exec-10,DEBUG,IDBankUnifoServiceImpl,Принят запрос на экспорт начислений (msgID:null).
	Строка 2839437: 19.02.25 10:24:56.322,https-jsse-nio-8443-exec-10,DEBUG,WebServiceUtils,Stopping application finished ms:1
	Строка 2839476: 19.02.25 10:24:56.329,https-jsse-nio-8443-exec-10,DEBUG,IDBankUnifoServiceImpl,Принят запрос на экспорт начислений (msgID:null).
	Строка 2948704: 19.02.25 10:25:06.663,https-jsse-nio-8443-exec-10,DEBUG,WebServiceUtils,Stopping application finished ms:0
	Строка 2948715: 19.02.25 10:25:06.665,https-jsse-nio-8443-exec-10,DEBUG,IDBankUnifoServiceImpl,Принят запрос на экспорт начислений (msgID:null).
	Строка 3031061: 19.02.25 10:25:11.684,https-jsse-nio-8443-exec-10,DEBUG,WebServiceUtils,Stopping application finished ms:1'''

linesp=stt.split('\n')

for i in range(len(linesp)):
    if i%2==0:
        _,_,_,e1time,*args=linesp[i].split()
        date_time_obj1 =datetime.datetime.strptime(e1time[:12],'%H:%M:%S.%f')
    else:
        _, _, _, e2time, *args = linesp[i].split()
        date_time_obj2 = datetime.datetime.strptime(e2time[:12],'%H:%M:%S.%f')
        print(date_time_obj2-date_time_obj1)

