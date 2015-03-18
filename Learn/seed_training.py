# -*- encoding: utf-8 -*-

##############################################################
# * Given seed, learn the classifier for using               #
# * Author: Yu-Ju Chen                                       #
# * Date: 2015-03-10                                         #
##############################################################

#2015-03-10 todo:
# * read the training data
#   - decide the feature
# * read the testing data
# * transfer the data to feature
# * training - one class SVM
# * testing

import json
import sys
import os
sys.path.append('../../Tool/libsvm-3.20/python')
import svmutil

feature_map = {}
feature_num = -1

def extract_feature(raw_data):

    # todo: decide what feature to extract
    loc = raw_data['location']
    obj = raw_data['object']
    sen = raw_data['sentence']
    dep = raw_data['dependency']
    rel = raw_data['relation']

    #define output data
    order = True #which means loc_index > obj_index

    word_list = []
    for w in sen:
        word_list.append(w[0])

    loc_idx = word_list.index(loc.decode('utf-8'))
    obj_idx = word_list.index(obj.decode('utf-8'))

    idx_S, idx_L = obj_idx, loc_idx
    ent1, ent2 = obj, loc 
    
    if loc_idx < obj_idx:
        order = False
        idx_S, idx_L = loc_idx, obj_idx
        ent1, ent2 = loc, obj

    front = ''
    middle = ''
    back = ''

    for i in range(0, idx_S):
        front += sen[i][1]
        if i != idx_S-1:
            front += ' '
    
    for i in range(idx_S+1, idx_L):
        middle += sen[i][1]
        if i != idx_L-1:
            middle += ' '

    for i in range(idx_L+1, len(sen)):
        back += sen[i][1]
        if i != len(sen)-1:
            back += ' '
  
    dep_path = trace_tree(dep, ent1, ent2)
    feature = ['order:'+str(order), 'pos_f:'+front, 'pos_m:'+middle, 'pos_b:'+back, 'tree:'+dep_path]
    return feature_to_number(feature)


def find_path(tree, target):
    
    if type(tree[1]) is unicode:
        if tree[1].encode('utf-8') == target:
            return True, []
        else:
            return False, []

    elif type(tree[1]) is list:
        '''
        for child in tree[1]:
            found, path = find_path(child, target)
            if found:
                return found, [child[0]]+path
        '''
        for i in range(0, len(tree[1])):
            found, path = find_path(tree[1][i], target)
            if found:
                return found, [tree[1][i][0]+'-'+str(i)]+path

    #else:
    #    print type(tree[1])

    return found, path


def trace_tree(tree, ent1, ent2):
    import uniout 
    #print tree, '\n'
    (found, path1) = find_path(tree, ent1)
    (found, path2) = find_path(tree, ent2)
    #print ent1, ent2, path1, path2, '\n' 
    
    min_len = min(len(path1), len(path2))
    if min_len < 1:
        #print 'ERROR: min_len < 1'
        return ''

    branch = min_len
    for i in range(0, min_len):
        if path1[i] != path2[i]:
            branch = i
            break

    path = ''
    for i in range(0, len(path1)-branch):
        path += (path1[len(path1)-1-i].split('-')[0]+'<-')
    #print len(path1), branch
    path += path1[branch-1].split('-')[0]
    for i in range(branch, len(path2)):
        path += ('->'+path2[i].split('-')[0])

    #print path
    return path


def feature_to_number(feature_list):    
    number_feature = []
    for f in feature_list:
        if f not in feature_map:
            global feature_num
            feature_num = feature_num + 1
            feature_map[f] = feature_num
            number_feature.append(feature_num)
        else:
            number_feature.append(feature_map[f])
    return number_feature


