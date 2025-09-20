#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Adapter 标准参数到目标接口参数风格一致性测试
- 遍历所有已注册接口，基于接口示例参数(example_params)先收敛为 StandardParams
- 通过 adapt_params_for_interface(标准参数) 转换为目标接口参数
- 断言：转换后的参数风格（symbol/date/time 等）与 example 保持一致；输出参数键集合不超出接口定义的 required+optional
"""
import re
import unittest
from typing import Dict, Any
import sys
import os

# 确保导入当前项目的 core 包，避免与同级其他项目冲突
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入项目内模块
from core.data.interfaces.base import APIProviderManager
from core.data.interfaces.akshare import akshare_provider
from core.data.extractor.adapter import (
    adapt_params_for_interface,
    AkshareStockParamAdapter,
    StockSymbol,
    StandardParams,
    to_standard_params,
)


class TestAdapterCoversAllInterfaces(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 注册 provider
        cls.manager = APIProviderManager()
        cls.manager.register_provider(akshare_provider)
        # 适配器实例（用于调用内部检测工具方法）
        cls.adapter = AkshareStockParamAdapter()
        # 收集全部接口
        cls.interfaces = []
        for provider in cls.manager._providers.values():
            cls.interfaces.extend(provider.registry._interfaces.values())

    def _accepted_keys(self, metadata) -> set:
        return set((metadata.required_params or []) + (metadata.optional_params or []))

    def _detect_date_style(self, v: Any) -> str:
        if isinstance(v, str) and re.fullmatch(r"\d{8}", v.strip()):
            return "ymd"
        if isinstance(v, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", v.strip()):
            return "y-m-d"
        return "unknown"

    def _detect_time_style(self, v: Any) -> str:
        if isinstance(v, str) and re.fullmatch(r"\d{2}:\d{2}:\d{2}", v.strip()):
            return "h:m:s"
        if isinstance(v, str) and re.fullmatch(r"\d{6}", v.strip()):
            return "hms"
        return "unknown"

    def _style_of_symbol(self, s: str) -> str:
        return self.adapter._detect_symbol_style(s)

    def test_adapter_standard_params_to_example_style_for_all_interfaces(self):
        for meta in self.interfaces:
            with self.subTest(interface=meta.name):
                accepted = self._accepted_keys(meta)
                example = meta.example_params or {}

                # 1) 把示例参数收敛为标准参数（严格格式 + 统一字段）
                std: StandardParams = to_standard_params(example)

                # 2) 通过 adapter 将标准参数转换为目标接口参数
                adapted = adapt_params_for_interface(meta.name, std)

                # 断言：输出键集合不超出 accepted
                self.assertTrue(set(adapted.keys()).issubset(accepted), f"{meta.name}: 存在未被接受的参数键: {set(adapted.keys())-accepted}")

                # 3) symbol 家族：如果接口接受 symbol 且示例可识别风格，则检查风格一致
                target = self.adapter._detect_target_key_style_case(example, accepted)
                if target:
                    target_key, target_style, _case = target
                    example_val = example.get(target_key)
                    if target_style in {"dot", "prefix", "code"} and isinstance(example_val, str):
                        out_val = adapted.get(target_key)
                        if isinstance(out_val, str):
                            out_style = self._style_of_symbol(out_val)
                            self.assertEqual(out_style, target_style, f"{meta.name}: symbol 风格不匹配，应为 {target_style}, 实际 {out_style}")

                # 4) date / trade_date：若存在示例则检查风格一致
                for key_group in [
                    ["date", "trade_date"],
                    ["start_date", "from_date", "begin_date"],
                    ["end_date", "to_date"],
                ]:
                    target_key = next((k for k in key_group if k in accepted and k in example), None)
                    if not target_key:
                        continue
                    sample = example.get(target_key)
                    if not isinstance(sample, str):
                        continue
                    target_style = self._detect_date_style(sample)
                    if target_style == "unknown":
                        continue
                    out_val = adapted.get(target_key)
                    if isinstance(out_val, str):
                        out_style = self._detect_date_style(out_val)
                        self.assertEqual(out_style, target_style, f"{meta.name}: {target_key} 风格不匹配，应为 {target_style}, 实际 {out_style}")

                # 5) time：若存在示例则检查风格一致
                for key_group in [
                    ["start_time"],
                    ["end_time"],
                ]:
                    target_key = next((k for k in key_group if k in accepted and k in example), None)
                    if not target_key:
                        continue
                    sample = example.get(target_key)
                    if not isinstance(sample, str):
                        continue
                    target_style = self._detect_time_style(sample)
                    if target_style == "unknown":
                        continue
                    out_val = adapted.get(target_key)
                    if isinstance(out_val, str):
                        out_style = self._detect_time_style(out_val)
                        self.assertEqual(out_style, target_style, f"{meta.name}: {target_key} 风格不匹配，应为 {target_style}, 实际 {out_style}")


if __name__ == "__main__":
    unittest.main()