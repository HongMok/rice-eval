#!/usr/bin/env python3
"""
从原始 CSV 数据生成统一格式的评估配置 CSV。
表头格式：排序, 一级分类, 二级分类, 评估项目, 操作描述, 所需材料, 适用年龄, 是否必答,
         评分_a_分值, 评分_a_标签, 评分_a_说明, 评分_b_分值, 评分_b_标签, 评分_b_说明, 评分_c_分值, 评分_c_标签, 评分_c_说明
全部 QUOTE_ALL，UTF-8 无 BOM。
"""
import csv
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

UNIFIED_HEADER = [
    '排序', '一级分类', '二级分类', '评估项目', '操作描述', '所需材料', '适用年龄', '是否必答',
    '评分_a_分值', '评分_a_标签', '评分_a_说明',
    '评分_b_分值', '评分_b_标签', '评分_b_说明',
    '评分_c_分值', '评分_c_标签', '评分_c_说明',
]


def write_csv(filename, rows):
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(UNIFIED_HEADER)
        writer.writerows(rows)
    print(f'  写入 {filepath}，共 {len(rows)} 行')


def read_csv(filepath):
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        return list(reader)


def convert_vbmapp():
    """VB-MAPP: 评分说明_1_达标 / 评分说明_0.5_部分达标 / 评分说明_0_未达标"""
    print('处理 VB-MAPP...')
    src = os.path.join(DATA_DIR, 'VB', 'vbmapp-full-milestones.csv')
    rows_in = read_csv(src)
    rows_out = []
    for r in rows_in:
        rows_out.append([
            r['排序'], r['分组'], r['领域'], r['评估项目'], r['操作描述'],
            r['所需材料'], r['适用年龄'], r['是否必答'],
            '1', '达标', r['评分说明_1_达标'],
            '0.5', '部分达标', r['评分说明_0.5_部分达标'],
            '0', '未达标', r['评分说明_0_未达标'],
        ])
    write_csv('vbmapp-config.csv', rows_out)


def convert_pep3():
    """PEP-R: 评分说明_2_通过 / 评分说明_1_萌芽 / 评分说明_0_不通过"""
    print('处理 PEP-R (PEP-3)...')
    src = os.path.join(DATA_DIR, 'PEP-3', 'pep3-full-items.csv')
    rows_in = read_csv(src)
    rows_out = []
    for r in rows_in:
        rows_out.append([
            r['排序'], r['分组'], r['领域'], r['评估项目'], r['操作描述'],
            r['所需材料'], r['适用年龄'], r['是否必答'],
            '2', '通过', r['评分说明_2_通过'],
            '1', '萌芽', r['评分说明_1_萌芽'],
            '0', '不通过', r['评分说明_0_不通过'],
        ])
    write_csv('pep3-config.csv', rows_out)


def convert_cpep():
    """C-PEP: 评分分值_高_标签/说明 / 评分分值_中_标签/说明 / 评分分值_低_标签/说明
    前7领域: 通过=1, 中间反应='', 不通过=0
    情绪与行为: 没有='', 轻度='', 重度=''
    """
    print('处理 C-PEP...')
    src = os.path.join(DATA_DIR, 'PEP-3', 'cpep-full-items.csv')
    rows_in = read_csv(src)
    rows_out = []

    # 根据标签推断分值
    score_map = {
        '通过': '1', '中间反应': '', '不通过': '0',
        '没有': '', '轻度': '', '重度': '',
    }

    for r in rows_in:
        label_a = r['评分分值_高_标签']
        label_b = r['评分分值_中_标签']
        label_c = r['评分分值_低_标签']
        rows_out.append([
            r['排序'], r['分组'], r['领域'], r['评估项目'], r['操作描述'],
            r['所需材料'], r['适用年龄'], r['是否必答'],
            score_map.get(label_a, ''), label_a, r['评分分值_高_说明'],
            score_map.get(label_b, ''), label_b, r['评分分值_中_说明'],
            score_map.get(label_c, ''), label_c, r['评分分值_低_说明'],
        ])
    write_csv('cpep-config.csv', rows_out)


if __name__ == '__main__':
    print('=== 生成统一格式评估配置 CSV ===')
    convert_vbmapp()
    convert_pep3()
    convert_cpep()
    print('=== 完成 ===')
