#!/usr/bin/python

import MySQLdb
dwDbConn = MySQLdb.connect(host="10.20.8.39",user="readonly_v2",passwd="aNjuKe9dx1Pdw",db="dw_db")
fetchCursor = dwDbConn.cursor()

sql = "SELECT log_time,city_id,url,mac_id,cv,request_time,app,pm FROM dw_iphone_imp_dtl"
n = fetchCursor.execute(sql,{})

mdcDbConn = MySQLdb.connect(host="10.20.8.39",user="readonly_v2",passwd="aNjuKe9dx1Pdw",db="MobileMDC")