from test1 import func2

def func1():
    dict1 = {'room' :
                 {'state' : 0,
                  'layout' : 1,
                  'enemy spawn' : 1}}
    func2(dict1)
    print(dict1)


dict1 = {'room':0, 'floor':1, 'state':2}

for main in dict1:
    value = sum(dict1.values())

for value in dict1.keys():
    value = 0

print(dict1)
