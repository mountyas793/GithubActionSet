# -*- coding: utf-8 -*-
# @Project: gihub_action_sanyaosa
# @File: __init__.py
# @Author: #3sanas
# @Date: 2025/12/15 10:38
# @Desc: 夸克签到模块统一入口

"""
夸克自动签到模块

该模块提供了夸克网盘自动签到的功能，支持多账户签到和结果邮件通知。
"""

from .config import get_email_config, get_env
from .email import send_email
from .main import main
from .quark import Quark
from .utils.url_parser import parse_quark_url

__all__ = [
    "main",
    "Quark",
    "send_email",
    "get_env",
    "get_email_config",
    "parse_quark_url",
]
