# /usr/bin/python
# -*- coding: utf-8 -*-

import requests
import sys
import lxml
import re
from bs4 import BeautifulSoup
# python getNPB.py 
# -> generate .txt and .csv file including 1950~2016 data of both central and pacific league
# python getNPB.py 1996
# -> return league data of 1996 season

argvs = sys.argv        
argc = len(argvs)       

def getNpbData(year, league): # year is 1950 ~ 2016 / league is "central" or "pacific"

	outputs = {"txt":"", "csv":""}
	headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"}
	URL = "http://npb.jp/bis/yearly/" + league + "league_" + str(year) +".html"
	resp = requests.get(URL, timeout=2, headers=headers)
	soup = BeautifulSoup(resp.content, "lxml")
	tables = soup.find(class_='contentsBorder').find_all(class_='contentsPadding')  
	# mainの<div>内のデータの<table>取得
	# テーブル3つ取得して２次元配列 => チーム毎にサーチをかけてfor文回す
	# team, all, win, lose, draw, winprob, batting ave, bats, get points, hits, double, triple, HR, RBI, steal, protection ratio, save, whole pitch, strikeouts, lost points のベクトルにする
	
	table_1_array = []
	table_2_array = []
	table_3_array = []

	table_1_tr = tables[0].find('table').find_all('tr') # tr-行要素の配列抽出
	for i in range(len(table_1_tr)): 
		table_1_td = table_1_tr[i].find_all('td') #  td-列データ要素の配列抽出
		td_array = [] # init
		for n in range(len(table_1_td)): # 行方向にデータを配列に格納
			td_array.append(table_1_td[n].text)
		td_array.append(i) #順位の挿入
		table_1_array.append(td_array)	

	table_2_tr = tables[1].find('table').find_all('tr')
	for i in range(len(table_2_tr)):
		table_2_td = table_2_tr[i].find_all('td')
		td_array = []
		for n in range(len(table_2_td)):
			td_array.append(table_2_td[n].text)
		table_2_array.append(td_array)

	table_3_tr = tables[2].find('table').find_all('tr')
	for i in range(len(table_3_tr)):
		table_3_td = table_3_tr[i].find_all('td')
		td_array = []
		for n in range(len(table_3_td)):
			td_array.append(table_3_td[n].text)
		table_3_array.append(td_array)

	del table_1_array[0]
	del table_2_array[0]
	del table_3_array[0]

	# sort by team name
	table_1_array.sort(key=lambda x:x[0])
	table_2_array.sort(key=lambda x:x[0])
	table_3_array.sort(key=lambda x:x[0])

	print(("セントラル" if league == "central" else "パシフィック") + "・リーグ" + str(year) + "年データを取得中...")	
	
	# 行列要素数確認用
	# print("チーム数 : ",len(table_1_array)," teams")
	# print("チーム別成績 :  ",len(table_1_td)," elements")
	# print("攻撃成績 : ",len(table_2_td), " elements")
	# print("投手成績 : ",len(table_3_td), " elements")

	for i in range(len(table_1_array)):
		
		rank = table_1_array[i][-1]
		team = table_1_array[i][0]
		allGames = table_1_array[i][1]
		win = table_1_array[i][2]
		lose = table_1_array[i][3]
		draw = table_1_array[i][4]
		winProb = table_1_array[i][6]
		battingAve = table_2_array[i][1]
		bats = table_2_array[i][3]
		getPoints = table_2_array[i][4]
		hits = table_2_array[i][5]
		double = table_2_array[i][6]
		triple = table_2_array[i][7]
		hr = table_2_array[i][8]
		rbi = table_2_array[i][9]
		steal = table_2_array[i][10]
		protectionRatio = table_3_array[i][1]
		# save = table_3_array[i][5]
		wholePitch = table_3_array[i][6]
		strikeOuts = table_3_array[i][10]
		lostPoints = table_3_array[i][11]

		outputs["txt"] += str(year) +' '+ league +' '+ str(rank) +' '+ team + ' '+ allGames +' '+ win +' '+ lose +' '+ draw +' '+ winProb +' '+ battingAve +' '+ bats +' '+ getPoints +' '+ hits +' '+ double +' '+ triple +' '+ hr +' '+ rbi +' '+ steal +' '+ protectionRatio +' '+ wholePitch +' '+ strikeOuts +' '+ lostPoints + '\n'
		outputs["csv"] += str(year) + ',' + league + ',' + str(rank) +','+ team +','+ allGames +','+ win +','+ lose +','+ draw +','+ winProb +','+ battingAve +','+ bats +','+ getPoints +','+ hits +','+ double +','+ triple +','+ hr +','+ rbi +','+ steal +','+ protectionRatio +','+ wholePitch +','+ strikeOuts +','+ lostPoints + '\n'

	return outputs

# __init__#

if argc > 1: # 引数指定時
	
	output = "年 リーグ 順位 チーム 全試 勝 負 引 勝率 打率 打数 得点 安打 二塁打 三塁打 本塁打 打点 盗塁 防御率 完投 脱三振 失点\n"

	for n in range(argc-1):
		d = argvs[n+1]
		if d.isdecimal():
			if int(d) < 2017 and int(d) > 1949:
				print(output + getNpbData(int(d), "central")["txt"])
				print(output + getNpbData(int(d), "pacific")["txt"])
			else:
				print("Please put year number within 1950 to 2016.")
		else:
			print("put year(1950~2016) numbers as augments. if you put no arguments, it will generate '.txt' and '.csv' file of 1950~2016 datas on the same directory.")

else:

	head = "This is NPB datas. crawled by Atsuya Kobayashi 2018/01/03\n\n"
	output = "Year League Rank Team All-Games Win Lose Draw Win-Prob Batting-Average Bats Points Hits Double Triple HR RBI Steal Protection-Ratio Whole-Pitch Strike-Outs Lost-Points\n"
	csvoutput = "Year,League,Rank,Team,All-Games,Win,Lose,Draw,Win-Prob,Batting-Average,Bats,Points,Hits,Double,Triple,HR,RBI,Steal,Protection-Ratio,Whole-Pitch,Strike-Outs,Lost-Points\n"

	for year in range(1950, 2018):
		res = getNpbData(year, "central")
		output += res["txt"]
		csvoutput += res["csv"]

	cc = open('central_league.csv', 'w')
	cc.write(csvoutput)
	print("central_league.csv を出力中...")
	cc.close()
	ct = open('central_league.txt', 'w')
	ct.write(output)
	print("central_league.txt を出力中...")
	ct.close()

	# init output string
	output = "Year League Rank Team All-Games Win Lose Draw Win-Prob Batting-Average Bats Points Hits Double Triple HR RBI Steal Protection-Ratio Whole-Pitch Strike-Outs Lost-Points\n"

	for year in range(1950, 2018):
		res = getNpbData(year, "pacific")
		output += res["txt"]
		csvoutput += res["csv"]
		
	pc = open('pacific_league.csv', 'w')
	pc.write(csvoutput)
	print("pacific_league.csv を出力中...")
	pc.close()
	pt = open('pacific_league.txt', 'w')
	pt.write(output)
	print("pacific_league.txt を出力中...")
	pt.close()
