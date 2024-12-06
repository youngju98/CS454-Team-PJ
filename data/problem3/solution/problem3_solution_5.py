def calculate(s: str) -> int:
    lines = s.strip().split("\n")
    V, E = map(int, lines[0].split())
    
    e = []
    for i in range(1, E + 1):
        A, B, C = map(int, lines[i].split())
        e.append((A, B, C))
    
    e.sort(key=lambda x: x[2])

    p = [i for i in range(V)]  

    def get_p(x):
        if p[x] == x:
            return x
        p[x] = get_p(p[x])
        return p[x]
    
    def union_p(a, b):
        a = get_p(a)
        b = get_p(b)
        if a < b:
            p[b] = a
        else:
            p[a] = b
    
    def same_p(a, b):
        return get_p(a) == get_p(b)
    
    answer = 0
    for a, b, cost in e:
        if not same_p(a, b):
            union_p(a, b)
            answer += cost
    
    return answer
