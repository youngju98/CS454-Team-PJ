from collections import defaultdict
import sys
sys.setrecursionlimit(10**6)

def calculate(s: str) -> str:
    # Parse input
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

    visited = set()

    def dfs(cur):
        nonlocal id
        id += 1
        d[cur] = id
        stack.append(cur)

        for node in visited:
            if node == cur:
                continue

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
            scc_lst.append(scc)
        return parent

    # Visit each node
    for i in range(v):
        if i not in visited:
            visited.add(i)
            dfs(i)

    # Final SCC sorting
    scc_lst = sorted([sorted(scc) for scc in scc_lst]) 

    # Prepare output
    result = []
    result.append(str(len(scc_lst)))
    for scc in scc_lst:
        result.append(" ".join(map(str, scc)) + " -1")
    return "\n".join(result)

