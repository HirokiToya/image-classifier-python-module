import json
import pprint


# Jsonファイルを読み取ります
def read_params_from_json(path):
    f = open(path)
    df = json.loads(f.read())
    f.close()
    # pprint.pprint(df, width=40)

    return df


if __name__ == '__main__':
  lexvec_similalities = read_params_from_json("input/data/lexvec_similality.json")
  wordnet_similalities = read_params_from_json("input/data/wordnet_similality.json")

  labels = wordnet_similalities['labels']
  pprint.pprint(labels[3])
