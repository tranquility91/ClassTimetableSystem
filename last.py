from table import allocate_courses, courses, teachers
import copy
from pulp import *
from typing import List, Dict, Any, Tuple
from collections import defaultdict

def get_prep_group_id(course):
    """獲取課程的備課組別ID"""
    subject = course["課程名稱"]
    grade = course["年級"]
    
    # 基礎科目（社會、動作、學習）算單獨的備課組別
    if subject in ["社會", "動作", "學習"]:
        return f"{subject}"
        
    # 國文和數學每個年級都是獨立的備課組別
    if subject in ["國語", "數學"]:
        return f"{subject}_{grade}"
    
    return f"{subject}_{grade}"

def count_prep_groups(courses_list):
    """計算一個課程列表中的備課組別數量"""
    prep_groups = set()
    for course in courses_list:
        prep_groups.add(get_prep_group_id(course))
    return len(prep_groups)

def calculate_basic_prep_groups(teacher_load):
    """計算特需課程的備課組別數。每一門課都算一個獨立的備課組別"""
    basic_courses = [c for c in teacher_load["課程"] 
                    if c["課程名稱"] in ["社會", "動作", "學習"]]
    # 每一門特需課程都算一個獨立的備課組別，不進行合併
    return len(basic_courses)

def calculate_chinese_math_prep_groups(teacher_load):
    """計算國數的備課組別數。只有同年級的國語或數學才會合併計算"""
    # 按照科目和年級分組
    groups = defaultdict(list)
    for course in teacher_load["課程"]:
        if course["課程名稱"] in ["國語", "數學"]:
            key = f"{course['課程名稱']}_{course['年級']}"
            groups[key].append(course)
    
    # 只計算不同的科目+年級組合數
    return len(groups)

def allocate_chinese_math(initial_loads, courses):
    """使用整數線性規劃分配國文和數學課"""
    result = copy.deepcopy(initial_loads)
    chinese_math_courses = [c for c in courses if c["課程名稱"] in ["國語", "數學"]]
    
    # 創建問題
    prob = LpProblem("CourseAllocation", LpMinimize)
    
    # 計算每位老師還能接受多少節數
    remaining_lessons = {
        t: 16 - load["節數"]
        for t, load in result.items()
    }
    
    # 計算每位老師的特需備課組別數
    special_prep_groups = {
        t: calculate_basic_prep_groups(load)
        for t, load in result.items()
    }
    
    # 決策變量
    teacher_course = LpVariable.dicts("Assign",
        ((t, i) for t in teachers for i in range(len(chinese_math_courses))),
        cat='Binary')
    
    # 輔助變量
    max_student_hours = LpVariable("MaxStudentHours", 0, None)
    min_student_hours = LpVariable("MinStudentHours", 0, None)
    max_prep_groups = LpVariable("MaxPrepGroups", 0, None)
    min_prep_groups = LpVariable("MinPrepGroups", 0, None)
    
    # 約束1：每個課程只能分配給一位老師
    for i in range(len(chinese_math_courses)):
        prob += lpSum(teacher_course[t, i] for t in teachers) == 1
    
    # 約束2：每位老師的總節數必須等於剩餘可用節數
    for t in teachers:
        prob += lpSum(teacher_course[t, i] * chinese_math_courses[i]["節數"] 
                     for i in range(len(chinese_math_courses))) == remaining_lessons[t]
    
    # 約束3：同年級同組別的國文和數學不能由同一位老師教授
    for i in range(len(chinese_math_courses)):
        for j in range(i + 1, len(chinese_math_courses)):
            if (chinese_math_courses[i]["年級"] == chinese_math_courses[j]["年級"] and 
                chinese_math_courses[i]["組別"] == chinese_math_courses[j]["組別"] and
                chinese_math_courses[i]["課程名稱"] != chinese_math_courses[j]["課程名稱"]):
                for t in teachers:
                    prob += teacher_course[t, i] + teacher_course[t, j] <= 1
    
    # 計算每位老師的總人次和備課組別數
    current_student_hours = {t: result[t]["人次"] for t in teachers}
    for t in teachers:
        # 計算總人次
        total_hours = current_student_hours[t] + lpSum(
            teacher_course[t, i] * chinese_math_courses[i]["人次"]
            for i in range(len(chinese_math_courses)))
        prob += max_student_hours >= total_hours
        prob += min_student_hours <= total_hours

        # 計算備課組別總數
        total_groups = special_prep_groups[t]  # 基礎備課組別數
        prob += max_prep_groups >= total_groups
        prob += min_prep_groups <= total_groups
    
    # 目標函數：同時考慮人次差異和備課組別差異
    prob += max_student_hours - min_student_hours + 100 * (max_prep_groups - min_prep_groups)
    
    # 增加備課組別差異的軟限制
    prob += max_prep_groups - min_prep_groups <= 1
    
    # 求解
    status = prob.solve(PULP_CBC_CMD(msg=False))
    
    if status != 1:
        return None
        
    # 根據求解結果分配課程
    for t in teachers:
        for i in range(len(chinese_math_courses)):
            if value(teacher_course[t, i]) == 1:
                result[t]["課程"].append(chinese_math_courses[i])
                result[t]["節數"] += chinese_math_courses[i]["節數"]
                result[t]["人次"] += chinese_math_courses[i]["人次"]
    
    return result

