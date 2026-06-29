import os
import customtkinter as ctk
from customtkinter import filedialog
from docling.document_converter import DocumentConverter
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from pptx import Presentation
from pptx.util import Inches, Pt


def process_files(file_paths, persona):
    if not file_paths:
        return

    llm = Ollama(model="llama3")

    for file_path in file_paths:
        try:
            # 1. 문서 변환기로 참조 제안서 읽기
            converter = DocumentConverter()
            result = converter.convert(file_path)
            document = result.document
            extracted_text = document.export_to_markdown()

            # 2. 페르소나 적용하기
            template = f"""
            당신은 {persona}입니다. 다음 문서를 바탕으로 격식 있고 설득력 있는 제안서 요약본을 작성해 주세요.

            문서 내용:
            {{content}}
            """

            prompt = PromptTemplate.from_template(template)
            chain = prompt | llm
            processed_content = chain.invoke({"content": extracted_text})

            # 3. 새로운 PPT 생성 및 가공된 내용 넣기
            prs = Presentation()
            blank_layout = prs.slide_layouts[6]
            slide = prs.slides.add_slide(blank_layout)

            txBox = slide.shapes.add_textbox(
                Inches(1), Inches(1), Inches(8), Inches(5.5)
            )
            tf = txBox.text_frame
            tf.word_wrap = True

            p = tf.paragraphs[0]
            p.text = "전문 제안서 요약"
            p.font.size = Pt(24)

            p = tf.add_paragraph()
            p.text = processed_content
            p.font.size = Pt(14)

            base_name = os.path.splitext(os.path.basename(file_path))[0]
            prs.save(f"새로운제안서_{base_name}.pptx")
            print(f"{base_name} 제안서 생성이 완료되었습니다!")
        except Exception as e:
            print(f"파일 처리 중 오류 발생 ({file_path}): {e}")


def generate_from_folder():
    folder_path = filedialog.askdirectory()
    if not folder_path:
        return

    persona = persona_input.get("1.0", "end-1c").strip()
    if not persona:
        persona = "전문 제안서 작성자"

    pdf_files = [
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if f.lower().endswith(".pdf")
    ]
    process_files(pdf_files, persona)


def generate_from_files():
    file_paths = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
    if not file_paths:
        return

    persona = persona_input.get("1.0", "end-1c").strip()
    if not persona:
        persona = "전문 제안서 작성자"

    process_files(file_paths, persona)


# GUI 구성
app = ctk.CTk()
app.title("제안서 생성기")
app.geometry("400x500")

ctk.CTkLabel(app, text="페르소나 설정:").pack(pady=(20, 5))
persona_input = ctk.CTkTextbox(app, height=100, width=300)
persona_input.insert("1.0", "전문 제안서 작성자")
persona_input.pack(pady=10)

btn_folder = ctk.CTkButton(
    app, text="폴더 선택 및 모든 PDF 처리", command=generate_from_folder
)
btn_folder.pack(pady=20)

btn_files = ctk.CTkButton(
    app, text="여러 PDF 파일 선택 및 처리", command=generate_from_files
)
btn_files.pack(pady=20)

app.mainloop()
