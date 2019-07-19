import requests
import re
import time


def get_str(url_s):

    url = 'http://www.pythonchallenge.com/pc/def/%s.html' % url_s
    res = requests.get(url).text
    # print(res)
    text = re.findall('.*<!--(.*)-->', res, re.S)
    # list转为str便于遍历字符
    return ''.join(text)


if __name__ == "__main__":
    # s = get_str('equality').replace('\n', '')
    # # s = 'ABCaABCsdAA'
    # return_s = ''
    # for i in range(4, len(s)-4):
    #
    #     if 'z' >= s[i] >= 'a' and s[i-3:i].upper() == s[i-3:i] and s[i+1: i + 4].upper() == s[i+1: i + 4] and 'z' >= s[i-4] >= 'a' and 'z' >= s[i+4] >= 'a':
    #         return_s += s[i]
    #
    # print(return_s)
    # num = 74595
    # while num:
    #     url = 'http://www.pythonchallenge.com/pc/def/linkedlist.php?nothing=%s' % num
    #     res = requests.get(url).text
    #     print(res)
    #     num = res.split(' ')[-1]
    #     print(url)
    #     time.sleep(1)
    import pickle
    ret_s = ''
    with open('banner.p', 'rb') as f:

        for l in pickle.load(f):
            for i in l:
                ret_s += i[0] * i[1]
            ret_s += '\n'

    print(ret_s)




