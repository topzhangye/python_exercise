def op(code):
    op_tab = ['', '+', '-']
    return op_tab[code]

#3进制表达"", + - 的8组排列组合
def get(num, i):
    temp = num
    while i != 0:
        k = temp // 3
        if k == 0:
            return op(temp)
        else:
            temp = k
            i -= 1

    return op(temp % 3)


def cal():
    total = 3 ** 8
    i = 0
    the_number = "123456789"
    while i < total:
        #生成表达式 例如 1+23-4+56+7+8+9
        t, j = "", 0
        while j < 8:
            t += (the_number[j] + get(i, j))
            j += 1
        t += the_number[8]
        i += 1
        yield t

if __name__ == "__main__": 
    for i in cal():
        if eval(i) == 100:
            print(i)

"""
1+23-4+56+7+8+9
12+3-4+5+67+8+9
1+23-4+56+7+8+9
1+2+3-4+5+6+78+9
12+3-4+5+67+8+9
1+23-4+56+7+8+9
1+2+34-5+67-8+9
1+23-4+5+6+78-9
123+45-67+8-9
123-4-5-6-7+8-9
"""

