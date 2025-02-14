import os
from huggingface_hub import list_repo_files

# Hugging Face 数据集仓库信息
repo_id = "ej2/df"  # 替换为你的仓库 ID
repo_type = "dataset"

# 获取仓库文件列表
files = list_repo_files(repo_id, repo_type=repo_type)

# 定义 Hugging Face 数据集基础 URL
base_url = f"https://huggingface.co/datasets/{repo_id}/resolve/main/"

# 本地保存路径
local_dir = "downloaded_dataset"

# 遍历文件列表，生成并执行 wget 命令
for file in files:
    file_url = base_url + file  # 构造完整下载链接
    local_path = os.path.join(local_dir, file)  # 本地存储路径
    local_folder = os.path.dirname(local_path)  # 获取文件所在的本地目录
    
    # 创建所需的文件夹
    os.makedirs(local_folder, exist_ok=True)
    
    # 构造 wget 命令
    wget_cmd = f'wget -c -t 50 --timeout=10 --retry-connrefused -P "{local_folder}" "{file_url}"'
    
    # 执行 wget 命令
    print(f"Executing: {wget_cmd}")
    os.system(wget_cmd)
