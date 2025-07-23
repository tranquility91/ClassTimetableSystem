from table import allocate_courses, courses, teachers
import copy
from pulp import *
from typing import List, Dict, Any, Tuple

def allocate_main_subjects(initial_loads, courses):
    """使用整數線性規劃分配國文和數學課"""
    # 複製初始負載
    result = copy.deepcopy(initial_loads)
    
    # 獲取還需要分配的課程
    main_courses = [c for c in courses if c["課程名稱"] in ["國語", "數學"]]
    
    # 創建問題
    prob = LpProblem("CourseAllocation", LpMinimize)
    
    # 計算每位老師還能接受多少節數
    remaining_lessons = {
        t: 16 - load["節數"]
        for t, load in result.items()
    }
    
    # 決策變量：teacher_course[t][c] = 1 表示課程c分配給老師t
    teacher_course = LpVariable.dicts("Assign",
        ((t, i) for t in teachers for i in range(len(main_courses))),
        cat='Binary')
    
    # 目標函數 (可以是最小化總人次差異)
    prob += 0
    
    # 約束1：每個課程只能分配給一位老師
    for i in range(len(main_courses)):
        prob += lpSum(teacher_course[t, i] for t in teachers) == 1
    
    # 約束2：每位老師的總節數必須等於剩餘可用節數
    for t in teachers:
        prob += lpSum(teacher_course[t, i] * main_courses[i]["節數"] 
                     for i in range(len(main_courses))) == remaining_lessons[t]
    
    # 約束3：同年級同組別的國文和數學不能由同一位老師教授
    for i in range(len(main_courses)):
        for j in range(i + 1, len(main_courses)):
            if (main_courses[i]["年級"] == main_courses[j]["年級"] and 
                main_courses[i]["組別"] == main_courses[j]["組別"] and
                main_courses[i]["課程名稱"] != main_courses[j]["課程名稱"]):
                for t in teachers:
                    prob += teacher_course[t, i] + teacher_course[t, j] <= 1
    
    # 求解
    status = prob.solve(PULP_CBC_CMD(msg=False))
    
    if status != 1:  # 如果沒有找到解
        return None
        
    # 根據求解結果分配課程
    for t in teachers:
        for i in range(len(main_courses)):
            if value(teacher_course[t, i]) == 1:
                result[t]["課程"].append(main_courses[i])
                result[t]["節數"] += main_courses[i]["節數"]
                result[t]["人次"] += main_courses[i]["人次"]
    
    return result

def main():
    while True:
        try:
            # 1. 先分配社會、動作和學習課
            initial_loads = allocate_courses(courses, teachers)
            
            # 2. 再分配國文和數學課
            final_loads = allocate_main_subjects(initial_loads, courses)
            
            if final_loads is None:
                print("無法找到可行的主科分配方案，重試中...")
                continue
                
            # 輸出最終分配結果
            print("\n最終分配結果:")
            for teacher, load in final_loads.items():
                print(f"\n{teacher}:")
                for course in sorted(load["課程"], 
                                  key=lambda x: (x["課程名稱"], x["年級"], x["組別"])):
                    print(f"  - {course['課程名稱']} {course['組別']} "
                          f"節數: {course['節數']}, 人次: {course['人次']}")
                print(f"  總節數: {load['節數']}, 總人次: {load['人次']}")
            
            # 驗證結果
            for teacher, load in final_loads.items():
                assert load["節數"] == 16, f"{teacher} 總節數不是16"
            
            break
            
        except Exception as e:
            print(f"發生錯誤: {e}，重試中...")
            continue

if __name__ == "__main__":
    main()