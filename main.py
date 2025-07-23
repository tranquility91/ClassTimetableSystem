# main.py
import os
from course_allocator import (allocate_courses, allocate_chinese_math,
                            calculate_basic_prep_groups, calculate_chinese_math_prep_groups, 
                            verify_chinese_math)
from data_handler import save_to_csv, update_excel_with_solution
from fet_converter import convert_to_fet_format
from table import courses, teachers

def get_user_choice():
    """獲取用戶選擇"""
    while True:
        print("\n請選擇操作：")
        print("1: 保存結果（CSV + Excel + FET格式）")
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
            # 執行完整的保存流程
            save_to_csv(best_solution)
            
            # 使用完整的 Excel 檔案路徑
            excel_path = r"C:\Users\USER\OneDrive\桌面\排課\【上傳用】113學年度特殊教育學生課程領域分組及節數一覽表(加上正式老師名字).xlsx"
            
            # 檢查檔案是否存在
            if not os.path.exists(excel_path):
                print(f"\nError: 找不到 Excel 檔案於: {excel_path}")
                print("請確認 Excel 檔案的名稱和位置是否正確。")
                continue
            
            try:
                update_excel_with_solution(best_solution, excel_path)
                output_dir = os.path.join(os.path.dirname(excel_path), "fet_export")
                convert_to_fet_format(best_solution, output_dir)
                print("所有結果都已保存完成！")
                break
            except Exception as e:
                print(f"\nError: 儲存過程中發生錯誤: {str(e)}")
                continue

        elif choice == '2':
            print("\n重新產生分配方案...")
            return main()
        else:  # choice == '3'
            print("\n程式結束")
            break

if __name__ == "__main__":
    main()