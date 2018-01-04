import csv
import json
import os,sys
import pdb

writer = csv.writer(open("test.csv","w"))
writer.writerow(["folder_name","file_name","type1_score","type2_score"])

def ave(lis):
	tot = 0
	for i in range(len(lis)):
		tot += lis[i]
	return float(tot)/float(len(lis))

people = [0,1,2,3,4,6,7,8,9,10]

folders = os.listdir("./data")
for folder in folders:
	ap_list = []
	files = os.listdir("./data/"+folder)
	for file in files:
		# print file[:7]
		if file[:7]=='points_':
			# print file
			loc_list=[folder,file]
			number = int(file[-6])
			game = json.load(open("./data/"+folder+"/"+file))["ROUND80"]
			# print game
			for i in range(len(game)):
				game[i] = int(game[i])
			# print game
			# print people[number]
			# print game
			player1 = game[:people[number]]
			player2 = game[people[number]:]
			# print player1
			# print player2
			player1_score = ave(player1)
			player2_score = ave(player2)
			# print player1_score,player2_score
			loc_list.append(player1_score)
			loc_list.append(player2_score)
			ap_list.append(loc_list)
	# print ap_list
	writer.writerows(ap_list)
	# pdb.set_trace()


