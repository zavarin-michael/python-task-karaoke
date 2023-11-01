# flake8: noqa

punctuation = ["_"]
whitespace = [" "]


def distance(a, b):
    n, m = len(a), len(b)
    if n > m:
        a, b = b, a
        n, m = m, n

    current_row = range(n + 1)
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = (
                previous_row[j] + 1,
                current_row[j - 1] + 1,
                previous_row[j - 1],
            )
            if a[j - 1] != b[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)
    return current_row[n]


def transliterate(text):
    text = text.lower()
    for c in punctuation + whitespace:
        text = text.replace(c, "")
    return text


def search(text, dict):
    text = transliterate(text)
    lt = {}
    for name in dict:
        lt[name] = {}
        if len(name) == len(text):
            lt[name][name] = distance(text, name)
        elif len(name) > len(text):
            for i in range(0, len(name)):
                q = name[i : len(text) + i]
                if len(text) > len(q):
                    break
                lt[name][q] = distance(text, q)
        elif len(name) < len(text):
            for i in range(0, len(text)):
                q = text[i : len(name) + i]
                if len(name) > len(q):
                    break
                lt[name][q] = distance(text, q)
    res = {}
    lst = lt
    for name in lt:
        items = list(lst[name].items())
        items.sort(key=lambda i: i[1])
        o = 99999
        for i in items:
            if i[1] <= o:
                lst[name][i[0]] = i[1]
                o = i[1]
    lt = lst
    del lst
    for name in lt:
        c = 99999
        res[name] = {}
        for val in lt[name]:
            if c >= lt[name][val]:
                res[name][val] = lt[name][val]
                c = lt[name][val]
        res[name] = {}
        for val in lt[name]:
            if c >= lt[name][val]:
                res[name][val] = lt[name][val]
                c = lt[name][val]
    result = {}
    for name in res:
        for val in res[name]:
            result[name] = res[name][val]
            break
    del res
    r = result
    c = 99999
    for name in list(result):
        if result[name] > c:
            del r[name]
        elif result[name] < c:
            c = result[name]
    for name in list(result):
        if result[name] > c:
            del r[name]
        elif result[name] < c:
            c = result[name]
    result = []
    for name in list(r):
        result.append(name)
    return result
