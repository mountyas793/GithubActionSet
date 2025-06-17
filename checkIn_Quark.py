# -*- coding: utf-8 -*-
# @Project: gihub_action_sanyaosa
# @File: checkIn_Quark.py
# @Author: 卯三
# @Date: 2025/06/16 16:43
# @Desc: 夸克自动签到
"""
V2版-目前有效
使用移动端接口修复每日自动签到，移除原有的“登录验证”，参数有效期未知
抓包流程：
    【手机端】
    ①打开抓包，手机端访问抽奖页
    ②找到url为 https://drive-m.quark.cn/1/clouddrive/act/growth/reward 的请求信息
    ③复制整段url，该链接后面必须要有参数: kps sign vcode，粘贴到环境变量
    环境变量名为 COOKIE_QUARK 多账户用 回车 或 && 分开
    user字段是用户名 (可是随意填写，多账户方便区分)
    例如: user=张三; url=https://drive-m.quark.cn/1/clouddrive/act/growth/reward?xxxxxx=xxxxxx&kps=abcdefg&sign=hijklmn&vcode=111111111;
    旧版环境变量格式也兼容，例如: 
    user=sanyaosa3; 
    kps_wg=AAQRsBGzCtZ4qNDt6sWj2uzqjqp/Q==; 
    sign_wg=AARVuvfjTfc=; 
    vcode=1750065928578;
"""

import email.utils  # 新增导入
import os
import re
import smtplib
import socket
import sys
from email.header import Header
from email.mime.text import MIMEText

import requests

# 获取环境变量
cookie = os.environ.get('COOKIE_QUARK')

# 测试用环境变量
# os.environ['COOKIE_QUARK'] = 'url='

# 获取环境变量
def get_env():
    # 判断 COOKIE_QUARK是否存在于环境变量
    if "COOKIE_QUARK" in os.environ:
        # 读取系统变量以 \n 或 && 分割变量
        cookie_list = re.split('\n|&&', os.environ.get('COOKIE_QUARK'))
    else:
        # 标准日志输出
        print('❌未添加COOKIE_QUARK变量')
        # send('夸克自动签到', '❌未添加COOKIE_QUARK变量')
        # 脚本退出
        sys.exit(0)

    return cookie_list

