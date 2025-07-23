import random
from collections import defaultdict
from typing import List, Dict, Any, Tuple

courses = [
    {"年級": 1, "課程名稱": "國語", "組別": "A", "節數": 2, "人數": 4, "人次": 8},
    {"年級": 2, "課程名稱": "國語", "組別": "A", "節數": 6, "人數": 2, "人次": 12},
    {"年級": 2, "課程名稱": "國語", "組別": "B", "節數": 2, "人數": 3, "人次": 6},
    {"年級": 3, "課程名稱": "國語", "組別": "A", "節數": 5, "人數": 5, "人次": 25},
    {"年級": 3, "課程名稱": "國語", "組別": "B", "節數": 2, "人數": 5, "人次": 10},
    {"年級": 4, "課程名稱": "國語", "組別": "A", "節數": 5, "人數": 3, "人次": 15},
    {"年級": 5, "課程名稱": "國語", "組別": "A", "節數": 5, "人數": 4, "人次": 20},
    {"年級": 6, "課程名稱": "國語", "組別": "A", "節數": 5, "人數": 3, "人次": 15},
    {"年級": 4, "課程名稱": "學習", "組別": "A", "節數": 2, "人數": 5, "人次": 10},
    {"年級": 5, "課程名稱": "學習", "組別": "B", "節數": 2, "人數": 6, "人次": 12},
    {"年級": 1, "課程名稱": "數學", "組別": "A", "節數": 2, "人數": 4, "人次": 8},
    {"年級": 2, "課程名稱": "數學", "組別": "A", "節數": 4, "人數": 2, "人次": 8},
    {"年級": 2, "課程名稱": "數學", "組別": "B", "節數": 2, "人數": 3, "人次": 6},
    {"年級": 3, "課程名稱": "數學", "組別": "A", "節數": 4, "人數": 4, "人次": 16},
    {"年級": 3, "課程名稱": "數學", "組別": "B", "節數": 2, "人數": 5, "人次": 10},
    {"年級": 4, "課程名稱": "數學", "組別": "A", "節數": 4, "人數": 3, "人次": 12},
    {"年級": 5, "課程名稱": "數學", "組別": "A", "節數": 4, "人數": 4, "人次": 16},
    {"年級": 5, "課程名稱": "數學", "組別": "B", "節數": 2, "人數": 4, "人次": 8},
    {"年級": 6, "課程名稱": "數學", "組別": "A", "節數": 4, "人數": 4, "人次": 16},
    {"年級": 6, "課程名稱": "數學", "組別": "B", "節數": 2, "人數": 3, "人次": 6},
    {"年級": 1, "課程名稱": "社會", "組別": "A", "節數": 1, "人數": 4, "人次": 4},
    {"年級": 2, "課程名稱": "社會", "組別": "B", "節數": 1, "人數": 7, "人次": 7},
    {"年級": 2, "課程名稱": "社會", "組別": "C", "節數": 1, "人數": 6, "人次": 6},
    {"年級": 2, "課程名稱": "社會", "組別": "D", "節數": 1, "人數": 4, "人次": 4},
    {"年級": 4, "課程名稱": "社會", "組別": "E", "節數": 1, "人數": 6, "人次": 6},
    {"年級": 5, "課程名稱": "社會", "組別": "F", "節數": 1, "人數": 4, "人次": 4},
    {"年級": 5, "課程名稱": "社會", "組別": "G", "節數": 1, "人數": 4, "人次": 4},
    {"年級": 6, "課程名稱": "社會", "組別": "H", "節數": 1, "人數": 5, "人次": 5},
    {"年級": 4, "課程名稱": "社會", "組別": "I", "節數": 1, "人數": 6, "人次": 6},
    {"年級": 1, "課程名稱": "動作", "組別": "A", "節數": 1, "人數": 4, "人次": 4},
    {"年級": 2, "課程名稱": "動作", "組別": "B", "節數": 1, "人數": 3, "人次": 3},
    {"年級": 3, "課程名稱": "動作", "組別": "C", "節數": 1, "人數": 4, "人次": 4},
    {"年級": 2, "課程名稱": "動作", "組別": "D", "節數": 1, "人數": 4, "人次": 4},
    {"年級": 5, "課程名稱": "動作", "組別": "E", "節數": 1, "人數": 7, "人次": 7}
]
teachers = ["A老師", "B老師", "C老師", "D老師", "E老師"]


