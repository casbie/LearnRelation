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
    print(data)

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

    print(''.join(tokens))

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

    return tree[0]


def main():

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
        data_dep = f_dep.read()
        #print(data_dep)
        tree = parse(data_dep)
        pprint(tree)


if __name__ == '__main__':
    main()