def read_seed(seed_file, data_path):
    print 'start reading seed...'
    fp_seed = open(seed_file)
    seed_data = []
    for line in fp_seed:
        index_info = line.strip().split(' ')
        file_index  = index_info[0].split('-')[0]
        sentence_index = int(index_info[0].split('-')[1])
        obj = index_info[1].split('-')[0]
        loc = index_info[1].split('-')[1]

        if int(file_index) < 10:
            file_name = '../Data/sa_feature_json_test/000' + file_index + '.json'
        elif int(file_index) < 100:
            file_name = '../Data/sa_feature_json_test/00' + file_index + '.json'
        elif int(file_index) < 1000:
            file_name = '../Data/sa_feature_json_test/0' + file_index + '.json'
        else:
            file_name = '../Data/sa_feature_json_test/' + file_index + '.json'

        if os.path.isfile(file_name):

            #transfer "臺" to "台"
            fp_tmp = open('tmp', 'w')
            fp_tmp.write(open(file_name).read().replace('\xe8\x87\xba', '\xe5\x8f\xb0'))
            fp_tmp.close()

            fp_data = open('tmp')
            #fp_data = open(file_name)
            data = json.load(fp_data)
        
            data_sentence = data['sentence'][sentence_index]
            data_dependency = data['dependency'][sentence_index]
            data_relation = data['relation'][sentence_index]

            raw_data = {'sentence': data_sentence, 
                    'dependency': data_dependency, 
                    'relation': data_relation, 
                    'location': loc, 
                    'object': obj}

            feature = extract_feature(raw_data)
            seed_data.append(feature)
    return seed_data


def read_data():
    return 0


def gene_testing_data(data_path):
    from os import listdir
    from os.path import isfile, join
    file_list = [ f for f in listdir(data_path) if isfile(join(data_path,f)) ]

    fp_out = open('../Data/testing_data.txt', 'w')

    for f in file_list:
        print f
        file_info = str(int(f[0:4]))
        fp = open(join(data_path, f))
        data = json.load(fp)

        for words in data['sentence']:

            sentence_info = str(data['sentence'].index(words))

            text = ''
            noun_list = []
            loc_list = []
            for i in range(len(words)):
                text += (words[i][0]+' ')
                if words[i][1][0:2] == 'Nc':
                    loc_list.append(words[i][0])
                elif words[i][1][0:2] in ['Na', 'Nb']:
                    noun_list.append(words[i][0])
            
            for i in range(0, len(noun_list)):
                for j in range(i+1, len(loc_list)):
                    fp_out.write(file_info+'-'+sentence_info+' '+(noun_list[i]+'-'+loc_list[j]+' '+text).encode('utf-8')+'\n')


def write_SVM_data(data_list, output_file):
    fp = open(output_file, 'w')
    for data in data_list:
        fp.write('+1 ')
        for dim in range(0, len(data)):
            fp.write(str(data[dim])+':1')
            if dim != len(data)-1:
                fp.write(' ')
            else:
                fp.write('\n')


def check_label(label, input_data, output_data):
    fp_in = open(input_data)
    fp_out = open(output_data, 'w')
    data = []
    for line in fp_in:
        text = ''
        words = line.strip().split(' ')
        text += (words[0]+' ')
        text += (words[1].split('-')[0]+' ')
        text += (words[1].split('-')[1]+' ')
        for i in range(2, len(words)):
            text += words[i]
        data.append(text)

    for i in range(0, len(label)):
        if int(label[i]) == 1:
            fp_out.write(str(int(label[i]))+' '+data[i]+'\n')


def one_class_cross():
    y1, x1 = svm_read_problem('training.txt')
    m = svm_train(y1, x1, '-c 4 -s 2 -v 5')


def one_class():
    y1, x1 = svm_read_problem('training.txt')
    m = svm_train(y1, x1, '-c 4 -s 2 -v 5')
    y2, x2 = svm_read_problem('testing.txt')
    p_label, p_acc, p_val = svm_predict(y2, x2, m)
    
    check_label(p_label, '../Data/testing_data.txt', '../Result/result0320_true.txt')


def main():
    seed_file = '../Seed/seed_list_CN.txt'
    data_path = '../Data/sa_feature_json_test'

    seed_feature = read_seed(seed_file, data_path)
    write_SVM_data(seed_feature, 'training.txt')
     
    # training
    gene_testing_data(data_path)

    # read testing data and training
    data_file = '../Data/testing_data.txt'
    #data_feature = read_seed(data_file, data_path)
    #for i in range(0, len(data_feature)):
    #    print data_feature[i]

    #write_SVM_data(data_feature, 'testing.txt')

if __name__ == '__main__':
    main()
