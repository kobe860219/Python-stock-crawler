import tkinter as tk
import requests
from io import StringIO
import pandas as pd
import numpy as np
import datetime
import time
import tkinter.messagebox
import json
import csv
import datetime
from tkinter import *
import pickle

#新增一個視窗
window = tk.Tk()
#標題
window.title('ACS104118')
#大小
window.geometry('1000x1000')
#第一個標籤+掛上
l = tk.Label(window, text='ACS104118', bg='green', font=('Arial', 12), width=30, height=2,)
l.pack() 

#新增畫布
canvas = tk.Canvas(window, bg='green', height=250, width=500)
x0, y0, x1, y1 = 100, 100, 150, 150 #定義多邊形的基本參數
line = canvas.create_line(x0-50, y0-50, x1-50, y1-50)                   # 畫直線
oval = canvas.create_oval(x0+120, y0+50, x1+120, y1+50, fill='yellow')  # 畫黃色圓形
arc = canvas.create_arc(x0, y0+50, x1, y1+50, start=0, extent=180)      # 畫180度的善行
rect = canvas.create_rectangle(330, 30, 330+20, 30+20)                  # 畫正方形
canvas.pack(side='right')
#移動圖形(正方形)
def moveit():
    canvas.move(rect, 2, 2) # 按每次（x=2, y=2）移動
 
# 定義一個按鈕來移動正方形
b7 = tk.Button(window, text='move item',command=moveit).pack(side='right')


#listbox的部分-顯示
var1 = tk.StringVar()  # 選擇的
l1 = tk.Label(window, bg='green', fg='yellow',font=('Arial', 12), width=10, textvariable=var1)
l1.pack(side='left')
 
# 顯示選擇
def print_selection():
    value = lb.get(lb.curselection())   # 選中的
    var1.set(value)  # 設定var1
 
# print_selection的按鈕
b1 = tk.Button(window, text='print selection', width=15, height=2, command=print_selection)
b1.pack(side='left')
 
# 選擇有哪些
var2 = tk.StringVar()
var2.set(('台積電','台泥','鴻海')) # 可選的
# 創建Listbox放選擇
lb = tk.Listbox(window, listvariable=var2)  #設定
lb.pack(side='left')

#登入系統-------------------------------------------------------------------------------

#使用者資訊的標籤
tk.Label(window, text='User name:', font=('Arial', 14)).place(x=10, y=170)
tk.Label(window, text='Password:', font=('Arial', 14)).place(x=10, y=210)

#輸入框-帳號
var_usr_name = tk.StringVar()
var_usr_name.set('StudentID')
entry_usr_name = tk.Entry(window, textvariable=var_usr_name, font=('Arial', 14))
entry_usr_name.place(x=120,y=175)
#輸入框-密碼
var_usr_pwd = tk.StringVar()
entry_usr_pwd = tk.Entry(window, textvariable=var_usr_pwd, font=('Arial', 14), show='*')
entry_usr_pwd.place(x=120,y=215)

def usr_login():
    # 獲得使用者輸入的usr_name和usr_pwd
    usr_name = var_usr_name.get()
    usr_pwd = var_usr_pwd.get()

    # 將輸入和文件裡的資料比對
    try:
        with open('usrs_info.pickle', 'rb') as usr_file:
            usrs_info = pickle.load(usr_file)
    except FileNotFoundError:
        # 沒有`usr_file`的時候，建立一個`usr_file`這個文件，並將管理員的使用者和密碼寫入，即使用者名稱為`admin`密碼為`admin`。
        with open('usrs_info.pickle', 'wb') as usr_file:
            usrs_info = {'admin': 'admin'}
            pickle.dump(usrs_info, usr_file)
            usr_file.close()    # 必須先關閉，否則pickle.load()會出現EOFError

    # 使用者名稱和密碼與文件中的比對成功，則會登入成功，並跳出彈窗how are you? 加上你的使用者名稱。
    if usr_name in usrs_info:
        if usr_pwd == usrs_info[usr_name]:
            tkinter.messagebox.showinfo(title='Welcome', message='How are you? ' + usr_name)
			
        # 如果使用者名稱匹配成功，而密碼輸入錯誤，則會彈出'Error, your password is wrong, try again.'
        else:
            tkinter.messagebox.showerror(message='Error, your password is wrong, try again.')
    else:  # 如果發現使用者名稱不存在
        is_sign_up = tkinter.messagebox.askyesno('Welcome！ ', 'You have not sign up yet. Sign up now?')
        # 提示需不需要註冊新使用者
        if is_sign_up:
            usr_sign_up()

