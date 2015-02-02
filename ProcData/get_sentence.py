# date: 2015-02-02
# Input: Data/output.jsons
# Output: Sentences

from os.path import join
from os.path import exists
import json
import os

def transfer_jsons():
    input_path = '../Data/sa_json'
    filename = 'output.jsons'

    output_dir = '../Data/sa_sentence_t'
    if not exists(output_dir):
        os.makedirs(output_dir)

    fp = open(join(input_path, filename), 'r')
    
    for line in fp:
        data = json.loads(line)
        write_sentence(data, output_dir)


def write_sentence(data, output_dir):
    
    index = data['index']
    if index < 10:
        str_idx = '000' + str(index)
    elif index < 100:
        str_idx = '00' + str(index)
    elif index < 1000:
        str_idx = '0' + str(index)
    else:
        str_idx = str(index)
    
    fp = open(join(output_dir, str_idx), 'w')
    print str_idx
    for s in data['sentence']:
        for i in range(0, len(s)):
            fp.write(s[i][0].encode('utf-8'))
            if i == len(s)-1:
                fp.write('\n')
            else:
                fp.write(' ')


def main():
    transfer_jsons()


if __name__ == '__main__':
    main()
