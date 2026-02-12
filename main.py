"""
招商银行产品净值爬虫 - 主程序入口
"""

import sys
import os
from scraper import CMBNetValueScraper
from config import Config
from utils.logger import setup_logger


def main():
    """主函数"""
    # 设置日志
    logger = setup_logger()
    logger.info("=" * 60)
    logger.info("招商银行产品净值爬虫启动")
    logger.info("=" * 60)

    # 检查命令行参数
    url = None
    if len(sys.argv) > 1:
        url = sys.argv[1]
        logger.info(f"使用自定义URL: {url}")

    # 执行爬取
    try:
        with CMBNetValueScraper(headless=Config.HEADLESS) as scraper:
            filepath = scraper.scrape(url=url)

            if filepath:
                logger.info("=" * 60)
                logger.info("爬取成功!")
                logger.info(f"数据文件: {filepath}")
                logger.info(f"数据行数: {len(scraper.data)}")
                logger.info("=" * 60)
                return 0
            else:
                logger.error("=" * 60)
                logger.error("爬取失败: 未能获取数据")
                logger.error("=" * 60)
                return 1

    except KeyboardInterrupt:
        logger.warning("用户中断程序")
        return 1
    except Exception as e:
        logger.error(f"程序异常: {str(e)}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
