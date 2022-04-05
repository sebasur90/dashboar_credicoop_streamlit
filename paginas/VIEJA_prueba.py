lista1=[1,2,3,4,5]
lista2=[10,11,12,13,14]

lista3=[str(x)+str(y) for x,y in zip (lista1,lista2)]

print(lista3)