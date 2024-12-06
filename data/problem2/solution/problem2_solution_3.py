from collections import deque

def calculate(s: str) -> int:
    lines = s.strip().split("\n")
    N, M = map(int, lines[0].split())
    country = [list(map(int, lines[i + 1].split())) for i in range(N)]
    answer = 0  # 초기화
    cnt = 1
    used = []
    edge = []
    queue = deque([])

    direction = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # 섬을 번호로 매기는 부분 (BFS)
    for i in range(N):
        for j in range(M):
            if country[i][j] and (i, j) not in used:
                queue.append((i, j))
                used.append((i, j))
                while queue:
                    r, c = queue.popleft()
                    country[r][c] = cnt
                    for idx in range(4):
                        nr = r + direction[idx][0]
                        nc = c + direction[idx][1]
                        if 0 <= nr < N and 0 <= nc < M:
                            if country[nr][nc] and (nr, nc) not in used:
                                queue.append((nr, nc))
                                used.append((nr, nc))
                cnt += 1

    # 행 또는 열을 인자로 넣었을 때 생성할 수 있는 다리가 있는지 확인하는 함수
    def check(li):
        start, cnt = 0, 0
        flag = False
        for idx in range(len(li)):
            if li[idx] and not flag:
                flag = True
                start = li[idx]
            elif not li[idx] and flag:
                cnt += 1
            elif li[idx] and flag and start != li[idx]:
                if start and cnt >= 2:
                    edge.append((start, li[idx], cnt))
                cnt = 0
                start = li[idx]
            elif start == li[idx]:
                cnt = 0

    # 행 탐색
    for row in country:
        if sum(row):
            check(row)

    # 열 탐색
    for col in list(zip(*country)):
        if sum(col):
            check(col)

    # 크루스칼 알고리즘을 활용한 MST 계산
    edge = sorted(edge, key=lambda x: x[2])
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
    root = find(2)
    for i in range(3, cnt):
        if find(i) != root:
            return -1

    return total_cost
