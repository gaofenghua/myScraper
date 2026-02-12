"""
配置文件 - 招商银行产品净值爬虫
"""

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Config:
    """配置类"""

    # 目标URL - 招商银行产品净值页面
    # 注意：此URL需要根据实际情况进行调整
    TARGET_URL = "https://www.cmbchina.com/cfweb/personal/proddetail"

    # 输出目录
    OUTPUT_DIR = os.path.join(BASE_DIR, "output")

    # CSV文件名格式
    CSV_FILENAME_FORMAT = "cmb_product_netvalue_{timestamp}.csv"

    # 浏览器配置
    HEADLESS = True
    WINDOW_SIZE = "1920,1080"
    PAGE_LOAD_TIMEOUT = 30
    ELEMENT_WAIT_TIMEOUT = 20

    # 数据提取配置
    TABLE_SELECTOR = "table"  # 表格选择器
    ROW_SELECTOR = "tr"       # 行选择器
    CELL_SELECTOR = "td, th"  # 单元格选择器

    # 分页配置
    MAX_SCROLL_TIMES = 10
    SCROLL_DELAY = 2

    # CSV导出配置
    CSV_ENCODING = "utf-8-sig"  # 使用BOM确保Excel正确显示中文
