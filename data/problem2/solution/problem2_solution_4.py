from collections import deque

def calculate(s: str) -> int:
    lines = s.strip().split("\n")
    N, M = map(int, lines[0].split())
    country = [list(map(int, lines[i + 1].split())) for i in range(N)]
    answer = 0  # 초기화
    cnt = 1
    edge = []
    queue = deque([])
    visited = [[False] * M for _ in range(N)]  # 방문 체크용 배열

    direction = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # 섬을 번호로 매기는 부분 (BFS)
    for i in range(N):
        for j in range(M):
            if country[i][j] == 1 and not visited[i][j]:
                queue.append((i, j))
                while queue:
                    r, c = queue.popleft()
                    if visited[r][c]:
                        continue
                    visited[r][c] = True
                    country[r][c] = cnt
                    for dx, dy in direction:
                        nr, nc = r + dx, c + dy
                        if 0 <= nr < N and 0 <= nc < M and country[nr][nc] == 1:
                            queue.append((nr, nc))
                cnt += 1

    # 2. 다리 탐색
    def check(li):
        for i in range(len(li)): 
            for j in range(i + 1, len(li)): 
                if li[i] != 0 and li[j] != 0 and li[i] != li[j]:
                    distance = abs(j - i) - 1
                    if distance >= 2:
                        edge.append((li[i], li[j], distance))

    # 행 탐색
    for row in country:
        if sum(row) > 0:  # 0이 아닌 값이 있으면 탐색
            check(row)

    # 열 탐색
    for c in range(M):
        column = [country[r][c] for r in range(N)]
        if sum(column) > 0:  # 0이 아닌 값이 있으면 탐색
            check(column)

    # 크루스칼 알고리즘을 활용한 MST 계산
    edge.sort(key=lambda x: x[2])  # 간선을 거리 기준으로 정렬
    parent = list(range(cnt))

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        root_x = find(x)
        root_y = find(y)
        if root_x != root_y:
            parent[root_y] = root_x

    total_cost = 0
    for a, b, cost in edge:
        if find(a) != find(b):
            union(a, b)
            total_cost += cost

    # 모든 섬이 연결되었는지 확인 
    roots = set(find(i) for i in range(2, cnt))
    if len(roots) > 1:
        return -1

    return total_cost
