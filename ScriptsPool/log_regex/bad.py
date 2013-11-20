# -*- coding: utf-8 -*-

# bad 400 regex

# 0.000 - 113.123.35.212 0 -  [17/Jan/2013:16:39:59 +0800]  "-" 400 0 "-" "-" "-" "-" - "114.80.230.198 -"

bad400_regex = r"""
(?P<request_time>\d+(\.\d+)?)
\s
-
\s
(?P<remote_addr>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})
\s
(?P<request_length>\d+)
\s
-
\s+
\[
(?P<day>\d+)
\/
(?P<month>[A-Za-z]{3})
\/
(?P<year>\d+)
:
(?P<hour>\d+)
:
(?P<min>\d+)
:
(?P<sec>\d+)
\s\+0800
\]
\s+
"-"
\s
(?P<http_code>\d{3})
\s
(?P<bytes_sent>\d+)
\s
"-"
\s
"-"
\s
"-"
\s
"-"
\s
-
\s
"
(
(?P<server_addr>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})
(:
(?P<server_port>\d+))?
|\-)
\s
-
"
"""

