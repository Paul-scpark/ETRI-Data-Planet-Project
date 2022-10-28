from konlpy.tag import Mecab
import pandas as pd

df = pd.read_csv("../total_data.csv", encoding="utf-8")
df.dropna(axis=0, inplace=True)
descript = df.loc[:, "description"]

tagger = Mecab()

noun_list = []
for script in descript:
    nouns = tagger.nouns(script)
    temp = " ".join(nouns)
    noun_list.append(temp)


df["description"] = noun_list
df.to_csv("../tokenized_data.csv", index=None)