#!/usr/bin/env python
# -*- coding: utf-8 -*-

import msgpack
import zmq
import sys
import re
import datetime
import time
import argparse
import os
import commands
from logging import basicConfig, getLogger, DEBUG
from traceback import print_exc
from os.path import exists, realpath, dirname
import log_regex
from log_regex import get_field_name

logging_format = '%(asctime)-15s [%(levelname)s]: %(message)s'
basicConfig(format=logging_format, level=DEBUG)
logger = getLogger()

LOG_PATH = realpath(dirname(realpath(sys.argv[0])) + "/../../logs")
DEFAULT_FIELD_VALUE = "-"

TIMEDELTA_ONE_MIN = datetime.timedelta(seconds=60)

F_TYPE_STRING = "string"
F_TYPE_INT = "integer"
F_TYPE_FLOAT = "float"

# [field name, field type]
FIELDS = [
    ["request_time", F_TYPE_FLOAT],
    ["upstream_response_time", F_TYPE_FLOAT],
    ["remote_addr", F_TYPE_STRING],
    ["request_length", F_TYPE_INT],
    ["upstream_addr", F_TYPE_STRING],
    ["year", F_TYPE_INT],
    ["month", F_TYPE_STRING], # Jan Feb...
    ["day", F_TYPE_INT],
    ["hour", F_TYPE_INT],
    ["min", F_TYPE_INT],
    ["sec", F_TYPE_INT],
    ["hostname", F_TYPE_STRING],
    ["method", F_TYPE_STRING],
    ["request_uri", F_TYPE_STRING],
    ["http_code", F_TYPE_INT],
    ["bytes_sent", F_TYPE_INT],
    ["referer", F_TYPE_STRING],
    ["user_agent", F_TYPE_STRING],
    ["gzip_ratio", F_TYPE_FLOAT],
    ["http_x_forwarded_for", F_TYPE_STRING],
    ["server_addr", F_TYPE_STRING],
    ["server_port", F_TYPE_INT],
    ["guid", F_TYPE_STRING]
]

