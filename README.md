# gihub-action-sanyaosa

## 项目简介
本项目 `gihub-action-sanyaosa` 是一个Python项目，主要功能涉及京东签到操作，具体可查看 `daily_sign.py` 文件。当前版本为 `0.1.0`，支持Python 3.11及以上版本。

## 环境要求
- Python版本：3.11及以上
- 依赖库：`requests>=2.32.3`，可通过 `pyproject.toml` 文件进行依赖管理。

## 安装依赖
```bash
pip install -r requirements.txt
```

## 使用uv管理
### 安装uv
确保你已经安装了 `uv`，如果没有安装，可以通过以下命令进行安装：
```bash
pip install uv
```

### 使用uv运行项目
你可以使用 `uv` 来管理和运行项目，以下是基本的使用示例：
```bash
uv run daily_sign.py
```

## 文件说明
- `.gitignore`：定义Git忽略的文件和目录。
- `.python-version`：指定项目使用的Python版本。
- `pyproject.toml`：项目依赖管理文件。

## 注意事项
- 运行脚本前，请先安装项目依赖和 `uv`。