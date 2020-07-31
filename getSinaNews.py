import re
import time
import requests
# url编码和解码
from urllib import parse


def get_text(url):
    resp = requests.get(url)
    hot_list = re.findall(r'([ep]"\starget=".*">.*[\u4e00-\u9fa5])', resp.text)
    return hot_list

def get_heat(url):
    resp = requests.get(url)
    heat_list = re.findall(r'<span>.*?\d*', resp.text)
    return heat_list

def Search():
    try:
        decision = int(input("\n是否使用关键词搜索功能(1 or 0)："))
        if decision == 1:
            char = input("请输入微博搜索关键词：")
            print('已获取链接：' + 'https://s.weibo.com/weibo?q=%23' + parse.quote(char) + '&Refer=top')
        elif decision == 0:
            print("程序结束")
        else:
            print("不正确输入")
    except ValueError as result:
        print("只能输入0和1")
    except Exception:
        pass

def main(url):
    hot_list = get_text(url)    # 获取热闻
    heat_list=get_heat(url)     # 获取热闻热度
    hot_line_list = []
    print("------------------微博实时热搜TOP50------------------")
    for i in range(hot_list.__len__()):
        # 获取'>'符号位置
        index1 = hot_list[i].index('>')
        index2 = heat_list[i].index('>')
        # 截取多余内容
        hot_list[i] = hot_list[i][index1+1:]    # 热闻
        heat_list[i] = heat_list[i][index2 + 1:]    # 热度

        # parse.quote(hot_list[i]) 对hot_list[i]进行编码操作
        hot_line_list.append('https://s.weibo.com/weibo?q=%23' + parse.quote(hot_list[i]) + '&Refer=top')

        print("[" + format(i + 1) + "]：" + hot_list[i] +'['+heat_list[i]+']'+ '\n\t\t\t' + hot_line_list[i])
    Search()


if __name__ == '__main__':
    # 微博热搜TOP50
    url = 'https://s.weibo.com/top/summary?Refer=top_hot&topnav=1&wvr=6'
    main(url)
    print('\n当前时间：' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    print("\t\t\t\t————来源于-微博实时热搜-")
