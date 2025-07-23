# fet_converter.py
import csv
import os
from datetime import datetime

def convert_to_fet_format(solution, output_dir=None):
    """將分配結果轉換為FET可匯入的CSV格式"""
    if output_dir is None:
        output_dir = os.path.join(os.getcwd(), "fet_export")
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 1. 生成教師CSV
    create_teachers_csv(solution, output_dir, timestamp)
    
    # 2. 生成科目CSV
    create_subjects_csv(solution, output_dir, timestamp)
    
    # 3. 生成學生/年級組別CSV
    create_students_csv(solution, output_dir, timestamp)
    
    # 4. 生成活動CSV
    create_activities_csv(solution, output_dir, timestamp)
    
    print(f"\nFET格式檔案已生成於 {output_dir} 資料夾中")

def create_teachers_csv(solution, output_dir, timestamp):
    """生成教師CSV"""
    filepath = os.path.join(output_dir, f'teachers_{timestamp}.csv')
    with open(filepath, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['Name'])
        for teacher in solution.keys():
            writer.writerow([teacher])

def create_subjects_csv(solution, output_dir, timestamp):
    """生成科目CSV"""
    subjects = set()
    for load in solution.values():
        for course in load['課程']:
            subjects.add(course['課程名稱'])
    
    filepath = os.path.join(output_dir, f'subjects_{timestamp}.csv')
    with open(filepath, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['Name'])
        for subject in sorted(subjects):
            writer.writerow([subject])

def create_students_csv(solution, output_dir, timestamp):
    """生成學生/年級組別CSV"""
    groups = set()
    for load in solution.values():
        for course in load['課程']:
            groups.add(f"{course['年級']}年級{course['組別']}")
    
    filepath = os.path.join(output_dir, f'students_{timestamp}.csv')
    with open(filepath, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['Year', 'Number_of_Students'])
        for group in sorted(groups):
            writer.writerow([group, 30])  # 假設每組30人

def create_activities_csv(solution, output_dir, timestamp):
    """生成活動CSV"""
    filepath = os.path.join(output_dir, f'activities_{timestamp}.csv')
    with open(filepath, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['Activity_Id', 'Subject', 'Teacher', 'Students', 
                        'Duration', 'Total_Duration', 'Active'])
        
        activity_id = 1
        for teacher, load in solution.items():
            for course in load['課程']:
                group_name = f"{course['年級']}年級{course['組別']}"
                writer.writerow([
                    activity_id,
                    course['課程名稱'],
                    teacher,
                    group_name,
                    course['節數'],
                    course['節數'],
                    'true'
                ])
                activity_id += 1