# -*- coding: utf-8 -*-
# @Project: gihub_action_sanyaosa
# @File: url_parser.py
# @Author: #3sanas
# @Date: 2025/12/15 11:06
# @Desc: 解析夸克网盘分享链接中的参数


def parse_quark_url(url):
    """
    从URL中提取所需的参数
    :param url: 包含参数的URL
    :return: 返回一个字典，包含所需的参数
    """
    # 提取URL中的查询参数部分（?后面的内容）
    query_start = url.find("?")
    query_string = url[query_start + 1 :] if query_start != -1 else ""

    # 解析查询参数
    params = {}
    for param in query_string.split("&"):
        if "=" in param:
            key, value = param.split("=", 1)
            params[key] = value

    # 返回所需的参数
    return {
        "user": params.get("user", ""),
        "kps": params.get("kps_wg", ""),
        "sign": params.get("sign_wg", ""),
        "vcode": params.get("vcode", ""),
    }


if __name__ == "__main__":
    # 尝试导入dotenv库（用于本地调试加载.env文件）
    try:
        import os

        from dotenv import load_dotenv

        # 加载.env文件（如果存在）
        load_dotenv()
        print("✅ 成功加载.env文件")
    except ImportError:
        print("ℹ️  未找到python-dotenv库，跳过.env文件加载")
        print("   安装命令：pip install python-dotenv")
    url = os.environ.get("COOKIE_QUARK")
    print(url)
    params = parse_quark_url(url)
    print(params)
