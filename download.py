# Flickrで写真を検索して、ダウンロードする
from flickrapi import FlickrAPI
from urllib.request import urlretrieve
import pprint
import ssl
import json
import os, time, sys

ssl._create_default_https_context = ssl._create_unverified_context

key = "5809b894abf744c71d17ccd003bdb259"
secret = "ff3aab491f9a930b"
wait_time = 1  # 待機秒数


def go_download(keyword, dir):

    # 画像の保存パスを決定
    savedir = "./" + dir
    if not os.path.exists(savedir):
        os.mkdir(savedir)

    flickr = FlickrAPI(key, secret, format='parsed-json')
    res = flickr.photos.search(
        text=keyword,  # 検索語
        per_page=50,  # 取得件数
        media='photos',  # 写真を検索
        sort="relevance",  # 検索語の関連順に並べる
        safe_search=1,  # セーフサーチ
        extras='url_q, license')
    # 検索結果を確認
    photos = res['photos']
    # pprint(photos)
    try:
        for i, photo in enumerate(photos['photo']):
            url_q = photo['url_q']
            filepath = savedir + '/' + photo['id'] + '.jpg'
            if os.path.exists(filepath): continue
            print(str(i + 1) + ":download=", url_q)
            urlretrieve(url_q, filepath)
            time.sleep(wait_time)

    except:
        import traceback
        traceback.print_exc()


# Jsonファイルを読み取ります
def read_params_from_json(path):
    f = open(path)
    df = json.loads(f.read())
    f.close()
    pprint.pprint(df, width=40)

    return df


def split_keyword(word):
    slashed_words = word.split("/")
    keywords = slashed_words[0].split("_")
    return keywords[0]


#params = read_params_from_json('data/label_list.json')
#labels = params['labels']
#for label in labels:
#    go_download(split_keyword(label['name']), '')


go_download('cabin stone wall', 'cabin/stone wall')
