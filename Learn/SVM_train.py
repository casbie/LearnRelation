import sys
sys.path.append('../../Tool/libsvm-3.20/python')
from svmutil import *

def main():
    y1, x1 = svm_read_problem('training.txt')
    m = svm_train(y1, x1, '-c 4 -s 2')
    y2, x2 = svm_read_problem('testing.txt')
    p_label, p_acc, p_val = svm_predict(y2, x2, m)
    #print p_label, p_acc, p_val
    #print p_label

if __name__ == '__main__':
    main()
