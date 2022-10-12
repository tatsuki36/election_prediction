import ast

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib
import seaborn as sns

with open('../dataset/popularity201710.txt',"r") as f:
	populality2017 = ast.literal_eval(f.read())

#読み込み
shugiin2017 = pd.read_csv("../dataset/shugiin2017.csv", names=["name","age","n_of_votes", "voting_rate", "party", "new_or_old", "n_of_wins", "win_or_lose"])
search_df = shugiin2017[["name","party"]]

while True:
	query = input('>> ')
	if query == "q":
		break
	query = query.replace(' ', '')
	judge_df = search_df["name"] == query
	print(judge_df.any())
	if judge_df.any():
		print(shugiin2017[judge_df])