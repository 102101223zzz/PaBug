import os
import time
import tkinter
import random
from tkinter import CENTER, RAISED
import tkinter as tk

import define as define
import requests
import tkinter
from bs4 import BeautifulSoup
import pandas as pd
import urllib.parse
from tkinter import ttk
from numpy import var
from pandas.io import json
#firstPath为自己电脑路径，需要自己修改
firstPath="C:\\Users\\zzz\\Desktop\\"
head = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.76",
        "Cookie": "__client_id=9430df4cf308562ea67f2b0c9dbd024e30e9aee8; _uid=740874; C3VK=bca6d2"}
luogu_path1 = "https://www.luogu.com.cn/problem/list?"
diffi = ["暂无评定","入门","普及-","普及和提高-","普及+和提高","提高+和省选-","省选和NOI-","NOI和NOI+和CTSC"]
tiku_tag = ["B%7CP","P","B","CF","SP","AT","UVA"]
tiku_name = ["洛谷","主题库","入门与考试","CodeForces","SPOJ","AtCoder" ,"UVA"]
def findByChoose(diff,keyword,tiku,window):
    print(diff,keyword,tiku)
    difficulty = 0
    type =""
    for i in range(0,8):
        if diff == diffi[i]:
            difficulty = i
          #  print(difficulty)
    for i in range(0,7):
        if str(tiku) == tiku_name[i]:
            type = tiku_tag[i]
          #  print(type)
    secondPath = str(diff)
   # print("diff ="+diff)
    if len(keyword)== 0:
        print("yse")
        Kw=""
        reseponse = requests.get(f"https://www.luogu.com.cn/problem/list?difficulty=" + str(difficulty) + "&type=" + str(type) + "&page=1",headers=head)
    else :
        # 判断keyword中有多少个关键字，每个关键字用"、"隔开,并把关键字放入Kw这个数组中
        Kw = keyword.split("、")
       # print(Kw)
        # 创建一个变量名字为secondPath，值为变量difficulty的值+“-”+数组KW里面每一个关键字，每一个关键字带上序号，例如关键词1、关键词2，每个关键词用“-”号分隔,末尾没有“
        for i in range(0, len(Kw)):
            secondPath = secondPath + str("-") + str(Kw[i]) + str(i)
       # print("no")
        reseponse = requests.get(f"https://www.luogu.com.cn/problem/list?difficulty="+str(difficulty)+"&keyword="+str(keyword)+"&type="+str(type)+"&page=1", headers=head)
    soup = BeautifulSoup(reseponse.text, "html.parser")
    secondPath = secondPath
    #寻找soup中所有的l1标签
    zz = soup.findAll("li")
    os.mkdir(firstPath + secondPath)
    # 遍历soup.findAll函数的返回值
    count=0
    # 进度条的颜色
    color = ["green", "yellow", "red", "blue", "pink", "black"]
    for j in zz:
        # 寻找soup.findAll函数返回值中所有的a标签
        title = j.find("a")
        # 获取a标签中的herf属性
        title_string_1 = title.attrs["href"]
        # 将herf属性中的Pxxx 去掉
        title_string_2 =j.text.replace(str(title_string_1)+' ',"")
      #  print(title_string_1)
       # print(title_string_2)
        #创建一个在C:\Users\zzz\Desktop\pythonzzz文件下名字为变量title_string_1的值+"-"+变量title_string_2的值的文件夹
       # print(firstPath+secondPath+"\\"+str(title_string_1) + "-" + str(title_string_2)+"\\" )
        os.mkdir(firstPath+secondPath+"\\"+str(title_string_1) + "-" + str(title_string_2)+"\\" )
        if title_string_2.find("\/"):
            title_string_2.replace("\/","÷")
        #找到题目
        findProblem(title_string_1, title_string_2,secondPath)
        #找到题目的题解
        findSolution(title_string_1, title_string_2,secondPath)
        count+=1
        # 用tkinter画一个能够实时显示进度的进度条，其进度为当前的count/50的长度
        # 创建一个画布
        canvas = tkinter.Canvas(window, bg="white", width=400, height=70, relief=RAISED, bd=2)
        #创造一个标签，用于提示信息”正在爬取ing“紧贴着进度条，随时显示进度条的进度
        canvas.create_text(200, 40, text="正在爬取ing，当前进度为"+str(count) + "/"+str(len(zz)), font=("Arial", 10))
        #显示当前的文件名
        canvas.create_text(150, 55, text="当前题目为:" + str(title_string_1)+str(title_string_2), font=("Arial", 10))
        # 画出进度条
        canvas.create_rectangle(0, 0, count * 8*50/len(zz), 30, fill=color[random.randint(0, 5)])
        # 显示进度条
        # 让进度条显示在屏幕中央
        canvas.place(x=470, y=400, anchor=CENTER)
        # 让进度条实时显示
        canvas.update()
        # 销毁进度条
        canvas.destroy()
    canvas = tkinter.Canvas(window, bg="white", width=400, height=50, relief=RAISED, bd=2)
    # 创造一个标签，用于提示信息”正在爬取ing“紧贴着进度条
    canvas.create_text(200, 40, text="爬取成功！快说谢谢猿神", font=("Arial", 20))
    canvas.place(x=470, y=400, anchor=CENTER)


