import os
import shutil
from pathlib import Path
from itertools import cycle

# 配置
SOURCE_DIR = Path("oriImg")
OUTPUT_DIR = Path("img")
# 生成 256 个文件 (00.jpg ~ ff.jpg)
# 这样可以使用 Cloudflare 规则 substring(uuid, 0, 2)
NUM_FILES = 256 

def ensure_dir(path: Path):
    if not path.exists():
        path.mkdir(parents=True)

def main():
    if not SOURCE_DIR.exists():
        print(f"Error: Source directory '{SOURCE_DIR}' does not exist.")
        return

    # 1. 获取所有图片文件
    # 支持常见的图片格式
    extensions = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
    images = sorted([
        f for f in SOURCE_DIR.iterdir() 
        if f.is_file() and f.suffix.lower() in extensions
    ])

    if not images:
        print(f"No images found in {SOURCE_DIR}")
        return

    print(f"Found {len(images)} images.")
    
    # 2. 准备输出目录
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    ensure_dir(OUTPUT_DIR)

    # 3. 循环复制图片
    img_cycle = cycle(images)
    
    print(f"Generating {NUM_FILES} files in {OUTPUT_DIR}...")
    
    for i in range(NUM_FILES):
        src_img = next(img_cycle)
        # 生成十六进制文件名: 00.jpg, 01.jpg ... ff.jpg
        # 统一使用源文件的扩展名，或者为了 API 统一性，可以考虑重命名为 .jpg (如果源文件格式兼容)
        # 这里为了简单和兼容性，我们强制输出为 .jpg，
        # 注意：如果源文件是 png 改名 jpg 浏览器通常也能显示，但最好保持一致。
        # 既然用户提供的都是 jpg，我们这里固定用 .jpg。
        # 如果需要更通用的做法，可以在规则里不带后缀，利用 Content-Type，
        # 但静态文件托管通常依赖后缀推断 Content-Type。
        # 既然是 Demo，我们假设输出都是 .jpg
        file_name = f"{i:02x}.jpg"
        dest_path = OUTPUT_DIR / file_name
        
        shutil.copy(src_img, dest_path)
        
    print("Done.")

if __name__ == "__main__":
    main()