def allocate_courses(courses: List[Dict[str, Any]], teachers: List[str]) -> Dict[str, Dict]:
    teacher_loads = defaultdict(lambda: {"節數": 0, "人次": 0, "課程": []})

    def assign_course(teacher: str, course: Dict[str, Any]):
        teacher_loads[teacher]["課程"].append(course)
        teacher_loads[teacher]["節數"] += course["節數"]
        teacher_loads[teacher]["人次"] += course["人次"]

    # 分類課程
    social_courses = [c for c in courses if c["課程名稱"] == "社會"]
    action_courses = [c for c in courses if c["課程名稱"] == "動作"]
    study_courses = [c for c in courses if c["課程名稱"] == "學習"]

    # 檢查基本課數
    if len(social_courses) != 9 or len(study_courses) != 2:
        raise ValueError("社會課應為9堂，學習課應為2堂")

    # 先行平均分配特定 5 堂課
    special = [
        next(c for c in courses if c["課程名稱"] == "社會" and c["年級"] == 4 and c["組別"] == "E"),
        next(c for c in courses if c["課程名稱"] == "社會" and c["年級"] == 5 and c["組別"] == "F"),
        next(c for c in courses if c["課程名稱"] == "社會" and c["年級"] == 5 and c["組別"] == "G"),
        next(c for c in courses if c["課程名稱"] == "社會" and c["年級"] == 2 and c["組別"] == "C"),
        next(c for c in courses if c["課程名稱"] == "動作" and c["年級"] == 2 and c["組別"] == "B"),
    ]
    # 隨機打亂老師順序，平均分配
    random.shuffle(teachers)
    for teacher, course in zip(teachers, special):
        assign_course(teacher, course)
    # 從課程列表中移除
    social_courses = [c for c in social_courses if c not in special]
    action_courses = [c for c in action_courses if c not in special]

    # 隨機打散剩餘社會課並 round-robin 分配
    random.shuffle(social_courses)
    for idx, course in enumerate(social_courses):
        t = teachers[idx % len(teachers)]
        assign_course(t, course)

    # 分配學習課
    random.shuffle(study_courses)
    # 學習課可自由分配，但確保第一位老師多一門
    assign_course(teachers[0], study_courses[0])
    assign_course(random.choice(teachers), study_courses[1])

    # 分配剩餘動作課
    for course in action_courses:
        assign_course(random.choice(teachers), course)

    return teacher_loads


##0608早版
# def allocate_courses(courses: List[Dict[str, Any]], teachers: List[str]) -> Dict[str, Dict]:
#     from collections import defaultdict
#     import random

#     teacher_loads = defaultdict(lambda: {"節數": 0, "人次": 0, "課程": []})

#     def assign_course(teacher: str, course: Dict[str, Any]):
#         teacher_loads[teacher]["課程"].append(course)
#         teacher_loads[teacher]["節數"] += course["節數"]
#         teacher_loads[teacher]["人次"] += course["人次"]

#     # 分類課程
#     social_courses = [c for c in courses if c["課程名稱"] == "社會"]
#     action_courses = [c for c in courses if c["課程名稱"] == "動作"]
#     study_courses = [c for c in courses if c["課程名稱"] == "學習"]

#     # 檢查基本課數
#     if len(social_courses) != 9 or len(study_courses) != 2:
#         raise ValueError("社會課應為9堂，學習課應為2堂")

#     # Step 1: 分配社會課（1位老師分1堂，其餘4位各2堂）
#     random.shuffle(teachers)
#     one_social_teacher = teachers[0]
#     other_teachers = teachers[1:]

#     # 給 one_social_teacher 第一堂
#     assign_course(one_social_teacher, social_courses[0])

#     # 給其他老師兩堂
#     idx = 1
#     for t in other_teachers:
#         for _ in range(2):
#             assign_course(t, social_courses[idx])
#             idx += 1

