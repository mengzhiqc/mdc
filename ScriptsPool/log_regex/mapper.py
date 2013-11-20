# -*- coding: utf-8 -*-

def get_field_name(name):
    mapper = {
            "hour":                   "A",
            "year":                   "B",
            "day":                    "C",
            "min":                    "D",
            "request_time":           "E",
            "upstream_response_time": "F",
            "remote_addr":            "G",
            "upstream_addr":          "H",
            "hostname":               "I",
            "method":                 "J",
            "request_uri":            "K",
            # L
            "http_code":              "M",
            "bytes_sent":             "N",
            "referer":                "O",
            "user_agent":             "P",
            "gzip_ratio":             "Q",
            "http_x_forwarded_for":   "R",
            "server_addr":            "S",
            "guid":                   "T",
            "sec":                    "U",
            "month":                  "V",
            "request_length":         "W",
            "server_port":            "X"
            }
    return mapper[name]

