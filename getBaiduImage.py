import re
import os
import json
import time
import urllib
import random
import requests
# 用于随机获取User_Agent
from fake_useragent import UserAgent


# 获取存放json数据的url地址，key_word即是输入的值，page为获得的url地址的个数
def get_urlset(key_word, page):
    url_list = []
    kw = urllib.parse.quote(key_word)
    for j in range(page):
        p = j * 30
        url_list.append(
            "https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=" + kw + "&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&hd=&latest=&copyright=&word=" + kw + "&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&expermode=&force=&pn=" + str(
                p) + "&rn=30&gsm=b4")
    return url_list


# 获取IP伪装
def get_fake_IP():
    ip_page = requests.get(  # 获取200条IP
        'http://www.89ip.cn/tqdl.html?num=60&address=&kill_address=&port=&kill_port=&isp=')
    proxies_list = re.findall(
        r'(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)(:-?[1-9]\d*)',
        ip_page.text)

    # 转换proxies_list的元素为list,最初为'tuple'元组格式
    proxies_list = list(map(list, proxies_list))

    # 格式化ip  ('112', '111', '217', '188', ':9999')  --->  112.111.217.188:9999
    for u in range(0, len(proxies_list)):
        # 通过小数点来连接为字符
        proxies_list[u] = '.'.join(proxies_list[u])
        # 用rindex()查找最后一个小数点的位置，
        index = proxies_list[u].rindex('.')
        # 将元素转换为list格式
        proxies_list[u] = list(proxies_list[u])
        # 修改位置为index的字符为空白（去除最后一个小数点）
        proxies_list[u][index] = ''
        # 重新通过空白符连接为字符
        proxies_list[u] = ''.join(proxies_list[u])

    # proxies = {'协议':'协议://IP:端口号'}
    # 'https':'https://59.172.27.6:38380'
    # IP伪装
    return "'" + random.choice(proxies_list) + "'"


# 获取随机User_Agent伪装
def get_fake_User_Agent():
    # 随机获取User_Agent
    ua = UserAgent()
    user_anget = ua.random
    return user_anget


# 解析网址
def get_html(url):
    headers = {
        'User-Agent': get_fake_User_Agent()
    }
    proxies = {'http': get_fake_IP()}
    try:
        resp = requests.get(url, headers=headers)
    except:
        resp = requests.get(url, headers=headers, proxies=proxies)
    return resp


# 解析json获得图片地址
def parse_json(text):
    img_url = []
    try:  # 多用用try，防止加载失败，程序退出
        result = json.loads(text)
        if result:
            for i in result.get("data"):
                img_url.append(i.get("hoverURL"))
        return img_url
    except:
        print("获取图片地址失败")


# 创建目录(如果设置相对路径会报错，第一次创建目录，报错，第二次则会运行成功)
def mkdir(path):
    # os.path.exists(name)判断是否存在路径
    # os.path.join(path, name)连接目录与文件名
    isExists = os.path.exists(os.path.join("D:/百度爬图", path))
    if not isExists:
        print('子目录', path)
        os.makedirs(os.path.join("D:/百度爬图", path))
        os.chdir(os.path.join("D:/百度爬图", path))
        return True
    else:
        print(path, '已存在')
        return False


# 打开并保存图片到文件中
def open_img(img, number):
    if img:
        filename = key_word + '-' + str(number + 1) + ".jpg"
        with open(r"D:/百度爬图/" + key_word + r'/' + filename, 'wb') as f:
            try:
                f.write(get_html(img).content)
                print(filename + "下载成功")
            except:
                print("读取文件失败")


# 主函数
def main(keyword, page):
    mkdir(keyword)
    urlset = get_urlset(keyword, page)
    number = 0  # 用来计数
    for url in urlset:
        Text = get_html(url).text
        img_url = parse_json(Text)
        if img_url:
            for img in img_url:
                open_img(img, number)
                number += 1


if __name__ == '__main__':
    # 计时
    start = time.time()
    key_word = input("请输入搜索关键字：")
    page = int(input("请输入你要爬取的页数:"))
    main(key_word, page)
    print("\n图片存储路径为：" + r"D:/百度爬图/" + key_word + r'/')
    print("用时%.2f" % (time.time() - start) + 's')
