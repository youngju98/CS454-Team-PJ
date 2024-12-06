def calculate(s: str) -> str:
    import sys
    sys.setrecursionlimit(10**6)

    # Constants
    VISIT = 0
    NOTVISIT = -1

    # Parse input from string
    lines = s.strip().split("\n")
    V, E = map(int, lines[0].split())
    G = [[] for _ in range(V + 1)]
    visited = [NOTVISIT for _ in range(V + 1)]
    stack = []
    answer = []
    cnt = 0

    # Graph input
    for line in lines[1:]:
        A, B = map(int, line.split())
        G[A].append(B)

    # Tarjan's SCC algorithm
    def dfs(n):
        nonlocal cnt
        cnt += 1
        visited[n] = cnt
        stack.append(n)

        p = visited[n]
        for x in G[n]:
            if visited[x] == NOTVISIT:
                p = min(p, dfs(x))
            elif visited[x] != VISIT:
                p = min(p, visited[x])
        if p == visited[n]:
            temp = []
            while True:
                t = stack.pop()
                temp.append(t)
                visited[t] = VISIT
                if t == n:
                    break
            temp.sort()
            answer.append(temp)

        return p

    # Find all SCCs
    for i in range(1, V + 1):
        if visited[i] == NOTVISIT:
            dfs(i)

    # Prepare the output
    result = []
    result.append(str(len(answer)))
    answer.sort()
    for k in answer:
        result.append(" ".join(map(str, k)) + " -1")
    
    return "\n".join(result)

