# -*- encoding: utf-8 -*-

#########################################################
# * This file is used for parsing xml data to json data #
#   Input: balanced data from CKIP                      #
#    Output: sentences and pos tag with json format     #
# * Thanks Mr. Aahin for encoding problem               #
# * Author: Yu-Ju Chen                                  #
# * Date: 2014-10-31                                    #
# * Modified: 2015-01-28                                #
#########################################################

import codecs
import json
import io
import sys
import xml.etree.ElementTree as ET
from os import listdir, makedirs
from os.path import isfile, join, exists


sys.path.insert(0, '../Util')
from mytool import delete_same

reload(sys)
sys.setdefaultencoding('utf-8')

def transfer_xml_data(data_path):
    # tell codecs the encoding of file
    #with codecs.open(fpath, encoding='big5') as f:
    with codecs.open(data_path, encoding='big5', errors='ignore') as f:
        content = f.read()
        # now content is utf-8 encoded

    # replace encoding declaration
    content = content.replace('encoding="Big5"', 'encoding="utf-8"', 1)

    with codecs.open('tmp.xml', 'wb', encoding='utf-8') as f:
        f.write(content)


def extract_all_data(start_index):
    data = []
    tree = ET.parse('tmp.xml')
    root = tree.getroot()
    
    index = start_index
    #root: corpus, child: article
    for child in root:
        index += 1
        title = child.find('title').text
        topic = child.find('topic').text
        sentences = child.iter(tag='sentence')

        pos_sentences = []
        for s in sentences:
            pos_sentences.append(parse_data(s.text))
        data.append({'index': index, 'title': title, 'topic': topic, 'sentence': pos_sentences})

    return data, index


def parse_data(sentence):
    
    postag = sentence.split('　'.decode('utf8'))
    pos_sentence = []
    
    for word in postag:
        word_split = word.split('(')
        if len(word_split) != 2:
            continue
        content = word_split[0]
        tag = word_split[1][0:-1]
        pos_sentence.append((content,tag))
    
    return pos_sentence
    

def write_data(output_file_name, output_data):

    fp_out=io.open(output_file_name, 'wb')
    for data in output_data:
        json.dump(data, fp_out, ensure_ascii=False)
        fp_out.write('\n')


def main():
    
    data_path = '../Data/sa_corpus'
    files = [ f for f in listdir(data_path) if isfile(join(data_path,f)) ]
    #files = [ f for f in ['xmlcorpus_115.xml', 'xmlcorpus_300.xml'] if isfile(join(data_path,f)) ]

    # read all data from corpus
    final_data = []
    tmp_index = 0
    for f in files:
        print f
        transfer_xml_data(join(data_path,f))
        data, tmp_index = extract_all_data(tmp_index)
        final_data = final_data + data

   
    #create folder for output data
    output_path = '../Data/sa_json'
    if not exists(output_path):
        makedirs(output_path)

    '''
    #seperate the data as 10 pieces, save them to a json file
    data_num = len(final_data)
    data_num_per_file = data_num / 10
    
    #write output data to files
    for i in range(0,10):
        start_index = data_num_per_file * i
        if i == 9:
            end_index = data_num - 1
        else:
            end_index = start_index + data_num_per_file
        write_data('output' + str(i) + '.jsons',final_data[start_index:end_index], i)
    '''

    write_data(join(output_path,'output.jsons'), final_data)

if __name__ == '__main__':
    main()