#     # 確保 F 與 G 不同老師
#     teacher_with_fg = None
#     for t, load in teacher_loads.items():
#         fg = [c for c in load["課程"] if c["課程名稱"] == "社會" and c["組別"] in ("F", "G")]
#         if len(fg) == 2:
#             teacher_with_fg = t
#             break
#     if teacher_with_fg:
#         # 取出 G
#         g_course = next(c for c in teacher_loads[teacher_with_fg]["課程"] if c["組別"] == "G")
#         # 找其他老師可交換
#         for t2 in other_teachers:
#             if t2 == teacher_with_fg:
#                 continue
#             socials2 = [c for c in teacher_loads[t2]["課程"] if c["課程名稱"] == "社會" and c["組別"] not in ("F", "G")]
#             if socials2:
#                 swap_course = socials2[0]
#                 # 移除並更新
#                 teacher_loads[teacher_with_fg]["課程"].remove(g_course)
#                 teacher_loads[teacher_with_fg]["節數"] -= g_course["節數"]
#                 teacher_loads[teacher_with_fg]["人次"] -= g_course["人次"]

#                 teacher_loads[t2]["課程"].remove(swap_course)
#                 teacher_loads[t2]["節數"] -= swap_course["節數"]
#                 teacher_loads[t2]["人次"] -= swap_course["人次"]

#                 # 重新分配
#                 assign_course(teacher_with_fg, swap_course)
#                 assign_course(t2, g_course)
#                 break

#     # Step 2: 分配學習課
#     assign_course(one_social_teacher, study_courses[0])
#     random_teacher = random.choice(teachers)
#     assign_course(random_teacher, study_courses[1])

#     # Step 3: 分配動作課（不設限）
#     for course in action_courses:
#         assign_course(random.choice(teachers), course)

#     return teacher_loads


##有課後一定必須的
# def allocate_courses(courses: List[Dict[str, Any]], teachers: List[str]) -> Dict[str, Dict]:
#     teacher_loads = defaultdict(lambda: {"節數": 0, "人次": 0, "課程": []})

#     def assign_course(teacher: str, course: Dict[str, Any]):
#         teacher_loads[teacher]["課程"].append(course)
#         teacher_loads[teacher]["節數"] += course["節數"]
#         teacher_loads[teacher]["人次"] += course["人次"]

#     # 分類課程
#     social_courses = [c for c in courses if c["課程名稱"] == "社會"]
#     action_courses = [c for c in courses if c["課程名稱"] == "動作"]
#     study_courses = [c for c in courses if c["課程名稱"] == "學習"]

#     # 檢查基本課數
#     if len(social_courses) != 9 or len(study_courses) != 2:
#         raise ValueError("社會課應為9堂，學習課應為2堂")

#     # Step 1: 分配社會課（1位老師分1堂，其餘4位各2堂）
#     random.shuffle(teachers)
#     one_social_teacher = teachers[0]
#     other_teachers = teachers[1:]

#     social_index = 0
#     assign_course(one_social_teacher, social_courses[social_index])
#     social_index += 1
#     for t in other_teachers:
#         for _ in range(2):
#             assign_course(t, social_courses[social_index])
#             social_index += 1

#     # Step 2: 分配學習課
#     assign_course(one_social_teacher, study_courses[0])
#     assign_course(random.choice(teachers), study_courses[1])

#     # Step 3: 分配動作課（不設限）
#     for course in action_courses:
#         assign_course(random.choice(teachers), course)

#     # Step 4: 額外限制 — 除了分到1年級動作的老師，其他四人各分到指定一堂國數課
#     special_courses_meta = [
#         {"課程名稱": "國語", "年級": 1, "組別": "A"},
#         {"課程名稱": "國語", "年級": 2, "組別": "B"},
#         {"課程名稱": "數學", "年級": 1, "組別": "A"},
#         {"課程名稱": "數學", "年級": 2, "組別": "B"},
#     ]

#     # 找出誰有 1年級動作課
#     action_grade1 = [c for c in action_courses if c["年級"] == 1]
#     teacher_with_grade1_action = None
#     for teacher, load in teacher_loads.items():
#         if any(c in action_grade1 for c in load["課程"]):
#             teacher_with_grade1_action = teacher
#             break

#     remaining_teachers = [t for t in teachers if t != teacher_with_grade1_action]
#     random.shuffle(remaining_teachers)

