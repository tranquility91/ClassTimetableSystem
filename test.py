from pulp import LpProblem, LpMinimize, LpVariable, lpSum, PULP_CBC_CMD, LpStatus

teachers = ["A", "B", "C", "D", "E"]  # E 不參與
courses = ["國語_1A", "國語_2B", "數學_1A", "數學_2B"]

prob = LpProblem("Test", LpMinimize)
assign = LpVariable.dicts("Assign", [(t, c) for t in teachers[:-1] for c in courses], cat="Binary")

# 每堂課只給一個人
for c in courses:
    prob += lpSum(assign[t, c] for t in teachers[:-1]) == 1

# 每個人只上一堂
for t in teachers[:-1]:
    prob += lpSum(assign[t, c] for c in courses) <= 1

# 解題
status = prob.solve(PULP_CBC_CMD(msg=1))
print("解的狀態:", LpStatus[status])
for t, c in assign:
    if assign[t, c].varValue == 1:
        print(f"{t} 教 {c}")
