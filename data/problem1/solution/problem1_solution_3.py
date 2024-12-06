from collections import defaultdict, deque
import sys
sys.setrecursionlimit(10**6)

def calculate(s: str) -> str:
    # Parse input from string
    lines = s.strip().split("\n")
    v, e = map(int, lines[0].split())
    graph = defaultdict(list)
    for line in lines[1:]:
        a, b = map(int, line.split())
        graph[a - 1].append(b - 1)  # Convert to 0-based index

    d = [-1 for _ in range(v)]  # Discovery time of each node
    stack = []
    on_stack = [False for _ in range(v)]
    scc_lst = []
    id = 0

    # Tarjan's algorithm for SCC detection
    def dfs(cur):
        nonlocal id
        id += 1
        d[cur] = id
        stack.append(cur)
        on_stack[cur] = True

        parent = d[cur]
        for next in graph[cur]:
            if d[next] == -1:  # Unvisited node
                parent = min(parent, dfs(next))
            elif on_stack[next]:  # Back edge to a node on the stack
                parent = min(parent, d[next])

            return parent

        # If cur is the root of an SCC, extract all nodes in this SCC
        scc = []
        while True:
            node = stack.pop()
            on_stack[node] = False
            scc.append(node + 1)  # Convert back to 1-based index
            if cur == node:
                break
        scc_lst.append(scc)  # **Unsorted SCC** (no sorting performed)
        return parent

    # Run DFS for all nodes
    for i in range(v):
        if d[i] == -1:  # Unvisited node
            dfs(i)

    result = []
    result.append(str(len(scc_lst)))
    for scc in scc_lst:  # Output SCCs in the order they were added
        result.append(" ".join(map(str, scc)) + " -1")

    return "\n".join(result)


