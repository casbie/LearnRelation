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


def main():
    y, x = svm_read_problem('training.txt')
    data_num = len(y)
    fold_num = 5
    for i in range(0, 5):
        if i != fold_num-1:
            index_start = i * (data_num/fold_num)
            index_end = (i+1) * (data_num/fold_num)
        else:
            index_start = i * (data_num / fold_num)
            index_end = data_num 
        print index_start, index_end
        
        m = svm_train(y[index_start:index_end], x[index_start:index_end], '-c 4 -s 2')
        

def main2():
    y1, x1 = svm_read_problem('training.txt')
    m = svm_train(y1, x1, '-c 4 -s 2 -v 5')
    #y2, x2 = svm_read_problem('testing.txt')
    #p_label, p_acc, p_val = svm_predict(y2, x2, m)
    
    #check_label(p_label, '../Data/testing_data.txt', '../Result/result0316_true.txt')
    #print p_label, p_acc, p_val
    #print p_label

if __name__ == '__main__':
    main2()