class Quark:
    '''
    Quark类封装了签到、领取签到奖励的方法
    '''
    def __init__(self, user_data):
        '''
        初始化方法
        :param user_data: 用户信息，用于后续的请求
        '''
        self.param = user_data

    def convert_bytes(self, b):
        '''
        将字节转换为 MB GB TB
        :param b: 字节数
        :return: 返回 MB GB TB
        '''
        units = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = 0
        while b >= 1024 and i < len(units) - 1:
            b /= 1024
            i += 1
        return f"{b:.2f} {units[i]}"

    def get_growth_info(self):
        '''
        获取用户当前的签到信息
        :return: 返回一个字典，包含用户当前的签到信息
        '''
        url = "https://drive-m.quark.cn/1/clouddrive/capacity/growth/info"
        querystring = {
            "pr": "ucpro",
            "fr": "android",
            "kps": self.param.get('kps'),
            "sign": self.param.get('sign'),
            "vcode": self.param.get('vcode')
        }
        response = requests.get(url=url, params=querystring).json()
        #print(response)
        if response.get("data"):
            return response["data"]
        else:
            return False

    def get_growth_sign(self):
        '''
        获取用户当前的签到信息
        :return: 返回一个字典，包含用户当前的签到信息
        '''
        url = "https://drive-m.quark.cn/1/clouddrive/capacity/growth/sign"
        querystring = {
            "pr": "ucpro",
            "fr": "android",
            "kps": self.param.get('kps'),
            "sign": self.param.get('sign'),
            "vcode": self.param.get('vcode')
        }
        data = {"sign_cyclic": True}
        response = requests.post(url=url, json=data, params=querystring).json()
        # print(response)
        # 检查响应是否包含期望的数据
        if response.get("data") and "sign_daily_reward" in response["data"]:
            # 返回成功状态和奖励数据
            return True, response["data"]["sign_daily_reward"]
        else:
            # 返回失败状态和错误信息
            error_msg = response.get("message", "未知错误")
            return False, error_msg

    def queryBalance(self):
        '''
        查询抽奖余额
        '''
        url = "https://coral2.quark.cn/currency/v1/queryBalance"
        querystring = {
            "moduleCode": "1f3563d38896438db994f118d4ff53cb",
            "kps": self.param.get('kps'),
        }
        response = requests.get(url=url, params=querystring).json()
        # print(response)
        if response.get("data"):
            return response["data"]["balance"]
        else:
            return response["msg"]

    def do_sign(self):
        '''
        执行签到任务
        :return: 返回一个字符串，包含签到结果
        '''
        log = ""
        # 每日领空间
        growth_info = self.get_growth_info()
        if not growth_info:
            log += "❌❌ 签到异常: 获取成长信息失败\n"
            return log

        log += (
            f" {'88VIP' if growth_info['88VIP'] else '普通用户'} {self.param.get('user')}\n"
            f"💾 网盘总容量：{self.convert_bytes(growth_info['total_capacity'])}，"
            f"签到累计容量：")

        if "sign_reward" in growth_info['cap_composition']:
            log += f"{self.convert_bytes(growth_info['cap_composition']['sign_reward'])}\n"
        else:
            log += "0 MB\n"

        if growth_info["cap_sign"]["sign_daily"]:
            log += (
                f"✅ 签到日志: 今日已签到+{self.convert_bytes(growth_info['cap_sign']['sign_daily_reward'])}，"
                f"连签进度({growth_info['cap_sign']['sign_progress']}/{growth_info['cap_sign']['sign_target']})\n"
            )
        else:
            try:
                sign_success, sign_return = self.get_growth_sign()
                if sign_success:
                    log += (
                        f"✅ 执行签到: 今日签到+{self.convert_bytes(sign_return)}，"
                        f"连签进度({growth_info['cap_sign']['sign_progress'] + 1}/{growth_info['cap_sign']['sign_target']})\n"
                    )
                else:
                    log += f"❌❌ 签到异常: {sign_return}\n"
            except Exception as e:
                log += f"❌❌ 签到异常: {str(e)}\n"

        return log


def extract_params(url):
    '''
    从URL中提取所需的参数
    :param url: 包含参数的URL
    :return: 返回一个字典，包含所需的参数
    '''
    # 提取URL中的查询参数部分（?后面的内容）
    query_start = url.find('?')
    query_string = url[query_start + 1:] if query_start != -1 else ''

    # 解析查询参数
    params = {}
    for param in query_string.split('&'):
        if '=' in param:
            key, value = param.split('=', 1)
            params[key] = value

    # 返回所需的参数
    return {
        'kps': params.get('kps_wg', ''),
        'sign': params.get('sign_wg', ''),
        'vcode': params.get('vcode', '')
    }


