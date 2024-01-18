import matplotlib.pyplot as plt
import japanize_matplotlib
import pandas as pd
import base64
from io import BytesIO
from urllib.request import urlopen, Request
import requests

def Output_Graph():
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    img = buffer.getvalue()
    graph = base64.b64encode(img)
    graph = graph.decode("utf-8")
    buffer.close()
    return graph

def Plot_Graph(mainx, mainy, x, y, title, subtitle):
    plt.switch_backend("AGG")
    plt.figure(figsize=(6, 4))
    plt.xlim(-12, 12)
    plt.ylim(-12, 12)
    plt.axvline(x=0, color="g", linestyle="dotted")
    plt.axhline(y=0, color="g", linestyle="dotted")
    plt.scatter(mainx, mainy, s=300, c="yellow", marker="*", edgecolors="orange")
    plt.scatter(x, y, s=40, c="pink", marker="o", alpha=0.5)
    plt.title("お米の特徴図")
    plt.xlabel("しっかり<----->もちもち", color="r")
    plt.ylabel("あっさり<----->甘い", color="r")
    xy  = (mainx - 1.5, mainy - 2)
    plt.annotate(title, xy)
    for i in range(len(subtitle)):
        target = (x[i] - 1.5, y[i] - 2)
        plt.annotate(subtitle[i], target, color="black", alpha=0.3)
    # plt.grid(True)
    plt.tight_layout()
    graph = Output_Graph()
    return graph

def Productor_Statistics_Graph():
    url = "https://www.e-stat.go.jp/stat-search/files/data?sinfid=000040080140&ext=xls"
    # url += '&download=1'
    #  , engine='openpyxl'
    # 出典：政府統計の総合窓口(e-Stat)農業・食料関連産業の経済計算 / 作況調査(水陸稲、麦類、豆類、かんしょ、飼料作物、工芸農作物) / 収穫量累年統計 / 水稲 / 全国(明治16年～令和3年)（https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040000680&fileKind=0）
    # 「作物統計調査」（農林水産省）を加工して作成
    resp = requests.get(url)
    df = pd.read_excel(BytesIO(resp.content), sheet_name=[1 , 7]) 
    # df["t"].astype(float)
    age = df[1].iloc[9 : 16, 0].tolist()
    new_employee = df[1].iloc[9 : 16 , 12].tolist()
    newcomer = df[1].iloc[9 : 16 , -1].tolist()
    
    plt.switch_backend("AGG")
    plt.figure(figsize=(6, 4))
    plt.bar(age, new_employee, align="edge", width=-0.3, color="lightblue", label="新規雇用就農者数")
    plt.bar(age, newcomer, align="edge", width=0.3, color="pink", label="新規参入者数")
    plt.title("就農形態別新規就農者数（令和４年）")
    plt.xticks(fontsize=8)
    plt.legend()
    graph = Output_Graph()

    kinds = df[7].iloc[4, 1:]
    kinds_num = [x for x in range(13)]
    amount = df[7].iloc[5, 1:]
    print(kinds_num)
    print(amount)
    print(kinds)

    plt.switch_backend("AGG")
    plt.figure(figsize=(6, 4))
    plt.bar(kinds_num, amount, align="edge", width=-0.3, color="yellow", label="部門別新規就農者数")
    plt.bar(kinds_num, amount, align="edge", width=0.3, color="red", label="新規参入者数")
    plt.title("部門別新規就農者数（令和４年）")
    plt.xlabel(kinds)
    plt.xticks(fontsize=8)
    plt.legend()
    graph2 = Output_Graph()
    return graph, graph2

def Crop_Condition_Graph(term):
    url = "https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040000680&fileKind=0"
    terms = int(term)
    # url += '&download=1'
    #  , engine='openpyxl'
    # 出典：政府統計の総合窓口(e-Stat)農業・食料関連産業の経済計算 / 作況調査(水陸稲、麦類、豆類、かんしょ、飼料作物、工芸農作物) / 収穫量累年統計 / 水稲 / 全国(明治16年～令和3年)（https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040000680&fileKind=0）
    # 「作物統計調査」（農林水産省）を加工して作成
    resp = requests.get(url)
    df = pd.read_excel(BytesIO(resp.content)) 
    # df["t"].astype(float)
    age = df.iloc[-terms:, 0].tolist()
    planting_area = df.iloc[-terms: , 1].tolist()
    harvest_amount = df.iloc[-terms: , 3].tolist()
    for i in range(terms):
        age[i] = age[i].split("(")[0]
        harvest_amount[i] = harvest_amount[i] / 1000000
        planting_area[i] = planting_area[i] / 1000000
    age = tategaki(age)
    
    plt.switch_backend("AGG")
    plt.figure(figsize=(6, 4))
    plt.bar(age, harvest_amount, align="edge", width=-0.3, color="orange", label="平年収量（百万t）")
    plt.bar(age, planting_area, align="edge", width=0.3, color="lightgreen", label="作付面積（百万ha）")
    plt.title(f"お米の平年収量（過去{terms}年分）")
    plt.xticks(fontsize=8)
    plt.legend()
    plt.tight_layout()
    graph = Output_Graph()
    return graph

def tategaki(labels):
    new_labels = []
    for n in labels:
        na = n.split(".")
        n2 = na[0] + '\n' + na[1] + '\n' + "年"
        new_labels.append(n2)
    return new_labels

