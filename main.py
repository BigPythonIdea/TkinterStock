import tkinter as tk
import pandas as pd
from bs4 import BeautifulSoup
import requests
import twstock

# 股票main

# 基本設定
window = tk.Tk()
window.geometry('640x480')
window.title('股票盤後查看')
input_fm = tk.Frame(window, width=640, height=120)
input_fm.pack()
lb = tk.Label(input_fm, bg='#36688D', fg='white', text="請輸入股票代號",
              font=('微軟正黑體', 12),width=640, height=120)
lb.place(rely=0.25, relx=0.5, anchor='center')

# 取得Url的框框
stock_url = tk.StringVar()
entry = tk.Entry(input_fm, textvariable=stock_url, width=50)
entry.place(rely=0.5, relx=0.5, anchor='center')

# 按鈕事件
def click_func():
    def get_setting():
        res = []
        try:
            pds = pd.read_csv('stock_number.csv')
            s = pds["股票代號"].tolist()
            for i in s:
                res.append(i)
        except:
            print('load error')
        return res

    def get_price(stockid):
        price = ""
        try:
            res = requests.get("https://invest.cnyes.com/twstock/TWS/" + str(stockid))
            soup = BeautifulSoup(res.text, "html.parser")
            finds = soup.find("div", class_="jsx-2941083017 info-lp")
            price = finds.text
        except:
            print("connect get_price error!")

        return price

    def get_best(stockid):
        stock = twstock.Stock(str(stockid))
        bp = twstock.BestFourPoint(stock).best_four_point()
        if (bp):
            return (str(stockid), '買進' if bp[0] else '賣出', bp[1])
        else:
            return (False, False)

    stock = get_setting()
    stock2 = get_setting()

    for i in stock:
        get_price(i)

    for i in stock2:
        listbox.insert(0, get_best(i))


btn = tk.Button(input_fm, text='查詢', command=click_func,
                bg='#F18904', fg='Black', font=('微軟正黑體', 10))
btn.place(rely=0.5, relx=0.85, anchor='center')

# 清單區域
dload_fm = tk.Frame(window, width=640, height=480-120)
dload_fm.pack()

# lable
lb = tk.Label(dload_fm, text="查詢結果", fg='black', font=('微軟正黑體', 10),
              width=640, height=120)
lb.place(rely=0.25, relx=0.5, anchor='center')

# listlabel
listbox = tk.Listbox(dload_fm, width=65, height=15)
listbox.place(rely=0.5, relx=0.5, anchor='center')


# Scrollbar
sbar = tk.Scrollbar(dload_fm)
sbar.place(rely=0.5, relx=0.87, anchor='center', relheight=0.7)

# Scrollbar cross List
listbox.config(yscrollcommand=sbar.set)
sbar.config(command=listbox.yview)

window.mainloop()



# lb.pack()
# window.mainloop()
