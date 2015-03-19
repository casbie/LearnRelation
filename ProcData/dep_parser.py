#-*- encoding: utf-8

##########################################################
# * Given json file and dependency tree result,          #
#   combine the feature of dependency tree to the result #
# * Thanks Mr. Aahin and Mr. KC                          #
# * Author: Yu-Ju Chen                                   #
# * Date: 2014-12-26                                     #
# * Modified: 2015-03-03                                 #
##########################################################

from pprint import pprint
import re
import uniout
from subprocess import call
import subprocess
import json
import sys
import os
import io

reload(sys)
sys.setdefaultencoding('utf-8')

def parse(data):

    tokens = []
    value = ''

    # get rid off redundant whitespace, like [ \n\t\r\f\v]
    data = re.sub('\s+\(', '(', data)
    data = re.sub('\s+\)', ')', data)
    # ')(' means we stay in the same level
    data = data.replace(')(', '|')

    # get rid off tailing \n
    data = data.strip()

    # data now should be like
    #(parent(child1(grandchild1:ooo|grandchild2:ooo)|child2:ooo))

    for ch in data.replace(')(', '|'):
        if ch == '(':
            if value != '':
                tokens.append(value)
            tokens.append(ch)
            value = ''
        elif ch == ')':
            if value != '':
                tokens.append(value)
            tokens.append(ch)
            value = ''
        elif ch == '|':
            if value != '':
                tokens.append(value)
            tokens.append(ch)
            value = ''
        elif ch == ' ':
            if value != '':
                tokens.append(value)
            tokens.append(':')
            value = ''
        else:
            value += ch

    #print(''.join(tokens))

    tree = []
    pointer = tree
    parent = []
    leaf = False
    key = ''
    value = ''
    prdigree = []

    for token in tokens:

        if token == '(':
            parent = pointer
            prdigree.append(parent)
            parent.append((key,[]))
            pointer = parent[-1][1]

        elif token == ')':
            if leaf:
                pointer.append((key,value))
            leaf = False
            #pointer = parent
            pointer = prdigree.pop()

        elif token == '|':
            if leaf:
                pointer.append((key,value))
            leaf = False

        elif token == ':':
            leaf = True

        elif leaf:
            value = token
        else:
            key = token

    if len(tree) > 0:
        return tree[0]
    else:
        return []

#example of rel_text: prep(研究-17, 主題-16)
def parse_rel(rel_text):

    index_left = rel_text.find('(')
    index_right = rel_text.rfind(')')
    rel = rel_text[0:index_left]
    content = rel_text[index_left+1:index_right]

    term = content.split(', ')
    
    index = term[0].rfind('-')
    word1 = term[0][0:index]
    num1 = term[0][index+1:]
    
    index = term[1].rfind('-')
    word2 = term[1][0:index]
    num2 = term[1][index+1:]

    rel_list = [rel, word1, word2, num1, num2]
    return rel_list


def main():

    f_json = open('../Data/sa_json/output.jsons')
    new_data = {}

    number = 0
    for line in f_json:
        number += 1
        if number <= 4060:
            continue

        data = json.loads(line)
        new_data = data.copy()

        dependency = []
        relation = []
        for sentence in data['sentence']:
            text = ''
            for i in range(0, len(sentence)):
                text += sentence[i][0]
                if i != len(sentence)-1:
                    text += ' '

            f_tmp = open('tmp_sentence_t', 'w')
            f_tmp.write(text)
            f_tmp.close()
            
            my_cmd = 'opencc -i tmp_sentence_t -o tmp_sentence_s -c ../../opencc/zht2zhs.ini'
            call(my_cmd.split())
            
            my_cmd = '../../tool/stanford-parser-full-2014-10-31/lexparser.sh tmp_sentence_s > tmp_dep_s'
            p = subprocess.Popen(my_cmd, shell=True)
            os.waitpid(p.pid, 0)

            my_cmd = 'opencc -i tmp_dep_s -o tmp_dep_t -c ../../opencc/zhs2zht.ini'
            call(my_cmd.split())

            data_dep = ''
            data_rel = []
            f_dep = open('tmp_dep_t')
            for line in f_dep:
                if line.strip() != '':
                    data_dep += line.strip()
                else:
                    break

            for line in f_dep:
                if line.strip() != '':
                    rel = parse_rel(line.strip())
                    data_rel.append(rel)
                else:
                    break
            
            #data_dep = f_dep.read()
            tree = parse(data_dep)
            dependency.append(tree)
            relation.append(data_rel)

        new_data['dependency'] = dependency
        new_data['relation'] = relation

        filename = ''
        if number < 10:
            filename = '000' + str(number)
        elif number < 100:
            filename = '00' + str(number)
        elif number < 1000:
            filename = '0' + str(number)
        else:
            filename = str(number)

        f_out = io.open('../Data/sa_feature_json/'+filename+'.json', 'wb')
        json.dump(new_data, f_out, ensure_ascii=False)


def main_tmp():

    f_json = open('../Data/sa_json/output.jsons')
    
    for i in range(1, 2):
        
        data_json = f_json.readline()

        if i < 10:
            filename = '000' + str(i)
        elif i < 100:
            filename = '00' + str(i)
        elif i < 1000:
            filename = '0' + str(i)
        else:
            filename = str(i)

        f_dep = open('../Data/sa_parsing_t/'+filename)
        
        for line in f_dep:
            if line.strip() != '':
                data_dep += line
            else:
                break

        #data_dep = f_dep.read()
        #print(data_dep)
        tree = parse(data_dep)
        #pprint(tree)


if __name__ == '__main__':
    main()
