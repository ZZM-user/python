import re
import os
import time
import requests


# todo [最终效果]  用户输入获取的页数  [完成]
#                 程序模拟浏览器翻页  [完成]
#                 获取所有主图的链接和标题  [完成]
#                 通过主图的链接来获取大图的链接  [完成]
#                 通过大图链接来下载高清图  [完成]
#                 告知用户 图片总页数  [完成]
#                 告知用户 爬取图片的数量  [完成]
#                 真正的从第一页开始 [完成]
#                 多线程 节约用时


# 获取总页数
def get_counts():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
        "Referer": "http://pic.netbian.com/index_2.html"
    }
    url = "http://pic.netbian.com/4kmeinv/index.html"
    html = requests.get(url, headers=headers)
    html.encoding = 'gbk'
    # print(html.text)
    counts = re.findall(
        r'<span class="slh">…</span><a href="/4kmeinv/index_.*.html">(.*?)</a><a href="/4kmeinv/index_.*.html">下一页</a></div>',
        html.text)

    counts = ''.join(counts)
    return counts


# 获取图的主链接和标题
def get_html(page):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
        "Referer": "http://pic.netbian.com/4kmeinv/index.html"
    }
    if page == 1:
        url = "http://pic.netbian.com/4kmeinv/index.html"
    else:
        url = "http://pic.netbian.com/4kmeinv/index_" + str(page) + ".html"
    html = requests.get(url, headers=headers)
    html.encoding = 'gbk'
    # print(html.text)
    mainLink_list = re.findall(r'<a href="(/tupian/.*?.html)"\starget="_blank">', html.text)

    global titile_list
    titile_list = re.findall(r'<img src="/uploads/allimg/.*?.jpg" alt=".*?" /><b>(.*?)</b>', html.text)

    # 格式化链接
    for i in range(len(mainLink_list)):
        mainLink_list[i] = 'http://pic.netbian.com' + str(mainLink_list[i])
    return mainLink_list


# 通过主链接来获取大图的链接
def get_mainImage(link):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'
    }
    html = requests.get(link, headers=headers)
    html.encoding = 'gbk'
    # print(html.text)
    img_list = re.findall(r'<img src="(/uploads/allimg/.*?.jpg)" data-pic', html.text)

    # 格式化链接
    for i in range(len(img_list)):
        img_list[i] = 'http://pic.netbian.com' + str(img_list[i])
    return img_list


# 创建目录(如果设置相对路径会报错，第一次创建目录，报错，第二次则会运行成功)
def mkdir(path):
    isExists = os.path.exists(os.path.join("D:/", path))
    if not isExists:
        print('创建目录', path)
        os.makedirs(os.path.join("D:/", path))
        os.chdir(os.path.join("D:/", path))
        return True
    else:
        print(path, '已存在')
        return False


def save_img(url, titile):
    # 传过来的url参数是str，无法使用.content
    try:
        url = requests.get(url)
        url.encoding = 'gbk'
    except requests.exceptions.MissingSchema:
        pass

    filename = titile + ".jpg"
    while True:
        try:
            with open(r"D://meizi爬图" + r'//' + filename, 'wb') as f:
                try:
                    f.write(url.content)
                except Exception:
                    pass
                finally:
                    break
        except OSError:  # 可能会遇到一些怪怪的名字，会出现错误（如：titile带删除线）
            with open(r"D://meizi爬图" + r'//' + "Error", 'wb') as f:
                try:
                    f.write(url.content)
                except Exception:
                    pass
                finally:
                    break


def main():
    counts = get_counts()
    mkdir("meizi爬图")
    number = 0

    page_count = int(input("请输入需要下载图片的总页数(共{}页)：".format(counts)))
    start = time.perf_counter()

    for page in range(1, page_count + 1):  # 翻页
        print("----------------------------第{}页----------------------------".format(page))
        page_list = get_html(page)  # 获取主链接
        for i in range(len(page_list)):  # 遍历主链接
            download_img = get_mainImage(page_list[i])  # 获取大图链接
            # download_list = page_list[i]  # 测试主链接
            # print(download_list)
            if download_img is None:
                pass
            else:
                download_img = ''.join(download_img)
                save_img(download_img, titile_list[i])  # 保存

                number += 1
                print(str(number) + ".\t" + titile_list[i] + '\t' + download_img)

    end = time.perf_counter() - start
    print("\n共采集图片{}张".format(number))
    print("总用时：" + str(end) + "s\t\t约等于" + str(end / 60)[:4] + "min")
    print("图片存储路径：D://mazi爬图")


if __name__ == '__main__':
    main()
