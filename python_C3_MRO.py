

def c3(_Ks, start):
    if _Ks[start] == []:
        return [start]
    else:
        _self = start
        _p = [c3(_Ks, i) for i in _Ks[start]]
        _pp = [[i] for i in _Ks[start]]
        return [_self] + merge(_p + _pp)

def merge(args):
    _args = [i for i in args if i !=[]]
    _list = []
    while _args != []:
        for l in _args:
            ret = remove(l[0], _args)
            if ret != []:
                _list.append(l[0])
                _args = ret
                _args = [i for i in _args if i !=[]]
                break
        else:
            raise Exception("AB - BA")

    return _list



def remove(ele, _args):
    t = []
    for i in _args:
        if ele in i[1:]:
            break
    else:
        for i in _args:
            if i[0] == ele:
                t.append(i[1:])
            else:
                t.append(i)
    return t

Ks = {
    "O": [],
    "A": ["O"],
    "B": ["O"],
    "C": ["O"],
    "E": ["A", "B"],
    "F": ["B", "C"],
    "G": ["E", "F"]
}
print(c3(Ks, "O"))
print(c3(Ks, "A"))
print(c3(Ks, "E"))
print(c3(Ks, "G"))

Ks = {
    "O": [],
    "A": ["O"],
    "B": ["O"],
    "C": ["A", "B"],
    "E": ["B", "A"],
    "F": ["C", "E"]
}
print(c3(Ks, "F"))
