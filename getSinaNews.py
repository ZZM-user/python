import re
import time
import requests
# 对url的编码和解码
from urllib import parse


def get_text(url):
    resp = requests.get(url)
    hot_list = re.findall(r'(k">.*[\u4e00-\u9fa5]).*?', resp.text)
    return hot_list


def Search():
    char = input("请输入微博搜索关键词：")
    print('已获取链接：' + 'https://s.weibo.com/weibo?q=%23' + parse.quote(char) + '&Refer=top')


def main(url):
    hot_list = get_text(url)
    hot_line_list = []
    print("------------------微博实时热搜TOP50------------------")
    for i in range(hot_list.__len__()):
        # 获取'>'符号位置
        index = hot_list[i].index('>')
        # 截取字符串，去除多余内容
        if i >= 50:
            break
        hot_list[i] = hot_list[i][3:]

        # parse.quote(hot_list[i]) 对hot_list[i]进行编码操作
        hot_line_list.append('https://s.weibo.com/weibo?q=%23' + parse.quote(hot_list[i]) + '&Refer=top')

        if "京网文" not in hot_list[i] and "京ICP备" not in hot_list[i]:
            print("[" + format(i + 1) + "]：" + hot_list[i] + '\n\t\t\t' + hot_line_list[i])
    try:
        decision = int(input("\n是否使用关键词搜索功能(1 or 0)："))
        if decision == 1:
            Search()
        elif decision == 0:
            print("程序结束")
        else:
            print("非法输入")
    except ValueError as result:
        print("只能输入0和1")
    except Exception:
        pass


if __name__ == '__main__':
    # 计时
    # start = time.time()
    # 微博热搜TOP50
    url = 'https://s.weibo.com/top/summary?Refer=top_hot&topnav=1&wvr=6'
    main(url)
    print('\n当前时间：' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    print("\t\t\t\t————来源于-微博实时热搜-")
    # print("用时%.2f" % (time.time() - start) + 's')
