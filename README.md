# Enana

一个轻量级的Python UI库，用于生成高质量的图片形式UI界面。

## 项目简介

Enana是一个基于Python的UI库，专注于生成图片形式的用户界面。它提供了一套简洁易用的API，允许开发者通过Python代码或JSON配置来创建各种UI组件，并将其渲染为高质量的图片。Enana适用于需要生成静态UI图片的场景，如报告生成、邮件模板、社交媒体图片等。

### 核心功能

- 支持多种UI组件（Container, Row, Column, Text, Image等）
- 支持从JSON配置生成UI界面
- 多进程并行渲染，提高生成速度
- 支持文本自动换行和样式定制
- 支持多种图片加载方式（网络URL、本地文件、base64编码）
- 支持响应式布局
- 支持圆角、边距、填充等样式属性

## 快速开始

### 安装

```bash
pip install enana
```

### 基本使用

#### 使用Python代码创建UI

```python
from enana import Page, Container, Text, Column, Row, Image
from pathlib import Path

# 创建UI组件
page = Page(
    child=Column(
        children=[
            Container(
                color=(255, 100, 100, 255),
                padding=20,
                border_radius=10,
                child=Text(
                    text="欢迎使用Enana UI",
                    font_size=24,
                    color=(255, 255, 255, 255)
                )
            ),
            Row(
                children=[
                    Image(
                        url="https://www.gstatic.com/images/branding/searchlogo/ico/favicon.ico",
                        width=100,
                        height=100,
                        size="cover"
                    ),
                    Image(
                        url="https://www.gstatic.com/images/branding/searchlogo/ico/favicon.ico",
                        width=100,
                        height=100,
                        size="contain"
                    )
                ]
            ),
            Text(
                text="这是一段示例文本，展示了如何在Enana UI中使用文本组件。文本可以自动换行，并且可以设置字体大小和颜色。",
                max_width=300,
                font_size=16,
                color=(50, 50, 50, 255)
            )
        ]
    )
)

# 渲染为图片
page.paint(scale=2.0, filename=Path("output.png"))
```

#### 使用JSON配置创建UI

```json
{
  "type": "Page",
  "child": {
    "type": "Column",
    "children": [
      {
        "type": "Container",
        "color": [255, 100, 100, 255],
        "padding": 20,
        "border_radius": 10,
        "child": {
          "type": "Text",
          "text": "欢迎使用Enana UI",
          "font_size": 24,
          "color": [255, 255, 255, 255]
        }
      }
    ]
  }
}
```

```python
from enana import Page
from pathlib import Path
import json

# 加载JSON配置
with open("example.json", "r") as f:
    config = json.load(f)

# 创建Page对象
page = Page.from_json(config)

# 渲染为图片
page.paint(scale=2.0, filename=Path("output.png"))
```

## 安装方法

### 使用pip安装

```bash
pip install enana
```

### 从源码安装

```bash
git clone https://github.com/Parallel-SEKAI/Enana.git
cd Enana
pip install -e .
```

## 组件说明

### Container

容器组件，用于包裹其他组件并提供样式属性。

#### 属性

- `width`: 容器宽度
- `height`: 容器高度
- `color`: 容器背景颜色（RGBA元组）
- `padding`: 内边距
- `margin`: 外边距
- `border_radius`: 圆角半径
- `child`: 子组件

### Row

水平布局组件，用于将子组件水平排列。

#### 属性

- `width`: 行宽度
- `height`: 行高度
- `color`: 背景颜色
- `padding`: 内边距
- `margin`: 外边距
- `border_radius`: 圆角半径
- `children`: 子组件列表

### Column

垂直布局组件，用于将子组件垂直排列。

#### 属性

- `width`: 列宽度
- `height`: 列高度
- `color`: 背景颜色
- `padding`: 内边距
- `margin`: 外边距
- `border_radius`: 圆角半径
- `children`: 子组件列表

### Text

文本组件，用于显示文本内容。

#### 属性

- `text`: 文本内容
- `font`: 字体名称
- `font_size`: 字体大小
- `max_width`: 最大宽度（超过则自动换行）
- `color`: 文本颜色

### Image

图片组件，用于显示图片。

#### 属性

- `url`: 图片URL（支持http(s)、file和base64格式）
- `width`: 图片宽度
- `height`: 图片高度
- `size`: 图片缩放方式（cover, contain, default）

## 项目结构

```
enana/
├── __init__.py          # 导出公共API
├── column.py            # Column组件实现
├── container.py         # Container组件实现
├── generator.py         # 图片生成逻辑
├── image.py             # Image组件实现
├── page.py              # Page组件实现
├── painter.py           # 绘制逻辑
├── row.py               # Row组件实现
├── text.py              # Text组件实现
├── typing.py            # 类型定义
└── utils.py             # 工具函数

tests/
├── test_enana.py        # 测试用例
└── test_json.py         # JSON解析测试

docs.md                 # API文档
example.json             # 示例JSON配置
widget.schema.json       # JSON Schema定义
```

## API文档

完整的API文档请查看 [docs.md](docs.md) 文件。

## 贡献指南

我们欢迎社区贡献！如果您想为Enana贡献代码，请遵循以下步骤：

1. Fork本仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个Pull Request

### 开发规范

- 代码风格遵循PEP 8
- 所有函数和方法必须添加类型注解
- 所有公共API必须添加文档字符串
- 提交前请运行测试 (`pytest tests/`)

## 许可证

Enana采用MIT许可证，详情请查看 [LICENSE](LICENSE) 文件。

## 联系方式

- GitHub: [https://github.com/Parallel-SEKAI/Enana](https://github.com/Parallel-SEKAI/Enana)
- Issues: [https://github.com/Parallel-SEKAI/Enana/issues](https://github.com/Parallel-SEKAI/Enana/issues)

## 致谢

感谢所有为Enana做出贡献的开发者！