#定義使用者註冊功能
def usr_sign_up():
    def sign_to_ACS104118_Website():
        # 獲取註冊時所輸入的資訊
        np = new_pwd.get()
        npf = new_pwd_confirm.get()
        nn = new_name.get()

        # 開啟記錄資料的文件，將註冊資料讀出
        with open('usrs_info.pickle', 'rb') as usr_file:
            exist_usr_info = pickle.load(usr_file)
        # 兩次密碼輸入不一致
        if np != npf:
            tkinter.messagebox.showerror('Error', 'Password and confirm password must be the same!')
        # 使用者名稱已經在我們的資料文件中
        elif nn in exist_usr_info:
            tkinter.messagebox.showerror('Error', 'The user has already signed up!')

        # 最後如果輸入無以上錯誤，則將註冊輸入的資訊記錄到文件當中，並提示註冊成功
        else:
            exist_usr_info[nn] = np
            with open('usrs_info.pickle', 'wb') as usr_file:
                pickle.dump(exist_usr_info, usr_file)
            tkinter.messagebox.showinfo('Welcome', 'You have successfully signed up!')
            # 然後銷燬視窗。
            window_sign_up.destroy()

    # 定義長在視窗上的視窗
    window_sign_up = tk.Toplevel(window)
    window_sign_up.geometry('300x200')
    window_sign_up.title('Sign up window')

    new_name = tk.StringVar()  # 將輸入的註冊名給變數
    new_name.set('StudentID')  # 將最初顯示定為'StudentID'
    tk.Label(window_sign_up, text='User name: ').place(x=10, y=10)  # 將`User name:`放置在座標（10,10）。
    entry_new_name = tk.Entry(window_sign_up, textvariable=new_name)  # 建立一個註冊名的`entry`，變數為`new_name`
    entry_new_name.place(x=130, y=10)  # `entry`放置在座標（130,10）.
	
	#密碼同上面帳號
    new_pwd = tk.StringVar()
    tk.Label(window_sign_up, text='Password: ').place(x=10, y=50)
    entry_usr_pwd = tk.Entry(window_sign_up, textvariable=new_pwd, show='*')
    entry_usr_pwd.place(x=130, y=50)
	
	#確認密碼
    new_pwd_confirm = tk.StringVar()
    tk.Label(window_sign_up, text='Confirm password: ').place(x=10, y=90)
    entry_usr_pwd_confirm = tk.Entry(window_sign_up, textvariable=new_pwd_confirm, show='*')
    entry_usr_pwd_confirm.place(x=130, y=90)

    # 下面的 sign_to_ACS104118_Website
    btn_comfirm_sign_up = tk.Button(window_sign_up, text='Sign up', command=sign_to_ACS104118_Website)
    btn_comfirm_sign_up.place(x=180, y=120)

#login and sign up 按鈕
btn_login = tk.Button(window, text='Login', command=usr_login)
btn_login.place(x=120, y=240)
btn_sign_up = tk.Button(window, text='Sign up', command=usr_sign_up)
btn_sign_up.place(x=200, y=240)

