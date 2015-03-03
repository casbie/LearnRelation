from pprint import pprint
import re


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
    data = ''
    with open('input.txt') as f:
        # get rid of \n and redundant whitespace
        data = f.read()
    print(data)
    tree = parse(data)
    pprint(tree)


if __name__ == '__main__':
    main()
