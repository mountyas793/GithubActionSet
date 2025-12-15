# -*- coding: utf-8 -*-
# @Project: gihub_action_sanyaosa
# @File: config.py
# @Author: #3sanas
# @Date: 2025/12/15 10:38
# @Desc: 配置管理模块，负责环境变量读取和配置管理

import os
import re
import sys

# 尝试导入dotenv库（用于本地调试加载.env文件）
try:
    from dotenv import load_dotenv
    # 加载.env文件（如果存在）
    load_dotenv()
    print("✅ 成功加载.env文件")
except ImportError:
    print("ℹ️  未找到python-dotenv库，跳过.env文件加载")
    print("   安装命令：pip install python-dotenv")


def get_env():
    """
    从环境变量中获取夸克签到的配置信息
    :return: 包含所有用户配置的列表
    """
    try:
        # 判断 COOKIE_QUARK 是否存在于环境变量
        if "COOKIE_QUARK" in os.environ:
            # 读取系统变量以 \n 或 && 分割变量
            cookie_list = re.split("\n|&&", os.environ.get("COOKIE_QUARK"))
        else:
            # 标准日志输出
            print("❌未添加COOKIE_QUARK变量")
            print("   本地调试：请在.env文件中设置COOKIE_QUARK")
            print("   GitHub Actions：请在Secrets中设置COOKIE_QUARK")
            # 脚本退出
            sys.exit(0)

        return cookie_list
    except Exception as e:
        print(f"❌获取COOKIE_QUARK变量失败: {e}")
        sys.exit(1)


def get_email_config():
    """
    获取邮件配置信息
    :return: 邮件配置字典
    """
    return {
        "smtp_server": os.environ.get("SMTP_SERVER", "smtp.qq.com"),
        "smtp_port": int(os.environ.get("SMTP_PORT", 465)),
        "email_username": os.environ.get("EMAIL_USERNAME"),
        "email_password": os.environ.get("EMAIL_PASSWORD"),
        "email_receiver": os.environ.get("EMAIL_RECEIVER"),
        "enable_email": os.environ.get("ENABLE_EMAIL", "true").lower() == "true",
        "email_subject": os.environ.get(
            "EMAIL_SUBJECT", "GitHub Action 完成通知 - 夸克签到结果"
        ),
    }
