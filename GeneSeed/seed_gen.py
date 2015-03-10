# -*- encoding: utf-8 -*-

##############################################################
# * Generate the seed for training the learner of AtLocation #
# * Author: Yu-Ju Chen                                       #
# * Date: 2015-03-09                                         #
##############################################################

#2015-03-09 Todo:
# * read the data in, find out the sentence containing location
# * location list
# * check feasibility by human, then output the result

import os

#read the data in the file and find the sentence with location inside
def find_location(filename, fp_out):
    print filename 
    fp_in = open(filename)
    
    import json
    data = json.load(fp_in)
    write_tag = False

    for words in data['sentence']:
        idx = data['sentence'].index(words)
        text = filename + '-' + str(idx) + ' '
        for i in range(0, len(words)):
            text += words[i][0]
            
            if words[i][1] == 'Nc':
                write_tag = True
                text += '(Nc)'
            
            if i != len(words)-1:
                text += ' '
        
        if write_tag:
            write_sentence(text, fp_out)

        write_tag = False


def write_sentence(content, fp_out):
    fp_out.write(content.encode('utf-8'))
    fp_out.write('\n')

def main():
    file_path = '../Data/sa_feature_json'
    file_list = os.listdir(file_path)

    fp_out = open('../Seed/seed_list.txt', 'w')

    for f in file_list:
        find_location(os.path.join(file_path, f), fp_out)

if __name__ == '__main__':
    main()
