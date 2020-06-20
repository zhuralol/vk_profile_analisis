# coding=utf-8
# не работает
def data_to_network():
    with open("testgraphdata.txt", encoding='utf-8') as fp:
        #lines = fp.readlines()
        lines = list(fp)
    pass
    return lines

d = data_to_network()
print(d)
