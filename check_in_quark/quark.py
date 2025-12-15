# -*- coding: utf-8 -*-
# @Project: gihub_action_sanyaosa
# @File: quark.py
# @Author: #3sanas
# @Date: 2025/12/15 10:38
# @Desc: 夸克签到核心逻辑模块

import requests


class Quark:
    """
    Quark类封装了签到、领取签到奖励的方法
    """

    def __init__(self, user_data):
        """
        初始化方法
        :param user_data: 用户信息，用于后续的请求
        """
        self.param = user_data

    def convert_bytes(self, b):
        """
        将字节转换为 MB GB TB
        :param b: 字节数
        :return: 返回格式化后的大小字符串
        """
        units = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = 0
        while b >= 1024 and i < len(units) - 1:
            b /= 1024
            i += 1
        return f"{b:.2f} {units[i]}"

    def get_growth_info(self, headers=None):
        """
        获取用户当前的签到信息
        :return: 返回一个字典，包含用户当前的签到信息，失败返回False
        """
        try:
            url = "https://drive-m.quark.cn/1/clouddrive/capacity/growth/info"
            querystring = {
                "pr": "ucpro",
                "fr": "android",
                "kps": self.param["kps"],
                "sign": self.param.get("sign"),
                "vcode": self.param.get("vcode"),
            }
            response = requests.get(url=url, params=querystring).json()
            if response.get("data"):
                return response["data"]
            else:
                status_code = response.get("status")
                error_msg = response.get("message", "未知错误")
                status_code = response.get("status_code")
                error_msg = response.get("message", "未知错误")
                print(f"获取签到信息失败，状态码: {status_code}，错误信息: {error_msg}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"请求异常: {e}")
            return False

    def get_growth_sign(self):
        """
        执行签到操作
        :return: 返回一个元组，第一个元素是布尔值表示是否成功，第二个元素是奖励数据或错误信息
        """
        try:
            url = "https://drive-m.quark.cn/1/clouddrive/capacity/growth/sign"
            querystring = {
                "pr": "ucpro",
                "fr": "android",
                "kps": self.param.get("kps") or self.param.get("kps_wg"),
                "sign": self.param.get("sign") or self.param.get("sign_wg"),
                "vcode": self.param.get("vcode"),
            }
            data = {"sign_cyclic": True}
            response = requests.post(
                url=url, json=data, params=querystring, proxies={}, timeout=10
            ).json()
            if response.get("data") and "sign_daily_reward" in response["data"]:
                # 返回成功状态和奖励数据
                return True, response["data"]["sign_daily_reward"]
            else:
                # 返回失败状态和错误信息
                error_msg = response.get("message", "未知错误")
                return False, error_msg
        except requests.exceptions.RequestException as e:
            print(f"请求异常: {e}")
            return False, str(e)

    def query_balance(self):
        """
        查询抽奖余额
        :return: 返回余额或错误信息
        """
        try:
            url = "https://coral2.quark.cn/currency/v1/queryBalance"
            querystring = {
                "moduleCode": "1f3563d38896438db994f118d4ff53cb",
                "kps": self.param.get("kps"),
            }
            response = requests.get(
                url=url, params=querystring, proxies={}, timeout=10
            ).json()
            if response.get("data"):
                return response["data"]["balance"]
            else:
                return response.get("msg", "未知错误")
        except requests.exceptions.RequestException as e:
            print(f"请求异常: {e}")
            return str(e)

    def do_sign(self):
        """
        执行签到任务
        :return: 返回一个字符串，包含签到结果
        """
        log = ""
        # 每日领空间
        growth_info = self.get_growth_info()
        if not growth_info:
            log += "❌❌ 签到异常: 获取成长信息失败\n"
            return log

        log += (
            f" {'88VIP' if growth_info['88VIP'] else '普通用户'} {self.param.get('user')}\n"
            f"💾 网盘总容量：{self.convert_bytes(growth_info['total_capacity'])}，"
            f"签到累计容量："
        )

        if "sign_reward" in growth_info["cap_composition"]:
            log += (
                f"{self.convert_bytes(growth_info['cap_composition']['sign_reward'])}\n"
            )
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


if __name__ == "__main__":
    pass
