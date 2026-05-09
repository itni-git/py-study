import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

class FileRenamerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("파일 이름 일괄 변경 도구")
        self.root.geometry("500x250")
        
        # 폴더 경로 변수
        self.folder_path = tk.StringVar()
        
        # UI 요소 배치
        self.create_widgets()

    def create_widgets(self):
        # 1. 폴더 선택 섹션
        tk.Label(self.root, text="대상 폴더:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        tk.Entry(self.root, textvariable=self.folder_path, width=40).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(self.root, text="찾아보기...", command=self.browse_folder).grid(row=0, column=2, padx=10, pady=10)

        # 2. 변경 규칙 섹션
        tk.Label(self.root, text="찾을 문자열:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.old_text_entry = tk.Entry(self.root, width=40)
        self.old_text_entry.grid(row=1, column=1, padx=10, pady=5, columnspan=2, sticky="w")

        tk.Label(self.root, text="바꿀 문자열:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.new_text_entry = tk.Entry(self.root, width=40)
        self.new_text_entry.grid(row=2, column=1, padx=10, pady=5, columnspan=2, sticky="w")

        # 3. 실행 버튼
        self.rename_button = tk.Button(self.root, text="이름 변경 실행", command=self.run_rename, 
                                       bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), height=2)
        self.rename_button.grid(row=3, column=0, columnspan=3, pady=20, sticky="ew", padx=10)

    def browse_folder(self):
        selected_dir = filedialog.askdirectory()
        if selected_dir:
            self.folder_path.set(selected_dir)

    def run_rename(self):
        folder = self.folder_path.get()
        old_pattern = self.old_text_entry.get()
        new_pattern = self.new_text_entry.get()

        if not folder or not Path(folder).is_dir():
            messagebox.showwarning("경고", "올바른 폴더 경로를 선택해주세요.")
            return
        
        if not old_pattern:
            messagebox.showwarning("경고", "찾을 문자열을 입력해주세요.")
            return

        try:
            path = Path(folder)
            count = 0
            for file_path in path.iterdir():
                if file_path.is_file() and old_pattern in file_path.name:
                    new_name = file_path.name.replace(old_pattern, new_pattern)
                    new_file_path = file_path.with_name(new_name)
                    file_path.rename(new_file_path)
                    count += 1
            
            messagebox.showinfo("완료", f"총 {count}개의 파일 이름이 변경되었습니다.")
        except Exception as e:
            messagebox.showerror("오류", f"작업 중 오류가 발생했습니다:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileRenamerGUI(root)
    root.mainloop()
