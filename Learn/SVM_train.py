import sys
sys.path.append('../../Tool/libsvm-3.20/python')
from svmutil import *

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
        

def cross_validation():
    y, x = svm_read_problem('training.txt')
    m = svm_train(y, x, '-c 4 -v 5 -t 0')


def train_predict(output_file):
    y1, x1 = svm_read_problem('training.txt')
    m = svm_train(y1, x1, '-c 4 -t 0')
    y2, x2 = svm_read_problem('testing.txt')
    p_label, p_acc, p_val = svm_predict(y2, x2, m)
    check_label(p_label, '../Data/testing_data.txt', output_file)
    

def main():
    #train_predict('../Result/result0319_0.txt')
    cross_validation()

if __name__ == '__main__':
    main()
