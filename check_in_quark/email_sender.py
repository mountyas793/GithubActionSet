# -*- coding: utf-8 -*-
# @Project: gihub_action_sanyaosa
# @File: email_sender.py
# @Author: #3sanas
# @Date: 2025/12/15 10:38
# @Desc: 邮件发送模块

import email.utils
import smtplib
import socket
from email.header import Header
from email.mime.text import MIMEText


def send_email(
    body, subject="GitHub Action Status - QuarkSignResult", email_config=None
):
    """
    发送邮件
    :param body: 邮件内容
    :param subject: 邮件主题
    :param email_config: 邮件配置字典
    :return: 发送成功返回True，失败返回False
    """
    try:
        # 验证必要的邮件配置
        if not email_config or not all(
            [
                email_config["smtp_server"],
                email_config["smtp_port"],
                email_config["email_username"],
                email_config["email_password"],
                email_config["email_receiver"],
            ]
        ):
            print("❌ 邮件配置不完整，跳过发送")
            return False

        # 严格按照RFC标准设置发件人
        sender_name = "QuarkSignBot"
        sender_address = email_config["email_username"]
        # 格式化发件人地址
        formatted_sender = email.utils.formataddr((sender_name, sender_address))

        # 创建邮件内容
        message = MIMEText(body, "plain")
        message["From"] = formatted_sender
        message["To"] = Header(email_config["email_receiver"])
        message["Subject"] = Header(subject, "utf-8")

        # 发送邮件
        with smtplib.SMTP_SSL(
            email_config["smtp_server"], email_config["smtp_port"]
        ) as server:
            server.login(email_config["email_username"], email_config["email_password"])
            server.sendmail(
                email_config["email_username"],
                [email_config["email_receiver"]],
                message.as_string(),
            )

        print("✅ 签到结果邮件已发送")
        return True

    except smtplib.SMTPAuthenticationError as e:
        print(f"❌❌❌❌ 邮件认证失败: {str(e)}")
        print("提示：QQ邮箱需要使用授权码而非密码，请到QQ邮箱设置中生成授权码")
        return False
    except smtplib.SMTPServerDisconnected as e:
        print(f"❌❌ 服务器意外断开连接: {str(e)}")
        print("提示：可能是网络问题或服务器限制，请稍后重试")
        return False
    except socket.timeout as e:
        print(f"❌❌ 连接超时: {str(e)}")
        print("提示：SMTP服务器响应超时，请检查网络连接")
        return False
    except Exception as e:
        # 特殊处理 QQ 邮箱的已知问题
        if "(-1, b'\x00\x00\x00')" in str(e):
            print("⚠️ 邮件发送出现已知问题，但邮件可能已成功发送")
            return True
        print(f"❌❌ 邮件发送失败: {str(e)}")
        return False
