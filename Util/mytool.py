#delete_same: delete the same items in a list
#   Input: list
#   Output: list with no duplication

def delete_same(noun_list):
    seen=[]
    for n in noun_list:
        if n not in seen:
            seen.append(n)
    return seen