def changeToMd(tim):
    # 将tim的内容转为markdown格式
    tim = tim.replace("<article>", "")
    tim = tim.replace("</article>", "")
    tim = tim.replace("<p>", "")
    tim = tim.replace("</p>", "")
    tim = tim.replace("<br/>", "")
    tim = tim.replace("<br>", "")
    tim = tim.replace("<br />", "")
    tim = tim.replace("<ul>", "")
    tim = tim.replace("</ul>", "")
    tim = tim.replace("<li>", "")
    tim = tim.replace("</li>", "")
    tim = tim.replace("<strong>", "**")
    tim = tim.replace("</strong>", "**")
    tim = tim.replace("<em>", "*")
    tim = tim.replace("</em>", "*")
    tim = tim.replace("<code>", "`")
    tim = tim.replace("</code>", "`")
    tim = tim.replace("<pre>", "```")
    tim = tim.replace("</pre>", "```")
    tim = tim.replace("<h1>", "# ")
    tim = tim.replace("</h1>", "")
    tim = tim.replace("<h2>", "## ")
    tim = tim.replace("</h2>", "")
    tim = tim.replace("<h3>", "### ")
    tim = tim.replace("</h3>", "")
    tim = tim.replace("<h4>", "#### ")
    tim = tim.replace("</h4>", "")
    tim = tim.replace("<h5>", "##### ")
    tim = tim.replace("</h5>", "")
    tim = tim.replace("<h6>", "###### ")
    tim = tim.replace("</h6>", "")
    tim = tim.replace("<div>", "")
    tim = tim.replace("</div>", "")
    tim = tim.replace("<span>", "")
    tim = tim.replace("</span>", "")
    tim = tim.replace("<a>", "")
    tim = tim.replace("</a>", "")
    tim = tim.replace("<img>", "")
    tim = tim.replace("</img>", "")
    tim = tim.replace("<blockquote>", ">")
    tim = tim.replace("</blockquote>", "")
    tim = tim.replace("<table>", "")
    tim = tim.replace("</table>", "")
    tim = tim.replace("<thead>", "")
    tim = tim.replace("</thead>", "")
    tim = tim.replace("<tbody>", "")
    tim = tim.replace("</tbody>", "")
    tim = tim.replace("<tr>", "")
    tim = tim.replace("</tr>", "")
    tim = tim.replace("<td>", "")
    tim = tim.replace("</td>", "")
    tim = tim.replace("\\","")
    tim = tim.replace("$","")
    return tim
def findProblem(title_string_1, title_string_2,secondPath):
    #找到问题的题解并且保存入文件
    reseponse = requests.get(f"https://www.luogu.com.cn/problem/"+str(title_string_1), headers=head)
    soup = BeautifulSoup(reseponse.text, "html.parser")
    tim = str(soup.find("article"))
    tim = changeToMd(tim)
    #将tim保存在firstPath +str(title_string_1) + "-" + str(title_string_2)+"\\"+str(title_string_1) + "-" + str(title_string_2)+".md"中
    with open(firstPath +secondPath+ "\\"+str(title_string_1) + "-" + str(title_string_2) + "\\" + str(title_string_1) + "-" + str(title_string_2) + ".md", "w", encoding="utf-8") as f:
         f.write(tim)