#     def find_course(subject, grade, group):
#         for c in courses:
#             if c["課程名稱"] == subject and c["年級"] == grade and c["組別"] == group:
#                 return c
#         return None

#     for t, meta in zip(remaining_teachers, special_courses_meta):
#         course = find_course(meta["課程名稱"], meta["年級"], meta["組別"])
#         if course is None:
#             raise ValueError(f"找不到指定課程：{meta}")
#         assign_course(t, course)

#     return teacher_loads




#無課外一定必須的版本
# def allocate_courses(courses: List[Dict[str, Any]], teachers: List[str]) -> Dict[str, Dict]:
#     from collections import defaultdict
#     import random

#     teacher_loads = defaultdict(lambda: {"節數": 0, "人次": 0, "課程": []})

#     def assign_course(teacher: str, course: Dict[str, Any]):
#         teacher_loads[teacher]["課程"].append(course)
#         teacher_loads[teacher]["節數"] += course["節數"]
#         teacher_loads[teacher]["人次"] += course["人次"]

#     # 分類課程
#     social_courses = [c for c in courses if c["課程名稱"] == "社會"]
#     action_courses = [c for c in courses if c["課程名稱"] == "動作"]
#     study_courses = [c for c in courses if c["課程名稱"] == "學習"]

#     # 檢查基本課數
#     if len(social_courses) != 9 or len(study_courses) != 2:
#         raise ValueError("社會課應為9堂，學習課應為2堂")

#     # Step 1: 分配社會課（1位老師分1堂，其餘4位各2堂）
#     random.shuffle(teachers)
#     one_social_teacher = teachers[0]
#     other_teachers = teachers[1:]

#     social_index = 0
#     assign_course(one_social_teacher, social_courses[social_index])
#     social_index += 1
#     for t in other_teachers:
#         for _ in range(2):
#             assign_course(t, social_courses[social_index])
#             social_index += 1

#     # Step 2: 分配學習課
#     assign_course(one_social_teacher, study_courses[0])
#     remaining_study = study_courses[1]
#     random_teacher = random.choice(teachers)
#     assign_course(random_teacher, remaining_study)

#     # Step 3: 分配動作課（不設限）
#     for course in action_courses:
#         assign_course(random.choice(teachers), course)

#     return teacher_loads



def verify_allocation(teacher_loads: Dict[str, Dict]) -> Tuple[bool, str]:
    """驗證分配是否符合所有規則"""
    for teacher, load in teacher_loads.items():
        # 計算每種課程的數量
        social_count = sum(1 for c in load["課程"] if c["課程名稱"] == "社會")
        action_count = sum(1 for c in load["課程"] if c["課程名稱"] == "動作")
        study_count = sum(1 for c in load["課程"] if c["課程名稱"] == "學習")
        
        # 檢查是否有老師只有1堂社會課
        if social_count == 1:
            if not (action_count == 1 and study_count == 1):
                return False, f"{teacher} 有1堂社會課但動作({action_count})和學習({study_count})課程分配不正確"
        
        # 檢查其他老師是否都有2堂社會課
        elif social_count != 2:
            return False, f"{teacher} 社會課數量不正確 ({social_count})"
        
        # 檢查沒有老師拿到超過1堂學習課
        if study_count > 1:
            return False, f"{teacher} 有超過1堂學習課 ({study_count})"
            
    return True, "分配符合所有規則"

# 主程式
def main():
    # 重複分配直到符合所有規則
    max_attempts = 1000
    attempt = 0
    
    while attempt < max_attempts:
        teacher_loads = allocate_courses(courses, ["A老師", "B老師", "C老師", "D老師", "E老師"])
        is_valid, message = verify_allocation(teacher_loads)
        
        if is_valid:
            print("\n成功分配課程！")
            print("\n老師負責的課程:")
            for teacher, load in teacher_loads.items():
                print(f"{teacher}:")
                for course in load["課程"]:
                    print(f"  - {course['課程名稱']} {course['組別']} 節數: {course['節數']}, 人次: {course['人次']}")
                print(f"  總節數: {load['節數']}, 總人次: {load['人次']}")
            return teacher_loads
            
        attempt += 1
    
    raise Exception("無法找到符合規則的分配方案")

if __name__ == "__main__":
    main()
    
    



