import gensim
import json
import numpy
import pprint


# Jsonファイルを読み取ります
def read_params_from_json(path):
    f = open(path)
    df = json.loads(f.read())
    f.close()
    pprint.pprint(df, width=40)

    return df


# JSONファイルに書き出します。
def write_params_to_json(path, data):
    fp = open('/'.join([path, 'data.json']), 'w')
    json.dump(data, fp, cls=MyEncoder)
    fp.close()


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

    params = read_params_from_json('data/label_list.json')

    lexvec_file_path = 'data/lexvec.commoncrawl.300d.W.pos.neg3.vectors'
    wm_en2 = gensim.models.KeyedVectors.load_word2vec_format(lexvec_file_path)

    labels = params['labels']

    all_similarity_list = []

    for label in labels:
      similarity_list = []
      for i in range(365):
        similarity_list.append(wm_en2.similarity(split_keyword(label['name']), split_keyword(labels[i]['name'])))
      all_similarity_list.append(similarity_list)


    result = {}
    result['labels'] = all_similarity_list
    pprint.pprint(result)
    write_params_to_json('output', result)
