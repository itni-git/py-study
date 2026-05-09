import os
from pathlib import Path

def rename_files(directory_path, old_pattern, new_pattern):
    """
    폴더 내의 파일명에서 특정 문자열을 찾아 변경합니다.
    """
    path = Path(directory_path)
    
    if not path.is_dir():
        print(f"오류: {directory_path}는 유효한 디렉토리가 아닙니다.")
        return

    count = 0
    for file_path in path.iterdir():
        if file_path.is_file():
            if old_pattern in file_path.name:
                new_name = file_path.name.replace(old_pattern, new_pattern)
                new_file_path = file_path.with_name(new_name)
                
                # 파일 이름 변경
                file_path.rename(new_file_path)
                print(f"변경됨: {file_path.name} -> {new_name}")
                count += 1
    
    print(f"총 {count}개의 파일 이름이 변경되었습니다.")

if __name__ == "__main__":
    # 사용 예시:
    # 현재 폴더(.)에서 'xxxx'를 'test'로 변경
    target_dir = "."
    search_str = "xxxx"
    replace_str = "test"
    
    rename_files(target_dir, search_str, replace_str)
