from collections import defaultdict
import sys
sys.setrecursionlimit(10**6)

def calculate(s: str) -> str:
    lines = s.strip().split("\n")
    v, e = map(int, lines[0].split())
    graph = defaultdict(list)
    for line in lines[1:]:
        a, b = map(int, line.split())
        graph[a - 1].append(b - 1)

    d = [-1 for _ in range(v)]
    stack = []
    scc_lst = []
    id = 0

    def dfs(cur):
        nonlocal id
        id += 1
        d[cur] = id
        stack.append(cur)

        parent = d[cur]
        for next in graph[cur]:
            if d[next] == -1:
                parent = min(parent, dfs(next))
            elif next in stack:
                parent = min(parent, d[next])

        if parent == d[cur]:
            scc = []
            while stack:
                node = stack.pop()
                scc.append(node + 1)
                if node == cur:
                    break
            scc_lst.append(sorted(scc))
        return parent

    # DFS 실행
    for i in range(v):
        if d[i] == -1:
            dfs(i)

    # 결과 정렬 (SCC)
    scc_lst.sort(key=lambda x: x[0])

    result = []
    result.append(str(len(scc_lst)))
    for scc in scc_lst:
        result.append(" ".join(map(str, scc)) + " -1")
    return "\n".join(result)
