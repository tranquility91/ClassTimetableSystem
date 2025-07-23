# course_allocator.py
from typing import List, Dict, Any, Tuple
from collections import defaultdict
from pulp import *
import copy
# 從 table.py 導入所需的函數和變數
from table import allocate_courses, courses, teachers

# 導出 allocate_courses 讓其他模組可以使用
__all__ = ['allocate_courses', 'allocate_chinese_math', 'calculate_basic_prep_groups', 
           'calculate_chinese_math_prep_groups', 'verify_chinese_math']

def get_prep_group_id(course):
    """獲取課程的備課組別ID"""
    subject = course["課程名稱"]
    grade = course["年級"]
    
    if subject in ["社會", "動作", "學習"]:
        return f"{subject}"
    
    if subject in ["國語", "數學"]:
        return f"{subject}_{grade}"
    
    return f"{subject}_{grade}"

# ... (其他函數保持不變) ...

def calculate_basic_prep_groups(teacher_load):
    """計算特需課程的備課組別數"""
    basic_courses = [c for c in teacher_load["課程"] 
                    if c["課程名稱"] in ["社會", "動作", "學習"]]
    return len(basic_courses)

def calculate_chinese_math_prep_groups(teacher_load):
    """計算國數的備課組別數"""
    groups = defaultdict(list)
    for course in teacher_load["課程"]:
        if course["課程名稱"] in ["國語", "數學"]:
            key = f"{course['課程名稱']}_{course['年級']}"
            groups[key].append(course)
    return len(groups)

def allocate_chinese_math(initial_loads, courses):
    """使用整數線性規劃分配尚未分配的國文與數學課"""
    import copy
    from pulp import LpProblem, LpMinimize, LpVariable, lpSum, value, LpBinary, PULP_CBC_CMD
    from collections import defaultdict

    result = initial_loads.copy()

    # 找出已經分配的課程 id
    assigned_course_ids = set(
        id(c) for load in result.values() for c in load["課程"]
    )

    # 保留尚未被分配的國語或數學課程
    chinese_math_courses = [
        c for c in courses
        if c["課程名稱"] in ["國語", "數學"] and id(c) not in assigned_course_ids
    ]

    # 計算老師剩餘可排節數
    remaining_lessons = {
        t: 16 - load["節數"]
        for t, load in result.items()
    }


    # 沒有需要分配的國數課就直接回傳
    if not chinese_math_courses:
        return result

    prob = LpProblem("CourseAllocation", LpMinimize)

    # 計算特需課的備課組數
    special_prep_groups = {
        t: calculate_basic_prep_groups(load)
        for t, load in result.items()
    }

    # 定義變數
    teacher_course = LpVariable.dicts("Assign",
        ((t, i) for t in result.keys() for i in range(len(chinese_math_courses))),
        cat=LpBinary)

    max_student_hours = LpVariable("MaxStudentHours", 0, None)
    min_student_hours = LpVariable("MinStudentHours", 0, None)
    max_prep_groups = LpVariable("MaxPrepGroups", 0, None)
    min_prep_groups = LpVariable("MinPrepGroups", 0, None)

    # 每堂課只能分配給一位老師
    for i in range(len(chinese_math_courses)):
        prob += lpSum(teacher_course[t, i] for t in result.keys()) == 1

    # 每位老師的總節數 = 剩餘節數（強制）
    for t in result.keys():
        prob += lpSum(
            teacher_course[t, i] * chinese_math_courses[i]["節數"]
            for i in range(len(chinese_math_courses))
        ) == remaining_lessons[t]

    # 同年級同組別不同科目不能由同一人授課
    for i in range(len(chinese_math_courses)):
        for j in range(i + 1, len(chinese_math_courses)):
            ci = chinese_math_courses[i]
            cj = chinese_math_courses[j]
            if ci["年級"] == cj["年級"] and ci["組別"] == cj["組別"] and ci["課程名稱"] != cj["課程名稱"]:
                for t in result.keys():
                    prob += teacher_course[t, i] + teacher_course[t, j] <= 1

    # 限制人次與備課組數
    current_student_hours = {t: result[t]["人次"] for t in result.keys()}
    for t in result.keys():
        total_hours = current_student_hours[t] + lpSum(
            teacher_course[t, i] * chinese_math_courses[i]["人次"]
            for i in range(len(chinese_math_courses)))
        prob += max_student_hours >= total_hours
        prob += min_student_hours <= total_hours

        total_groups = special_prep_groups[t]
        prob += max_prep_groups >= total_groups
        prob += min_prep_groups <= total_groups

    # 目標函數：平衡人次與備課組數
    prob += (max_student_hours - min_student_hours) + 100 * (max_prep_groups - min_prep_groups)

    # 軟性條件：備課組差異不超過 1
    prob += max_prep_groups - min_prep_groups <= 1

    # 求解
    status = prob.solve(PULP_CBC_CMD(msg=False))

    if status != 1:
        return None

    # 寫入結果
    for t in result.keys():
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