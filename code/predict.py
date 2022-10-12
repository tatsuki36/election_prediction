import ast

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import GradientBoostingRegressor, GradientBoostingClassifier
from sklearn.metrics import classification_report, confusion_matrix

with open('../dataset/popularity201710.txt',"r") as f:
	populality2017 = ast.literal_eval(f.read())

#読み込み
shugiin2017 = pd.read_csv("../dataset/shugiin2017.csv", names=["name","age","n_of_votes", "voting_rate", "party", "new_or_old", "n_of_wins", "win_or_lose"])

# print(shugiin2017.nunique())
# print(shugiin2017["party"].unique())

#支持率カラム追加
party_popularity = shugiin2017["party"].map(populality2017)
# print(party_popularity.isnull().all())
shugiin2017["party_popularity"] = party_popularity

#ダミー化
df = shugiin2017.drop("name",axis=1)
df = pd.get_dummies(df)

print(df.columns)
print(df.info())
print(df.describe())
print(df)

#分類
#学習データ作成
columns = ['age', 'n_of_wins',
       'party_popularity', 'party_公明', 'party_共産', 'party_希望', 'party_無所',
       'party_社民', 'party_立憲', 'party_維新', 'party_自民', 'party_諸派',
       'new_or_old_元', 'new_or_old_前', 'new_or_old_新']
X = df[columns]
y = df["win_or_lose"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=0, shuffle=True, stratify=y)

# X_real = pd.DataFrame([[59,6,38.8,0,0,0,0,0,0,0,1,0,0,1,0],[71,0,0,0,0,0,1,0,0,0,0,0,0,0,1],[75,13,6.6,0,0,0,0,0,1,0,0,0,0,1,0]])

#学習
# clf = GradientBoostingClassifier(random_state=0)
# clf.fit(X_train, y_train)

# テスト
# y_pred = clf.predict(X_test)
# print(classification_report(y_test, np.round(y_pred)))
# cm = confusion_matrix(y_test, np.round(y_pred))
# cm = pd.DataFrame(data=cm, index=[0, 1], columns=[0, 1])
# sns.heatmap(cm, square=True, cbar=True, annot=True, cmap='Blues')
# plt.yticks(rotation=0)
# plt.xlabel("pred", fontsize=13, rotation=0)
# plt.ylabel("true", fontsize=13)
# plt.show()

# y_pred = clf.predict_proba(X_real)
# print(y_pred)

# fi = dict(zip(columns, clf.feature_importances_))
# fi_sorted = sorted(fi.items(), key=lambda x:x[1], reverse=True)
# new_fi = dict()
# new_fi.update(fi_sorted)
# plt.bar(new_fi.keys(), new_fi.values())
# plt.tick_params(labelsize=5)
# plt.show()

#回帰
# 学習データ作成
columns = ['age', 'n_of_wins',
       'party_popularity', 'party_公明', 'party_共産', 'party_希望', 'party_無所',
       'party_社民', 'party_立憲', 'party_維新', 'party_自民', 'party_諸派',
       'new_or_old_元', 'new_or_old_前', 'new_or_old_新']
X = df[columns]
y = df["voting_rate"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=0, shuffle=True)

X_real = pd.DataFrame([[59,6,38.8,0,0,0,0,0,0,0,1,0,0,1,0],[71,0,0,0,0,0,1,0,0,0,0,0,0,0,1],[75,13,6.6,0,0,0,0,0,1,0,0,0,0,1,0]])

#学習
gbr = GradientBoostingRegressor(random_state=0).fit(X_train, y_train)

# #テスト
# y_pred = gbr.predict(X_test)
# rmse = np.sqrt(mean_squared_error(y_test, y_pred))
# print(rmse)
# print(y_test)
# print(y_pred)

y_pred = gbr.predict(X_real)
print(y_pred)

