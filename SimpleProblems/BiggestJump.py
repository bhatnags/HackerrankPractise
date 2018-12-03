#l = [27,3,6,10,13,21,45, 8, 10, 80]
l=[3,27,8,9,10,64,7,20,1]


a = [[(l[i]-l[j]) for j in range(i)] for i in range(len(l))]
b = [l[i]-l[j] for i in range(len(l)) for j in range(i) if l[i]>l[j]]

print(max(b))
