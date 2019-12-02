import gensim
import json
import numpy
import pprint
import requests

api = "https://script.google.com/macros/s/AKfycbxZQrv_KnBzjEGHIYqm9HcGWC7OS-mzAsagPqyZEmgO_XPX2Dhi/exec?text={text}&source=en&target=ja"


# Jsonファイルを読み取ります
def read_params_from_json(path):
  f = open(path)
  df = json.loads(f.read())
  f.close()
  # pprint.pprint(df, width=40)

  return df


# JSONファイルに書き出します。
def write_params_to_json(path, data):
  fp = open('/'.join([path, 'translate.json']), 'w')
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

  name = "hello"
  url = api.format(text=name)
  r = requests.get(url)
  print(r.text)

  # for label in labels:
  #   name = str(label['name']).replace('_', ' ').replace('/', ' ')
  #   url = api.format(text=name)
  #   r = requests.get(url)
  #   try:
  #     text = json.loads(r.text)
  #   except Exception as e:
  #     result[label['name']] = "error"
  #     print(label['name'], "error")
  #   else:
  #     result[label['name']] = text["text"]
  #     print(label['name'], text["text"])
  #
  # for i in range(0, 999):
  #   list = imagenet_labels['{0}'.format(i)]
  #   for label in list:
  #     name = str(label.replace(' ', '_'))
  #     url = api.format(text=label)
  #     r = requests.get(url)
  #
  #     try:
  #       text = json.loads(r.text)
  #     except Exception as e:
  #       result[name] = "error"
  #       print(name, "error")
  #     else:
  #       result[name] = text["text"]
  #       print(name, text["text"])

  pprint.pprint(result)
  print('finished')
  write_params_to_json('output', result)
