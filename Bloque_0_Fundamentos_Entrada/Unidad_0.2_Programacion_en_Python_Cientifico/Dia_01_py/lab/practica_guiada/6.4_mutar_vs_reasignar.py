def añade_en_sitio(lst):
    lst.append(0)  # muta


def reemplaza(lst):
    lst = [0]  # reasigna (local)


d = [1, 2];

añade_en_sitio(d);

print(d)  # [1, 2, 0]

d = [1, 2];
reemplaza(d);
print(d)  # [1, 2]
