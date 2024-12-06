def calculate(s: str) -> str:
    import collections

    # Parse input from string
    lines = s.strip().split("\n")
    v, e = map(int, lines[0].split())
    graph = collections.defaultdict(list)
    for line in lines[1:]:
        a, b = map(int, line.split())
        graph[a - 1].append(b - 1)  # Convert node numbers to 0-indexed

    # Initialize variables
    d = [-1 for _ in range(v)]
    stack = []
    on_stack = [False for _ in range(v)]
    scc_lst = []
    id = 0

    # DFS function
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
            elif on_stack[next]:  # Node is on the stack but not fully processed
                parent = min(parent, d[next])

        # SCC result
        if parent == d[cur]:  # Root of SCC
            scc = []
            while True:
                node = stack.pop()
                on_stack[node] = False
                scc.append(node + 1)  # Convert back to 1-indexed
                if cur == node:
                    break
            scc_lst.append(sorted(scc))

        return parent

    # Run DFS for all nodes
    for i in range(v):
        if d[i] == -1:  # Unvisited node
            dfs(i)

    # Prepare output
    scc_lst.sort()
    result = []
    result.append(str(len(scc_lst)))
    for scc in scc_lst:
        result.append(" ".join(map(str, scc)) + " -1")
    return "\n".join(result)