def findSolution(title_string_1,title_string_2,secondPath):
    #找到问题的题解
    reponse = requests.get("https://www.luogu.com.cn/problem/solution/" + str("P1013"), headers=head)
    soup = BeautifulSoup(reponse.text, "html.parser")
    # 将decoded_uri_componet转成Json格式
    decoded_uri_component = str(urllib.parse.unquote(reponse.text, encoding='unicode_escape', errors='replace'))
    result_index = decoded_uri_component.find("content\":\"")
    #去掉多余的符号
    result_index += 10;
    decoded_uri_component = decoded_uri_component[result_index:]
    final_index = decoded_uri_component.find("type")
    # 去掉多余的符号
    final_index -= 6
    decoded_uri_component = decoded_uri_component[:final_index]
    #改成markdown格式
    tij = changeToMd(decoded_uri_component)
    # print(tij)
    # #将decoded_uri_component转为markdown格式,并且存放在C:\Users\zzz\Desktop\pythonzzz文件下名字为P1000-超级玛丽游戏的文件中，命名为P1000-超级玛丽游戏-题解.md
    with open(firstPath + secondPath +"\\"+ str(title_string_1) + "-" + str(title_string_2) + "\\" + str(
            title_string_1) + "-" + str(title_string_2) + "-题解.md", "w", encoding="utf-8") as f:
            f.write(tij)
def CreateWindows():
    #用tkinter创建一个尺寸占屏幕十分之一，且位于中间的窗口,名字为PaBug
    window = tk.Tk()
    window.title("PaBug")
    window.geometry("949x560")
    image= tkinter.PhotoImage(file="./yuan.png")
    label_qid=tkinter.Label(window, image=image)
    label_qid.place(width=949,height=560)
    button1 = tkinter.Button(window, text="启动",image=image,compound=CENTER,command=CreateWindows2)
    button1.place(x=465, y=360, width=40, height=40)
    window.mainloop()
def CreateWindows2():
    window1 = tk.Tk()
    window1.withdraw()
    window1 = tk.Toplevel()
    window1.title("PaBug")
    window1.iconbitmap("woc猿.ico")
    window1.geometry("949x560")
    # 用 ComboBox 创建一个下拉列表 列表值为"暂无评定","入门","普及-","普及/提高-","普及+/提高","提高+/省选-","省选/NOI-","NOI/NOI+/CTSC"，默认值为"暂无评定"，选中后值会传递给 var
    Diff = tkinter.StringVar()
    Diff.set("暂无评定")
    label1=tkinter.Label(window1, text='所选题库',font=('华文彩云', 20), fg='red')
    label1.grid(row=1,column=0)
    #在第一排第二到第8列创造8个按钮，名字分别为tiku_name里面的内容，每次只能选择一个按钮，并把按钮的值传递给tiku
    TiKu= tkinter.StringVar()
    TiKu.set("洛谷")
    for i in range(1, 8):
            button = tkinter.Radiobutton(window1, text=tiku_name[i - 1], variable=TiKu,value= tiku_name[i - 1],relief=RAISED)
            button.grid(row=1, column=i+4)
    # 在第二排第一列创造一个标签，内容为筛选条件
    label2 = tkinter.Label(window1, text='筛选条件', font=('华文彩云', 20), fg='red')
    label2.grid(row=2, column=0)
    combobox = tkinter.ttk.Combobox(window1, textvariable=Diff, values=(
    "暂无评定", "入门", "普及-", "普及和提高-", "普及+和提高", "提高+和省选-", "省选和NOI-", "NOI和NOI+和CTSC"))
    combobox.grid(row=2, column=2)
    # 在第二排第四列创造一个输入框，输入的内容为关键字，并把输入的值存入keywd中第二排第三列要有一个提示标签，内容为请输入关键字
    KeyWd = tkinter.StringVar()
    KeyWd.set("")
    label3 = tkinter.Label(window1, text='请输入关键字',fg='red', font=('华文彩云', 20))
    label3.grid(row=3, column=0)
    entry = tkinter.Entry(window1, textvariable=KeyWd)
    entry.grid(row=3, column=2)
    image2 = tkinter.PhotoImage(file="./woc猿.ico")
    label3 = tkinter.Label(window1, text='求助下猿神吧--》', fg='red', font=('华文彩云', 20))
    label3.grid(row=5, column=0)
    # 在第三排第二列创造一个按钮，名字为搜索，点击后执行search函数
    button2 = tkinter.Button(window1, text="启动", image=image2,command=lambda:findByChoose(Diff.get(),KeyWd.get(),TiKu.get(),window1))
    button2.grid(row=5, column=5)
    window1.mainloop()
if __name__ == '__main__':
    CreateWindows()
   #判断keyword是否为空
  # findSolution("P1004","[NOIP2000 提高组] 方格取数","4")

  # print(decoded_uri_component[result_index:])
   # 查找"type"之前的内容的索引位置