def send_email(body, subject="GitHub Action Status - QuarkSignResult"):
    '''
    发送邮件
    :param body: 邮件内容
    :return: None
    '''
    try:
        # 从环境变量获取邮件配置
        smtp_server = os.environ.get('SMTP_SERVER', "smtp.qq.com")
        smtp_port = int(os.environ.get('SMTP_PORT', 465))
        email_username = os.environ.get('EMAIL_USERNAME')
        email_password = os.environ.get('EMAIL_PASSWORD')
        email_receiver = os.environ.get('EMAIL_RECEIVER')

        # 验证必要的邮件配置
        if not all([smtp_server, smtp_port, email_username, email_password, email_receiver]):
            print("❌ 邮件配置不完整，跳过发送")
            return False

        # 严格按照RFC标准设置发件人
        sender_name = "QuarkSignBot"
        sender_address = email_username
        # 格式化发件人地址
        formatted_sender = email.utils.formataddr((sender_name, sender_address))

        # 创建邮件内容
        message = MIMEText(body, 'plain')
        message['From'] = formatted_sender
        message['To'] = Header(email_receiver)
        message['Subject'] = Header(subject, 'utf-8')
        # print(message)

        # 创建更稳定的SMTP连接
        print(f"🔄 正在连接SMTP服务器: {smtp_server}:{smtp_port}")
        server = smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=30)
        server.set_debuglevel(1)  # 启用调试输出
        
        # 发送EHLO命令
        print("🔄 发送EHLO握手...")
        server.ehlo()
        
        # 登录并发送邮件
        print(f"🔐 登录邮箱账号: {email_username}")
        server.login(email_username, email_password)
        print(f"✉️ 发送邮件到: {email_receiver}")
        server.sendmail(sender_address, [email_receiver], message.as_string())

        # 正确关闭连接
        print("🔄 关闭SMTP连接...")
        try:
            server.quit()
        except Exception as quit_error:
            print(f"⚠️ 关闭连接时出错: {str(quit_error)}")
        
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
        print(f"❌❌ 邮件发送失败: {str(e)}")
        return False

def main():
    '''
    主函数
    :return: 返回一个字符串，包含签到结果
    '''
    msg = ""
    global cookie_quark
    cookie_quark = get_env()

    print("✅ 检测到共", len(cookie_quark), "个夸克账号\n")

    i = 0
    while i < len(cookie_quark):
        # 获取user_data参数
        user_data = {}  # 用户信息
        for a in cookie_quark[i].replace(" ", "").split(';'):
            if not a == '':
                user_data.update({a[0:a.index('=')]: a[a.index('=') + 1:]})
        
        # 从url参数中提取额外信息
        if 'url' in user_data:
            url_params = extract_params(user_data['url'])
            user_data.update(url_params)
        # print(user_data)
        
        # 开始任务
        log = f"🙍🏻‍♂️ 第{i + 1}个账号"
        msg += log
        # 登录
        log = Quark(user_data).do_sign()
        msg += log + "\n"
        i += 1

        # # 查询余额
        # log = Quark(user_data).queryBalance()
        # print(log)
        # i += 1
    
    print("----------夸克网盘签到完毕----------")
    # print(msg)

    # 获取自定义主题（如有）
    email_subject = os.environ.get('EMAIL_SUBJECT', "GitHub Action 完成通知 - 夸克签到结果")
    
    # 发送邮件
    if os.environ.get('ENABLE_EMAIL', 'true').lower() == 'true':
        send_email(msg, email_subject)
    else:
        print("❌ 邮件发送已禁用")

    return msg[:-1]

# 测试邮件发送
def test_email():
    msg = "✅ 测试邮件内容\n" \
        "✅ 签到日志: 今日已签到+40.00 MB，连签进度(2/7)\n" \
        "✅ 这是夸克签到脚本的测试邮件"
    
    # 使用环境变量配置
    os.environ['SMTP_SERVER'] = "smtp.qq.com"
    os.environ['SMTP_PORT'] = "465"
    os.environ['EMAIL_USERNAME'] = "mountyas793@foxmail.com"  # 替换为您的QQ邮箱
    os.environ['EMAIL_PASSWORD'] = "fzuensaacenpcabe"  # 替换为QQ邮箱授权码
    os.environ['EMAIL_RECEIVER'] = "wangyang@cndachang.cn"  # 替换为接收邮箱
    
    send_email(msg, "夸克签到测试邮件")

if __name__ == "__main__":
    print("----------夸克网盘开始签到----------")
    # test_email()
    result = main()
    # 如果邮件发送失败，输出结果到控制台
    if not os.environ.get('ENABLE_EMAIL', 'true').lower() == 'true':
        print("\n签到结果:\n" + result)
    print("----------程序执行完毕----------")
