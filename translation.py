import gensim
import json
import numpy
import pprint
from googletrans import Translator


# Jsonファイルを読み取ります
def read_params_from_json(path):
    f = open(path)
    df = json.loads(f.read())
    f.close()
    pprint.pprint(df, width=40)

    return df


# JSONファイルに書き出します。
def write_params_to_json(path, data):
    fp = open('/'.join([path, 'translate.json']), 'w')
    json.dump(data, fp, cls=MyEncoder)
    fp.close()


def split_keyword(word):
    slashed_words = word.split("/")
    keywords = slashed_words[0].split("_")
    return keywords[0]


def replace_keyword(word):
    word.replace('_', ' ').replace('/', ' ')
    return word


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

    translator = Translator()
    # response = translator.translate('Hello', dest='ja')
    # print(response.text)

    params = read_params_from_json('data/label_list.json')

    labels = params['labels']

    result = {}

    for label in labels:
        response = translator.translate(replace_keyword(label['name']), dest='ja')
        result[label['name']] = response.text

    pprint.pprint(result)
    write_params_to_json('output', result)
