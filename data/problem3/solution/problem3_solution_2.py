def calculate(s: str) -> int:
    # 입력 데이터를 문자열로 처리
    lines = s.strip().split("\n")
    V, E = map(int, lines[0].split())
    
    # 간선 정보 읽기
    edges = []
    for i in range(1, E + 1):
        A, B, C = map(int, lines[i].split())
        edges.append((A, B, C))  # 간선 정보 추가

    # Union-Find 초기화
    parent = [i for i in range(V + 1)]
    
    def get_parent(x):
        if parent[x] == x:
            return x
        parent[x] = get_parent(parent[x])  # 경로 압축
        return parent[x]
    
    def union_parent(a, b):
        a = get_parent(a)
        b = get_parent(b)
        if a < b:
            parent[b] = a
        else:
            parent[a] = b
    
    def same_parent(a, b):
        return get_parent(a) == get_parent(b)
    
    # Kruskal's Algorithm
    answer = 0
    for a, b, cost in edges:
        if not same_parent(a, b):  # 사이클이 생기지 않으면 추가
            union_parent(a, b)
            answer += cost
    
    return answer

