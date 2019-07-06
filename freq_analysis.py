def count_unsorted(s: str) -> dict:
    result = {}
    
    for c in s:
        # 利用错误处理机制，效率可能会更快
        try:
            result[c] += 1
        except KeyError:
            result[c] = 1
    
    return result

def count(s: str) -> list:
    # XXX: optimization
    
    result = count_unsorted(s)
    result = list(map(lambda x: (x, result[x]), result))
    
    # 直接在 result 上操作，节省内存占用
    result.sort(key=lambda x: x[1], reverse=True)
    
    return result

def frequency(s: str) -> dict:
    result = count(s)
    length = len(s)

    result = dict(map(lambda x: (x / length, result[x]), result))
    
    return result