def verify_chinese_math(loads):
    """檢查每位老師是否都至少有一堂國語和一堂數學"""
    for teacher, load in loads.items():
        has_chinese = any(c["課程名稱"] == "國語" for c in load["課程"])
        has_math = any(c["課程名稱"] == "數學" for c in load["課程"])
        if not (has_chinese and has_math):
            return False
    return True

def save_to_csv(solution):
    """將分配結果保存為CSV文件"""
    import csv
    import os
    from datetime import datetime
    
    # 指定儲存路徑
    save_path = r"C:\Users\USER\OneDrive\桌面"
    
    # 生成檔案名稱，包含時間戳
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"course_allocation_{timestamp}.csv"
    
    # 組合完整的檔案路徑
    full_path = os.path.join(save_path, filename)
    
    # 確保目標資料夾存在
    os.makedirs(save_path, exist_ok=True)
    
    # 準備CSV寫入
    with open(full_path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        # 寫入標題行
        writer.writerow(['老師', '年級', '課程名稱', '組別', '節數', '人次'])
        
        # 寫入每位老師的課程資料
        for teacher, load in solution.items():
            for course in sorted(load['課程'], 
                              key=lambda x: (x['課程名稱'], x['年級'], x['組別'])):
                writer.writerow([
                    teacher,
                    course['年級'],
                    course['課程名稱'],
                    course['組別'],
                    course['節數'],
                    course['人次']
                ])
            # 在每位老師的課程後加入合計行
            writer.writerow([
                f"{teacher}合計",
                '',
                '',
                '',
                load['節數'],
                load['人次']
            ])
            # 加入空行分隔
            writer.writerow([])
    
    print(f"\n分配結果已保存至 {full_path}")

def get_user_choice():
    """獲取用戶選擇"""
    while True:
        print("\n請選擇操作：")
        print("1: 保存這個分配結果")
        print("2: 重新產生新的分配")
        print("3: 結束程式")
        
        choice = input("請輸入選擇 (1/2/3): ").strip()
        
        if choice in ['1', '2', '3']:
            return choice
        else:
            print("無效的輸入，請重試。")

def main():
    max_attempts = 1000
    best_solution = None
    min_student_hours_diff = float('inf')
    min_prep_groups_diff = float('inf')
    
    for attempt in range(max_attempts):
        try:
            # 1. 先分配社會、動作和學習課（特需課程）
            initial_loads = allocate_courses(courses, teachers)
            
            # 2. 再分配國文和數學課（國數課程）
            final_loads = allocate_chinese_math(initial_loads, courses)
            
            if final_loads is None:
                continue
            
            # 檢查每位老師是否都至少有一堂國語和一堂數學
            if not verify_chinese_math(final_loads):
                continue
            
            # 計算人次差異和備課組別差異
            student_hours = [load["人次"] for load in final_loads.values()]
            hours_diff = max(student_hours) - min(student_hours)
            
            prep_groups = [calculate_basic_prep_groups(load) + calculate_chinese_math_prep_groups(load) 
                         for load in final_loads.values()]
            groups_diff = max(prep_groups) - min(prep_groups)
            
            # 如果是更好的解，就保存下來
            if groups_diff <= 1 and hours_diff < min_student_hours_diff:
                min_student_hours_diff = hours_diff
                min_prep_groups_diff = groups_diff
                best_solution = final_loads
                
                # 如果人次差異也在可接受範圍內，就可以結束了
                if hours_diff <= 10:
                    break
            
        except Exception as e:
            continue
    
    if best_solution is None:
        print("無法找到可行解")
        return
    
    while True:
        # 輸出最終分配結果
        print("\n最終分配結果:")
        for teacher, load in best_solution.items():
            print(f"\n{teacher}:")
            # 先輸出課程信息
            for course in sorted(load["課程"], 
                              key=lambda x: (x["課程名稱"], x["年級"], x["組別"])):
                print(f"  - {course['年級']}年級 {course['課程名稱']} {course['組別']} "
                      f"節數: {course['節數']}, 人次: {course['人次']}")
            
            # 計算並輸出備課組別信息
            special_groups = calculate_basic_prep_groups(load)
            chinese_math_groups = calculate_chinese_math_prep_groups(load)
            print(f"  總節數: {load['節數']}, 總人次: {load['人次']}")
            print(f"  備課組別: 特需{special_groups}組 + 國數{chinese_math_groups}組")
        
        # 獲取用戶選擇
        choice = get_user_choice()
        
        if choice == '1':
            save_to_csv(best_solution)
            break
        elif choice == '2':
            print("\n重新產生分配方案...")
            return main()  # 遞迴調用重新執行
        else:  # choice == '3'
            print("\n程式結束")
            break

if __name__ == "__main__":
    main()