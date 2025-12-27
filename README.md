# Cloudflare Random Image API

使用 Cloudflare 规则实现的不限请求次数的随机图片接口。

## 原理

利用 Cloudflare Pages 的 URL 重写规则，将请求随机映射到预生成的静态图片文件上。

## 目录结构

- `oriImg/`: 存放原始图片素材（只需放入少量图片）。
- `img/`: 生成的随机图片库（由脚本生成，包含 00.jpg ~ ff.jpg）。
- `gen_img.py`: 生成脚本。

## 快速开始

1. 将你的图片放入 `oriImg/` 文件夹（支持 jpg/png 等，建议统一格式）。
2. 运行生成脚本：
   ```bash
   python gen_img.py
   ```
   脚本会将原始图片循环复制为 256 个文件 (`00.jpg` 到 `ff.jpg`) 放入 `img/` 目录。
3. 部署到 Cloudflare Pages。

## Cloudflare Pages 配置

在 Cloudflare Pages 的设置中，添加一条 **Rewrite Rule**（重写规则）：

- **Field**: URI Path
- **Value**:
  ```javascript
  concat("/img/", substring(uuidv4(cf.random_seed), 0, 2), ".jpg")
  ```

### 规则说明
- `uuidv4(cf.random_seed)`: 生成一个随机 UUID。
- `substring(..., 0, 2)`: 截取 UUID 的前 2 位（十六进制 `00` ~ `ff`），正好对应我们生成的 256 个文件。
- `concat(...)`: 拼接成完整路径，例如 `/img/a1.jpg`。

这样，每次访问你的 Pages 域名，都会随机显示一张图片。
