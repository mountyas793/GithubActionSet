# -*- coding: utf-8 -*-
# @Project: gihub_action_sanyaosa
# @File: main.py
# @Author: #3sanas
# @Date: 2025/12/15 10:34
# @Desc: 夸克签到主入口模块

from .config import get_email_config, get_env
from .email_sender import send_email
from .quark import Quark
from .utils import parse_quark_url


def main():
    """
    主函数，执行夸克签到流程
    :return: 签到结果字符串
    """
    msg = ""
    cookie_quark = get_env()

    print("✅ 检测到共", len(cookie_quark), "个夸克账号\n, params:", cookie_quark)

    i = 0
    while i < len(cookie_quark):
        # 获取user_data参数
        user_data = {}  # 用户信息
        for a in cookie_quark[i].replace(" ", "").split(";"):
            if not a == "":
                user_data.update({a[0 : a.index("=")]: a[a.index("=") + 1 :]})

        # 从url参数中提取额外信息
        if "url" in user_data:
            url_params = parse_quark_url(user_data["url"])
            user_data.update(url_params)

        # 开始任务
        log = f"🙍🏻‍♂️ 第{i + 1}个账号"
        msg += log
        # 执行签到
        log = Quark(user_data).do_sign()
        msg += log + "\n"
        i += 1

    print("----------夸克网盘签到完毕----------")
    print(msg)

    # 获取邮件配置
    email_config = get_email_config()
    email_subject = email_config["email_subject"]

    # 发送邮件
    if email_config["enable_email"]:
        send_email(msg, email_subject, email_config)
    else:
        print("❌ 邮件发送已禁用")

    return msg[:-1]


if __name__ == "__main__":
    print("----------夸克网盘开始签到----------")
    result = main()
    # 如果邮件发送失败，输出结果到控制台
    print("----------程序执行完毕----------")
