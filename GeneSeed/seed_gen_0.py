# -*- encoding: utf-8 -*-

##############################################################
# * Generate the seed for training the learner of AtLocation #
# * Author: Yu-Ju Chen                                       #
# * Date: 2015-03-09                                         #
#   Modified: 2015-03-11                                     #
##############################################################

#2015-03-10 Todo:
# * link to conceptnet "AtLocation" (borrow the idea from distant supervision)

import os
import sys

#format of data_CN: [[location list], [object list]]
def find_data(data_CN, data_SA, data_SA_index, fp_out):
    print >> sys.stderr, data_SA_index

    import json
    data = json.loads(data_SA)
    write_tag = False

    for words in data['sentence']:
        idx = data['sentence'].index(words)
        info = str(data_SA_index) + '-' + str(idx)
        text = info + ' '
        loc_list = []
        obj_list = []
     
        loc_index = -1
        obj_index = -1

        for i in range(0, len(words)):
            #modify from here
            #check if the place in location list
            
            if words[i][0].encode('utf-8') in data_CN:
                loc = words[i][0].encode('utf-8')
                loc_list.append(i)
                obj_list += data_CN[loc]

        for i in range(0, len(words)):
            #text += words[i][0]
            
            for loc_idx in loc_list:
                if words[i][0].encode('utf-8') in data_CN[words[loc_idx][0].encode('utf-8')]:
                    write_tag = True
                    (loc_index, obj_index) = (loc_idx, i)
                    #text += '(obj)'
                    #print info, words[i][0].encode('utf-8'), words[loc_idx][0].encode('utf-8')
            
            '''
            if words[i][0].encode('utf-8') in obj_list:
                write_tag = True
                text += '(Obj)'
            
            if i in loc_list:
                text += '(Loc)'
            
            if i != len(words)-1:
                text += ' '
            #end modification
            '''

        if write_tag:
            text += (words[obj_index][0]+'-'+words[loc_index][0]+' ')
            for i in range(0, len(words)):
                text += words[i][0]

                '''
                if i == loc_index:
                    text += '(loc)'
                elif i == obj_index:
                    text += '(obj)'
                '''
                if i != len(words)-1:
                    text += ' '
            write_sentence(text, fp_out)

        write_tag = False
        

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


def main1():
    file_path = '../Data/sa_feature_json'
    file_list = os.listdir(file_path)

    fp_out = open('../Seed/seed_list.txt', 'w')

    for f in file_list:
        find_location(os.path.join(file_path, f), fp_out)


def load_conceptnet(data_path):
    fp = open(data_path)
    data_loc = []
    data_loc_obj = {}
    for line in fp:
        data = line.strip().split(',')
        if data[1] not in data_loc:
            data_loc.append(data[1])
            data_loc_obj[data[1]] = [data[0]]
        else:
            data_loc_obj[data[1]].append(data[0])
    
    return data_loc_obj

def main():
    
    fp_in = open('../Data/sa_json/output.jsons')
    fp_out = open('../Seed/seed_list_CN.txt', 'w')

    #read the AtLocation data from ConceptNet
    data_CN = load_conceptnet('../Seed/AtLocation_refine.csv')

    index = 0
    for line in fp_in:
        index += 1
        find_data(data_CN, line.strip(), index, fp_out)

if __name__ == '__main__':
    main()