class Parser:
    def __init__(self, host, port):
        self.context = zmq.Context()
        self.recver = self.context.socket(zmq.PULL)
        self.recver.setsockopt(zmq.HWM, 2)
        self.recver.connect("tcp://%s:%s" % (host, port))
        self.poller = zmq.Poller()
        self.poller.register(self.recver, zmq.POLLIN)
        self.normal_regex = re.compile(log_regex.normal_regex, re.VERBOSE)
        self.bad400_regex = re.compile(log_regex.bad400_regex, re.VERBOSE)

        self.monmap = {
                "Jan": '01',
                "Feb": '02',
                "Mar": '03',
                "Apr": '04',
                "May": '05',
                "Jun": '06',
                "Jul": '07',
                "Aug": '08',
                "Sep": '09',
                "Oct": '10',
                "Nov": '11',
                "Dec": '12'
        }

    def terminate(self):
        self.recver.close()

    def _convert(self, line):
        retdoc = {}

        try:
            # normal
            doc = self.normal_regex.match(line).groupdict()
        except:
            try:
                # bad 400
                doc = self.bad400_regex.match(line).groupdict()
            except Exception, e:
                logger.error("not matched line: %s" % line)
                return False

        try:
            for field in FIELDS:
                self._set_field_value(doc, retdoc, field[0], field[1])

        except:
            print_exc()
            return False

        return retdoc

    def _set_field_value(self, src_doc, dst_doc, field_name, field_type):

        dst_filed_name = get_field_name(field_name)

        if field_name in src_doc:
            # exists
            if src_doc[field_name] == 0:
                dst_doc[dst_filed_name] = src_doc[field_name]
            dst_doc[dst_filed_name] = src_doc[field_name]

            if field_type in [F_TYPE_INT, F_TYPE_FLOAT] and \
                (src_doc[field_name] == DEFAULT_FIELD_VALUE or
                 (not src_doc[field_name])):
                dst_doc[dst_filed_name] = -1

            if field_name in ["request_time", "upstream_response_time"] and \
                src_doc[field_name] >= 0:
                dst_doc[dst_filed_name] = float(dst_doc[dst_filed_name]) * 1000

            if field_name == "month":
                dst_doc[dst_filed_name] = self.monmap[dst_doc[dst_filed_name]]

        else:
            # not exists
            if field_type == F_TYPE_STRING:
                dst_doc[dst_filed_name] = DEFAULT_FIELD_VALUE
            else:
                dst_doc[dst_filed_name] = -1

    def _get_num(self, s):
        if s == DEFAULT_FIELD_VALUE:
	    return -1
        else:
            return float(s) * 1000

    def _get_string_field(self, val):
        if val:
            return str(val)
        else:
            return DEFAULT_FIELD_VALUE

    def _normalize_line(self, line):
        line = line.strip()
        try:
            line = line.encode('utf8')
        except Exception, exception:
            try:
                line = line.decode('gb18030', 'ignore').encode('utf8')
            except Exception, exception:
                logger.error(str(exception))
                logger.error(line)
        return line

    def run_system_command(self, cmd):
        """
        run system command

        return (return_code, message)
        """
        ret = commands.getstatusoutput(cmd)
        if ret[0] != 0:
            logger.error("put command error: %s" % str(ret[1]))
        return (ret[0], ret[1])

    def _get_current_datetime(self):
        """
        return current filename according to system datetime

        datetime.datetime.now()
        """
        return datetime.datetime.now()

    def parse(self):

        sep = "\t"
        c = 0
        prev_outfilename = ''
        current_file = None

        line_counter = 0

        while True:

            socks = dict(self.poller.poll(1000))
            if self.recver in socks and socks.get(self.recver) == zmq.POLLIN:
                msg = self.recver.recv()
            else:
                # wait for next run
                continue
            msg = msgpack.unpackb(msg)
            line = self._normalize_line(msg)
            line_counter += 1

            if not line:
                # not a valid line
                continue
            doc = self._convert(line)

            if not doc:
                # regex not matched
                continue

            current_datetime = self._get_current_datetime()
            w_date = (current_datetime - TIMEDELTA_ONE_MIN) \
                    .strftime("%Y%m%d%H")
            current_filename = "access_log_%s_log.current" % \
                    current_datetime.strftime("%Y%m%d%H%M")

            if not prev_outfilename:
                current_file = open(current_filename, 'a')

            if (prev_outfilename and prev_outfilename != current_filename):

                if current_file:
                    current_file.flush()
                    current_file.close()

                    # 'access_log_YYYYMMDDHHmmSS_log.current'
                    w_filename = prev_outfilename

                    # 'access_log_YYYYMMDDHHmmSS_log'
                    w_new_filename = w_filename.replace('.current', '')
                    w_gzipped_filename = w_new_filename + ".gz"

                    logger.debug(w_filename)
                    logger.debug(w_new_filename)
                    logger.debug(w_gzipped_filename)

                    if exists(LOG_PATH):
                        with open(LOG_PATH + "/" + w_filename,
                                "w") as lf:
                            lf.write(str(line_counter))
                            line_counter = 0

                    os.rename(w_filename, w_new_filename)
                    cmd = "gzip %s" % w_new_filename
                    logger.debug(cmd)
                    ret, err_msg = self.run_system_command(cmd)
                    if ret == 0:

                        p_year = w_date[:4]
                        p_month = w_date[4:6]
                        p_day = w_date[6:8]
                        p_hour = w_date[8:10]

                        remove_cmd = 'hadoop dfs -rm '
                        remove_cmd += \
                        '/user/hadoop/speed/p_year=%s/p_month=%s/p_day=%s/p_hour=%s/%s'
                        remove_cmd %= (p_year, p_month, p_day,
                                p_hour, w_gzipped_filename)

                        cmd = 'hadoop dfs -put %s '
                        cmd += \
                        '/user/hadoop/speed/p_year=%s/p_month=%s/p_day=%s/p_hour=%s/%s'
                        cmd %= (w_gzipped_filename, p_year, p_month, p_day,
                                p_hour, w_gzipped_filename)
                        ret = -1
                        put_retry_count = 0
                        while ret != 0 and put_retry_count < 2:
                            put_retry_count += 1

                            logger.debug(cmd)
                            ret, err_msg = self.run_system_command(cmd)
                            logger.debug(ret)
                            logger.debug(err_msg)
                            if ret == 0:
                                if exists(w_gzipped_filename):
                                    logger.debug("removing %s" %
                                            w_gzipped_filename)
                                    # os.remove(w_gzipped_filename)
                                break
                            else:
                                # put failed
                                # make sure that file not exists for next put
                                logger.debug(remove_cmd)
                                self.run_system_command(remove_cmd)


                current_file = open(current_filename, 'a')
                logger.debug('start to write %s' % current_filename)

            doc = sorted(doc.items(), key=lambda(k, v): (k, v))
            output = []
            for k, v in doc:
                output.append(v)
            output = sep.join(map(str, output)) + "\n"

            current_file.write(output)


            prev_outfilename = current_filename

def main():
    parser = argparse.ArgumentParser("access_log parser for hadoop hdfs")

    parser.add_argument('-H' , '--host', help="connect source host",
                        required=True)
    parser.add_argument('-p' , '--port', help="connect source port",
                        required=True)

    args = parser.parse_args()

    p = Parser(args.host, args.port)
    p.parse()

if __name__=="__main__":
    sys.exit(main())