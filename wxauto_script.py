# -*- coding: utf-8 -*-
# @Project: gihub_action_sanyaosa
# @File: wxauto.py
# @Author: 卯三
# @Date: 2025/06/03 17:27
# @Desc: 微信自动化脚本

import time
from wxauto import WeChat

def wx_auto_send():
    # 初始化微信
    wx = WeChat()
    # 定义监听列表
    listen_list = [
    '哈哈哈'
    ]
    # 添加监听对象
    for i in listen_list:
        wx.AddListenChat(who=i, savepic=False)  # savepic 保存图片，默认为False

    # 持续监听消息，并且收到消息后回复“收到”
    wait = 1  # 设置1秒查看一次是否有新消息
    while True:
        # 获取消息
        msgs = wx.GetListenMessage()
        for chat in msgs:
            who = chat.who              # 获取聊天窗口名（人或群名）
            one_msgs = msgs.get(chat)   # 获取消息内容
            # 回复收到
            for msg in one_msgs:
                msgtype = msg.type       # 获取消息类型
                print(f'【{who}】：{msgtype}')
                content = msg.content    # 获取消息内容，字符串类型的消息内容
                print(f'【{who}】：{content}')
            # ===================================================
            # 处理消息逻辑（如果有）
            # 
            # 处理消息内容的逻辑每个人都不同，按自己想法写就好了，这里不写了
            # 
            # ===================================================
                if msgtype == 'friend':
                    chat.SendMsg('收到')  # 回复收到
                elif msgtype == 'self' and content == '你是谁？':
                    wait = 3  # 重置等待时间
                    chat.SendMsg('我是你 爹 ')  # 回复收到
                    # 中断
                    break
                elif msgtype =='self' and content == '你会做什么？':
                    wait = 3  # 重置等待时间
                    chat.SendMsg('挑灵、撒纸、垫棺材')  # 回复收到
                    # 中断
                    break
        time.sleep(wait)


def main():
    wx_auto_send()  # 调用wx_auto_send()函数


if __name__ == '__main__':
    main()