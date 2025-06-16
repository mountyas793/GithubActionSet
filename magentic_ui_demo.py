# -*- coding: utf-8 -*-
# @Project: gihub_action_sanyaosa
# @File: magentic_ui_demo.py
# @Author: 卯三
# @Date: 2025/06/06 09:17
# @Desc: ...

import json


def main(arg1: str) -> str:
	data = json.loads(arg1)
	technical_summary = data
	['technical_summary']
	recent_data = data['recent_data']
	report = data['report']
	return {
		"technical_summary": json.dumps(technical_summary, ensure_ascii=False, indent=2),
		"recent_data": json.dumps(recent_data, ensure_ascii=False, indent=2)
	}


def main():
    pass

if __name__ == '__main__':
    main()