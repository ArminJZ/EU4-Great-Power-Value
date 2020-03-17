import re
import csv
import os
import json
import demjson
import threading as thd
from hashlib import md5
import time
import pandas as pd


old_hex_digest = ""

def create_csv():
	path="score_result.csv"
	with open(path, 'w') as f:
		csv_writer=csv.writer(f)
		csv_writer.writerow(['Date'])
	f.close()



def parse_eu4():

	m = md5()

	file_name = "autosave.eu4"

	md5_file = open(file_name, 'rb')
	m.update(md5_file.read())
	md5_file.close()
	new_hex_digest=m.hexdigest()
	global old_hex_digest
	if old_hex_digest != new_hex_digest:
		print("Hexdigest will be changed")
		old_hex_digest = new_hex_digest
		print(new_hex_digest)
	else:
		print("Hexdigest will not be changed")
		return 
	# 这里算出了md5值后和之前存储的md5对比，如果md5发生了变化就要进行下一次的追加存储


	with open(file_name, "r", encoding='windows-1252') as f:
		old_score_df = pd.read_csv('score_result.csv', index_col=0)
		print(old_score_df)
		exist_great_power=old_score_df[0:1]

		date = f.readlines()[1][5:].replace("\n", "") # 这里存储效率太低了，要读取文件的所有行
		result = {}
		result.update({'Date':date})
		# old_score_df = old_score_df.append([{'Date':date}])


		f.seek(0)	# 让光标回到第一行
		re_great_powers=re.compile(r'original=({[^{}]*})')
		ranking_result=re_great_powers.findall(f.read())
		for each_great_power in ranking_result:
			each_great_power=each_great_power.replace("\n\t","").replace("\t", ",").replace("=",":")
			dict_great_power=demjson.decode(each_great_power[0:1]+each_great_power[2:])
			result.update({dict_great_power['country']:dict_great_power['value']})
		print(result)
		old_score_df = old_score_df.append(result, ignore_index=True)
		print(old_score_df)
		old_score_df.to_csv('score_result.csv')
		f.close()

		return result

if os.path.exists("score_result.csv")==True:
	while True:
		parse_eu4()
		time.sleep(60)
else:
	create_csv()