#上市上櫃股票清單
def get():
	url = requests.get("http://isin.twse.com.tw/isin/C_public.jsp?strMode=2")#requests.get()模擬連到網頁-本國上市上櫃股票清單網站
	df = pd.read_html(url.text)[0] #爬取網頁原始碼
	df.columns = df.iloc[0]#設定columns的名稱
	df = df.iloc[1:]# 刪除第一行
	# 先移除row，再移除column，超過三個NaN則移除(dropna->NAN)
	df = df.dropna(thresh=3, axis=0).dropna(thresh=3, axis=1)
	df = df.set_index('有價證券代號及名稱')#把123456改成代號及名稱
	print(df)#顯示

#每日股價
def download_every_day_price():
	date = '20190116' #先寫死一天，當天還沒開盤完
	r = requests.post('http://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + date + '&type=ALL')#下載盤後資訊

	#爬下來的網頁包含ETF、指數及個股資訊。
	#用r.text可印出爬下來的資料
	#print(r.text())
	#其資料每個欄位是以逗號分隔、而每一筆資料是以\r\n分隔。
	#指數因為沒有開盤價、收盤價、本益比等等的資訊，所以資料長度是三個裡面最短的。
	#而ETF跟個股雖然都有17個欄位，但是ETF的資料開頭多了一個(=)做區隔，
	str_list = []
	for i in r.text.split('\n'):
		if len(i.split('",')) == 17 and i[0] != '=':       
			i = i.strip(",\r\n")
			str_list.append(i)      

	# read_csv( )將資料轉換成dataframe格式。
	df = pd.read_csv(StringIO("\n".join(str_list)))  #join()->把串列透過換行符號合併
	pd.set_option('display.max_rows', None) #後面為限制
	print(df)
	
#本益比小於3	
def lower_3():
	datestr='20190116' #先寫死一天，當天還沒開盤完
# 下載股價，台灣證交所
	r = requests.post('http://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + datestr + '&type=ALL')

# 整理資料，變成表格
	df = pd.read_csv(StringIO("\n".join([i.translate({ord(c): None for c in ' '}) 
                                     for i in r.text.split('\n') 
                                     if len(i.split('",')) == 17 and i[0] != '='])), header=0)
	print(df[pd.to_numeric(df['本益比'], errors='coerce') < 3]) #只印出本益比小於3的

#公關觀測資訊站，月報表->月營收
def monthly_report_1():
	#2019年1月的還沒出來
	year=107
	month=12
	url = 'http://mops.twse.com.tw/nas/t21/sii/t21sc03_'+str(year)+'_'+str(month)+'_0.html'#網站
	
	#偽瀏覽器
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
	
	#載該年月的網站，並用pandas轉換成 dataframe
	r = requests.get(url, headers=headers)
	r.encoding = 'big5'
	html_df = pd.read_html(StringIO(r.text))
	
	# 處理資料
	if html_df[0].shape[0] > 500:
		df = html_df[0].copy()
	else:
		df = pd.concat([df for df in html_df if df.shape[1] <= 11]) #剃除行數錯誤的表格,並將表格合併
	
	#設定表格
	df = df[list(range(0,10))]
	column_index = df.index[(df[0] == '公司代號')][0]
	
	#刪掉重複的欄位
	df.columns = df.iloc[column_index]
	df['當月營收'] = pd.to_numeric(df['當月營收'], 'coerce')
	df = df[~df['當月營收'].isnull()]
	df = df[df['公司代號'] != '合計']
	
	#暫緩
	time.sleep(5)
	print(df)

#三大法人
def big_three():
	date = '20180102'
	r = requests.get('http://www.tse.com.tw/fund/T86?response=csv&date='+date+'&selectType=ALLBUT0999')#
	df = pd.read_csv(StringIO(r.text), header=1).dropna(how='all', axis=1).dropna(how='any')
	print(df)

#爬N天
def n_day():
	#爬一天的，後面重複呼叫，原理與前面的差不多!
	def crawl_price(date):
		r = requests.post('http://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + str(date).split(' ')[0].replace('-','') + '&type=ALL')
		ret = pd.read_csv(StringIO("\n".join([i.translate({ord(c): None for c in ' '}) 
											for i in r.text.split('\n') 
											if len(i.split('",')) == 17 and i[0] != '='])), header=0)
		ret = ret.set_index('證券代號')
		ret['成交金額'] = ret['成交金額'].str.replace(',','')
		ret['成交股數'] = ret['成交股數'].str.replace(',','')
		return ret
	
	#爬9天
	data = {} #要放資料的
	n_days = 9 #要爬幾天
	date = datetime.datetime.now()#取得現在日期
	fail_count = 0 #失敗次數
	allow_continuous_fail_count = 5 #允許的連續失敗次數
	while len(data) < n_days:

		print('parsing', date)
		# 使用 crawPrice 爬資料
		try:
			# 抓資料
			data[date] = crawl_price(date)
			print('success!')
			fail_count = 0
		except:
			# 假日爬不到
			print('fail! Is holiday')
			fail_count += 1
			if fail_count == allow_continuous_fail_count:
				raise
				break
		
		# 減一天
		date -= datetime.timedelta(days=1)
		time.sleep(10)
	
	#整理後只剩收盤價，並會按照日期排
	close = pd.DataFrame({k:d['收盤價'] for k,d in data.items()}).transpose()
	close.index = pd.to_datetime(close.index)
	print(close)

#月報表爬N月
def  monthly_report_n():
	#定義爬一個月的，跟前面原理差不多!
	def monthly_report(year, month):
    
		# 假如是西元，轉成民國
		if year > 1990:
			year -= 1911
		
		url = 'http://mops.twse.com.tw/nas/t21/sii/t21sc03_'+str(year)+'_'+str(month)+'_0.html'
		if year <= 98:
			url = 'http://mops.twse.com.tw/nas/t21/sii/t21sc03_'+str(year)+'_'+str(month)+'.html'
		
		# 偽瀏覽器
		headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
		
		# 下載該年月的網站，並用pandas轉換成 dataframe
		r = requests.get(url, headers=headers)
		r.encoding = 'big5'
		html_df = pd.read_html(StringIO(r.text))
		
		# 處理一下資料
		if html_df[0].shape[0] > 500:
			df = html_df[0].copy()
		else:
			df = pd.concat([df for df in html_df if df.shape[1] <= 11])
		df = df[list(range(0,10))]
		column_index = df.index[(df[0] == '公司代號')][0]
		df.columns = df.iloc[column_index]
		df['當月營收'] = pd.to_numeric(df['當月營收'], 'coerce')
		df = df[~df['當月營收'].isnull()]
		df = df[df['公司代號'] != '合計']
		# 暫緩
		time.sleep(5)
	
	data = {} #放資料的
	n_days = 12 #爬12個月
	now = datetime.datetime.now() #現在日期

	year = now.year #現在年分
	month = now.month #現在月份
		
	while len(data) < n_days:
    
		print('parsing', year, month)
    
    # 使用 crawPrice 爬資料
		try:
			data['%d-%d-01'%(year, month)] = monthly_report(year, month)
		except Exception as e:
			print('Report not release yet!') #還沒公佈
		
		# 減一個月
		month -= 1
		if month == 0:
			month = 12
			year -= 1

		time.sleep(10)
	
	#以公司代號來放資料
	for k in data.keys():
		data[k].index = data[k]['公司代號']
    
	df = pd.DataFrame({k:df['當月營收'] for k, df in data.items()}).transpose() #只保留當月營收
	df.index = pd.to_datetime(df.index) #用時間當索引
	df = df.sort_index() #排序
	print(df.head())
	
#加法器
label_var = StringVar() #宣告
label_var.set('0') #預設為0

#加法器版面
my_label = Label(window, textvariable = label_var,width = 20, bg = 'yellow') #放和的
my_label.pack()

my_label1 = Label(window,text = '請輸入第一個數字') #第一個數字
my_label1.pack()

my_enter1 = Entry(window, width = 20) #輸入1
my_enter1.pack()

my_label2 = Label(window, text = '請輸入第二個數字') #第二個數字
my_label2.pack()

my_enter2 = Entry(window, width = 20) #輸入2
my_enter2.pack()

# 新增一個 Button 的 command 的處理函數
def add():
	label_var.set(int(my_enter1.get()) + int(my_enter2.get()))#加總
	
#按鈕
#每日價格的
b1 = tk.Button(window, text='每日價格',bg='yellow', font=('Arial', 12), width=50, height=1, command=download_every_day_price)
b1.pack(side='bottom')

#本益比小於3
b2 = tk.Button(window, text='本益比小於3的股', font=('Arial', 12), width=50, height=1,bg='green' ,command=lower_3)
b2.pack(side='bottom')

#月報表
b3 = tk.Button(window, text='月報表', font=('Arial', 12), width=50, height=1,bg='blue' ,command=monthly_report_1)
b3.pack(side='bottom')

#加法器的加
b4 = tk.Button(window, text='加', font=('Arial', 12), width=30, height=1,bg='red' ,command=add)
b4.pack()

#股票清單
b5 = tk.Button(window, text='上市上櫃股票清單', font=('Arial', 12), width=100, height=1,bg='red' ,command=get)
b5.pack(side='bottom')

#三大法人
b6 = tk.Button(window, text='三大法人', font=('Arial', 12), width=100, height=1,bg='yellow' ,command=big_three)
b6.pack(side='bottom')

#爬N天
b7 = tk.Button(window, text='爬N天', font=('Arial', 12), width=100, height=1,bg='yellow' ,command=n_day)
b7.pack(side='bottom')

#爬N月
b8 = tk.Button(window, text='爬N月', font=('Arial', 12), width=100, height=1,bg='yellow' ,command=monthly_report_n)
b8.pack(side='bottom')


#-------------------------上面選單--------------------------------
#do的次數設定
counter = 0
def do_job():
    global counter
    l.config(text='do '+ str(counter))
    counter += 1

# 建立一個視窗上方的選單欄
menubar = tk.Menu(window)

# 建立一個File選單
filemenu = tk.Menu(menubar, tearoff=0)#（預設不下拉)
# 定義的空選單名為File，放在選單欄中
menubar.add_cascade(label='File', menu=filemenu)

# 在File中加入New、Open、Save等小選單，即下拉選單，每一個小選單對應命令操作。
filemenu.add_command(label='New', command=do_job)
filemenu.add_command(label='Open', command=do_job)
filemenu.add_command(label='Save', command=do_job)
filemenu.add_separator()#新增一條分隔線
filemenu.add_command(label='Exit', command=window.quit) # tkinter裡面自帶quit()函式

# 建立一個Edit選單項（預設不下拉，下拉內容包括Cut，Copy，Paste功能項）
editmenu = tk.Menu(menubar, tearoff=0)
# 定義空選單命名為 Edit，放在選單欄中
menubar.add_cascade(label='Edit', menu=editmenu)

#  Edit 中加入Cut、Copy、Paste等小命令功能單元，觸發do_job的功能
editmenu.add_command(label='Cut', command=do_job)
editmenu.add_command(label='Copy', command=do_job)
editmenu.add_command(label='Paste', command=do_job)

# 建立第二級選單，即選單項裡面的選單
submenu = tk.Menu(filemenu) # 和上面定義選單一樣，但這是在File上建立另一個空的選單
filemenu.add_cascade(label='Import', menu=submenu, underline=0) # 給放入的選單submenu命名為Import

# 建立第三級選單命令，即選單項裡面的選單項裡面的選單命令
submenu.add_command(label='Submenu_1', command=do_job)   # 在Import選單項中加入一個小選單命令Submenu_1

# 建立選單欄完成後，配置讓選單欄menubar顯示出來
window.config(menu=menubar)	

window.mainloop()