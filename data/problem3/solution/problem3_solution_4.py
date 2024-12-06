def calculate(s: str) -> int:
    lines = s.strip().split("\n")
    V, E = map(int, lines[0].split())
    
    edges = []
    for i in range(1, E + 1):
        A, B, C = map(int, lines[i].split())
        edges.append((A, B, C))
    
    edges.sort(key=lambda x: x[2])

    parent = [i for i in range(V + 1)]
    
    def get_parent(x):
        while parent[x] != x:
            x = parent[x]
        return x
    
    def union(a, b):
        a = get_parent(a)
        b = get_parent(b)
        if a < b:
            parent[b] = a
        else:
            parent[a] = b
    
    def same_parent(a, b):
        return get_parent(a) == get_parent(b)
    
    answer = 0
    for a, b, c in edges:
        if not same_parent(a, b):
            union(a, b)
            answer += c
    
    return answer
