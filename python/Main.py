#!/usr/bin/env python3.2
# -*- coding: utf-8 -*-
# vim:fileencoding=utf8
# CDDL HEADER START
#
# The contents of this file are subject to the terms of the
# Common Development and Distribution License (the "License").
# You may not use this file except in compliance with the License.
#
# You can obtain a copy of the license in the CDDL_LICENSE file
# or at http://dev.sikevux.se/LICENSE.txt
# See the License for the specific language governing permissions
# and limitations under the License.
#
# When distributing Covered Code, include this CDDL HEADER in each
# file and include the License file CDDL_LICENSE.
# If applicable, add the following below this CDDL HEADER, with the
# fields enclosed by brackets "[]" replaced with your own identifying
# information: Portions Copyright [yyyy] [name of copyright owner]
#
# CDDL HEADER END
# 
#
# Copyright 2011 Patrik Greco All rights reserved.
# Use is subject to license terms.
#

import urllib.request
import urllib.parse
import io
import json
import os
import sys

user_input_url = str(input("URL to the stream "))

if user_input_url.startswith("http://svt") is not True:
	print("Bad URL. Not SVT Play?")
	sys.exit()

HTTP_socket = urllib.request.urlopen("http://svtget.se/get/get.php?" + str(urllib.parse.urlencode({"url" : user_input_url}).encode('utf-8'), 'utf-8'))
HTML_source = HTTP_socket.read().decode('utf-8')
HTTP_socket.close()
io = io.StringIO(HTML_source)
json_data = json.load(io)

print("#	Bitrate	Filename")

n=0

for tcUrl in json_data['tcUrls']:
	print(n, "	" + tcUrl[1] + "	" + tcUrl[0])
	n+=1

user_input_n = int(input("Which file do you want? [#] "))

print("Running RTMPDump on " + json_data['tcUrls'][user_input_n][0] + " and saving it as " + json_data['program_name'] + ".mp4")

os.system('rtmpdump -r ' + json_data['tcUrls'][user_input_n][0] + ' --swfVfy=' + json_data['swfUrl'] + ' -o ' + json_data['program_name'] + '.mp4')
