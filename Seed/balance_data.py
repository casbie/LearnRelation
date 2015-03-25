fp_pos = open('seed_list_CN.txt')
fp_neg = open('seed_list_Wrong.txt')
fp_out = open('seed_list_Wrong_balance.txt', 'w')

data_pos = []
data_neg = []

for line in fp_pos:
    data_pos.append(line)

for line in fp_neg:
    data_neg.append(line)

pos_num = len(data_pos)
neg_num = len(data_neg)
ratio = (neg_num+0.0)/pos_num

num_list = []
import random
for i in range(0, pos_num):
    rand_num = random.randint(0, neg_num)
    while rand_num in num_list:
        rand_num = random.randint(0, neg_num)
    num_list.append(rand_num)

num_list.sort()

for i in num_list:
    fp_out.write(data_neg[i])
