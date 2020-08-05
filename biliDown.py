import requests
import re
import pyperclip

def downAndSave(url,header,retry_time=5):
    try:
        if retry_time == 0:
            raise Exception("")
        BV_number = re.findall('BV.{10}', url)[0]
        url_base = 'https://m.bilibili.com/video/'
        url = url_base+BV_number
        res = requests.get(url, headers=header)
        res.encoding = 'utf-8'
        if res.status_code != 200:
            downAndSave(url,header,retry_time-1)
        re1 = 'readyVideoUrl.*?\'(.*?)\\\''
        video_url = re.findall(re1,res.text)[0]

        res_video = requests.get(video_url,headers=header)
        title = re.findall('<title.*?>(.*?)</title>',res.text)[0]
        save_name = legalfySaveName(title+re.findall('BV.{10}',url)[0]+'.mp4')
        with open(save_name, 'wb') as f:
            f.write(res_video.content)
            print("下载成功")
    except:
        if retry_time != 0:
            downAndSave(url,header,retry_time-1)
        else:
            print("下载失败")

def legalfySaveName(img_title):
    purified_zifr = ''
    for zifu in img_title:
        if zifu not in ['\\','+','\"','*','/','?','<','>','|',':']:
            purified_zifr =  purified_zifr+zifu
        else:
            purified_zifr =  purified_zifr+'-'
    return purified_zifr

def main():
    header_mobile = {'User-Agent':'Mozilla/5.0 (Linux; Android 7.0; SM-G892A Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/67.0.3396.87 Mobile Safari/537.36'}
    url = pyperclip.paste()
    downAndSave(url,header_mobile)

if __name__ == __name__:
    main()