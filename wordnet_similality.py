import json
import numpy
import pprint

from nltk.corpus import wordnet as wn


# Jsonファイルを読み取ります
def read_params_from_json(path):
    f = open(path)
    df = json.loads(f.read())
    f.close()
    pprint.pprint(df, width=40)

    return df


# JSONファイルに書き出します。
def write_params_to_json(path, file_name, data):
    fp = open('/'.join([path, file_name]), 'w')
    json.dump(data, fp, cls=MyEncoder)
    fp.close()


# synsetsの配列の要素を安全に取り出します．
def safe_list_get (l, idx, default):
  try:
    return l[idx].name()
  except IndexError:
    return default


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

  word = "sushi_bar"
  print(wn.synsets(word))

  synsets = wn.synsets(word)
  for synset in synsets:
    print(synset.name(), wn.synset(synset.name()).definition())

  # word1 = wn.synset('broadleaf.s.01')
  # word2 = wn.synset('forest.n.01')
  # print(word1.path_similarity(word2))


  # json = read_json("input/data/label_list_for_wordnet.json")
  # labels = json["labels"]
  #
  # new_label_list = []
  #
  # for label in labels:
  #   synsets = wn.synsets(label["name"])
  #   # print(safe_list_get(synsets, 0, ""))
  #
  #   label["wordnet_name"] = safe_list_get(synsets, 0, "")
  #   print(label)
  #   new_label_list.append(label)
  #
  # result = {}
  # result["labels"] = new_label_list
  # pprint.pprint(result)

  # params = read_params_from_json('input/data/label_list_for_wordnet.json')
  # labels = params['labels']
  #
  # all_similarity_list = []
  #
  # for label in labels:
  #   similarity_list = []
  #   for i in range(365):
  #     # similarity_list.append(wm_en2.similarity(split_keyword(label['name']), split_keyword(labels[i]['name'])))
  #     word1 = wn.synset(label['wordnet_name'])
  #     word2 = wn.synset(labels[i]['wordnet_name'])
  #     print(word1.path_similarity(word2))
  #     similarity_list.append(word1.path_similarity(word2))
  #   all_similarity_list.append(similarity_list)
  #
  # result = {}
  # result['labels'] = all_similarity_list
  # pprint.pprint(result)
  # write_params_to_json('output', 'wordnet_similality.json', result)
