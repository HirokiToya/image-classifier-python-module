import gensim
import json
import numpy
import pprint
import requests

api = "https://script.google.com/macros/s/AKfycbxZQrv_KnBzjEGHIYqm9HcGWC7OS-mzAsagPqyZEmgO_XPX2Dhi/exec?text={text}&source=en&target=ja"

APIKey = "trnsl.1.1.20191202T051703Z.9ec2241a35d55234.52e9f7b1c3f923628b2537d4e6013c3f47d4b6a4"
URL = "https://translate.yandex.net/api/v1.5/tr.json/translate?key={APIKey}&text={text}&lang=ja&format=html"

# Jsonファイルを読み取ります
def read_params_from_json(path):
  f = open(path)
  df = json.loads(f.read())
  f.close()
  return df


# JSONファイルに書き出します。
def write_params_to_json(path, data):
  fp = open('/'.join([path, 'translate1.json']), 'w')
  json.dump(data, fp, cls=MyEncoder)
  fp.close()


# txtファイルを読み取ります．
def read_text_file(path):
  f = open(path)
  list = f.readlines()
  f.close()

  return list


def split_keyword(word):
  slashed_words = word.split("/")
  keywords = slashed_words[0].split("_")
  return keywords[0]


class MyEncoder(json.JSONEncoder):

  def default(self, obj):
    if isinstance(obj, numpy.integer):
      return int(obj)
    elif isinstance(obj, numpy.floating):
      return float(obj)
    elif isinstance(obj, numpy.ndarray):
      return obj.tolist()
    else:
      return super(MyEncoder, self).default(obj)


if __name__ == '__main__':

  resnet_labels = read_params_from_json('input/data/label_list.json')
  imagenet_labels = read_params_from_json('input/data/imagenet1000_clsidx_to_labels.json')

  labels = resnet_labels['labels']
  result = {}

  url = api.format(text="hello")
  r = requests.get(url)
  text = json.loads(r.text)
  print(text)

  # name = 'cat'
  # url = URL.format(APIKey=APIKey, text=name)
  # r = requests.get(url)
  # text = json.loads(r.text)
  # print(text["text"][0])

  # for label in labels:
  #   name = str(label['name']).replace('_', ' ').replace('/', ' ')
  #   url = URL.format(APIKey=APIKey, text=name)
  #   r = requests.get(url)
  #   try:
  #     text = json.loads(r.text)
  #   except Exception as e:
  #     result[label['name']] = "error"
  #     print(label['name'], "error")
  #   else:
  #     result[label['name']] = text["text"][0]
  #     print(label['name'], text["text"][0])

  for i in range(100, 600):
    list = imagenet_labels['{0}'.format(i)]
    for label in list:
      name = str(label.replace(' ', '_'))
      # url = URL.format(APIKey=APIKey, text=name)
      url = api.format(text=name)
      r = requests.get(url)

      try:
        text = json.loads(r.text)
      except Exception as e:
        result[name] = "error"
        print("{\"{name}\":\"{text}\"}".format(name=name, text="error"))
      else:
        result[name] = text["text"]
        print("|\"{name}\":\"{text}\"?".format(name=name, text=text["text"]))

  pprint.pprint(result)
  print('finished')
  write_params_to_json('output', result)
