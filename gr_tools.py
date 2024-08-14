import os

import llm
from PyPDF2 import PdfReader

local_file_text = ''

prj_name = 'unbox_yolov5_deepsort_counting-main'
prj_path = f'/Users/cjzy/python-ws/aigc/github/{prj_name}'


def get_all_files_in_folder(folder_path):
    """
    读取项目下所有文件
    :param folder_path: 项目根目录
    :return: 项目下所有文件列表
    """
    file_list = []
    anon_dirs = []
    for root, dirs, files in os.walk(folder_path):
        if root in anon_dirs:
            anon_dirs.extend([os.path.join(root, dir) for dir in dirs])
        else:
            anon_dirs.extend([os.path.join(root, dir) for dir in dirs if dir.startswith('.')])

        if root in anon_dirs:
            continue
        for file in files:
            if not file.startswith('.'):
                file_list.append(os.path.join(root, file))
    return file_list

# 获取整个项目代码，拼接到 local_file_text 中
# file_list = get_all_files_in_folder(prj_path)
# for i, file_name in enumerate(file_list):
#     file_path = file_name.split(prj_name)[1]
#     local_file_text += f'文件名：{file_path}\n内容：\n'
#
#     with open(file_name, 'r', encoding='utf-8') as f:
#         file_content = f.read()
#     local_file_text += file_content


def get_file_content(file_path_list):
    """
    读取上传的文件
    :param file_path: 文件列表
    :return:
    """
    global local_file_text
    # 获取pdf文档内容并存入text
    for file_path in file_path_list:  # 读取每个文件
        file_name = os.path.basename(file_path)  # 获取文件名
        print(file_name)
        local_file_text += f'文件名：{file_name}\n论文正文：\n'

        pdf_reader = PdfReader(file_path)
        print(len(pdf_reader.pages))

        for page in pdf_reader.pages:  # 获取资料正文
            local_file_text += page.extract_text()

    print('done')


def chat(user_in_text: str, prj_chatbot: list):
    """
    大模型chat
    :param user_in_text: 用户提问
    :param prj_chatbot: 历史消息
    :return:
    """
    response = llm.chat(user_in_text, prj_chatbot, local_file_text)

    prj_chatbot.append([user_in_text, ''])
    yield prj_chatbot

    for chunk_content in response:
        prj_chatbot[-1][1] = f'{prj_chatbot[-1][1]}{chunk_content}'
        yield prj_chatbot