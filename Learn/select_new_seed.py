# -*- encoding: utf-8 -*-

# data sample: 
# 1 1804-32 同學 英國 ∥我跟幾位從英國來的同學合唱一首英國民謠，

fp_in = open('../Result/result0319_0.txt')
fp_out = open('../Seed/seed0319_0.txt', 'w')

data_list = []
pair_list = []

for line in fp_in:
    data = line.strip().split(' ')
    obj = data[2]
    loc = data[3]
    sentence = data[4]
    if (obj, loc) not in pair_list and len(loc)>3:
        pair_list.append((obj, loc))
        data_list.append([obj, loc, sentence])

for data in data_list:
    fp_out.write(data[0]+' ')
    fp_out.write(data[1]+' ')
    fp_out.write(data[2]+'\n')
