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

    # 섬을 번호로 매기는 부분(BFS)
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
                    if (start, li[idx], cnt) not in edge:
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

    # 그룹핑 함수
    def group(connected, yet, answer):
        for _ in range(len(yet)):
            test = yet.popleft()
            if test[0] in connected or test[1] in connected:
                if test[0] in connected and test[1] in connected:
                    yet.append(test)
                    continue
                if test[0] not in connected:
                    connected.append(test[0])
                else:
                    connected.append(test[1])
                answer += test[2]
        return answer

    edge = sorted(edge, key=lambda x: [x[2]])
    yet = deque([])
    if len(edge):
        connected = [edge[0][0], edge[0][1]]
        answer = edge[0][2]
        for idx in range(1, len(edge)):
            if edge[idx][0] in connected or edge[idx][1] in connected:
                if edge[idx][0] in connected and edge[idx][1] in connected:
                    continue
                if edge[idx][0] not in connected:
                    connected.append(edge[idx][0])
                else:
                    connected.append(edge[idx][1])
                answer += edge[idx][2]
                if len(yet):
                    answer = group(connected, yet, answer)
            else:
                yet.append(edge[idx])
        answer = answer if len(connected) == cnt - 1 else -1
        return answer
    else:
        return -1
