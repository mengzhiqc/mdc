# -*- coding: utf-8 -*-

# normal regex for access_log

# 0.098 0.098 120.128.6.101 894 10.10.3.23:20080  [13/Jan/2013:23:59:16 +0800] www.aifang.com "GET /wenda/ajax/GetApprove/?qid=1488190&page=1&_t=0.8030165014792372 HTTP/1.1" 200 373 "http://www.aifang.com/wenda/v1488190.html" "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1)" "-" "-" - "58.247.138.74 BCBCA2AC-18A7-72B1-9550-1F3E3C6A16B5"

normal_regex = r"""
(?P<request_time>[0-9.]+|\-)
\s
(?P<upstream_response_time>[0-9.]+|\-)
\s
(?P<remote_addr>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|\-)
\s
(?P<request_length>\d+)
\s
(?P<upstream_addr>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|\-)(:\d{1,5})?
\s+
\[(?P<day>\d{2})\/
(?P<month>[A-Z][a-z]{2}?)\/
(?P<year>\d{4})\:
(?P<hour>\d{2})\:
(?P<min>\d{2})\:
(?P<sec>\d{2})
\s+\+0800\]
\s
(?P<hostname>[^\s]+?)
\s
"
(?P<method>[A-Z]+)
\s
(?P<request_uri>[^\s]+?)
\s
HTTP/[0-9.]+
"
\s
(?P<http_code>\d{3})
\s
(?P<bytes_sent>\d+)
\s
"
(?P<referer>([^\"]+|\-))
"
\s
"(?P<user_agent>([^\"]+|\-))"
\s
"(?P<gzip_ratio>([^\"]+|\-))"
\s
"(?P<http_x_forwarded_for>([^\"]+|\-))"
\s
-
\s
"
(
(?P<server_addr>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})
(:
(?P<server_port>\d+))?
|\-)
(\s)?
((?P<guid>.+?))?
"
.*
"""

