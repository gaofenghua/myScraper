"""
招商银行产品净值爬虫
使用 Selenium 爬取产品净值页面数据并导出为CSV
"""

import time
import csv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

from config import Config
from utils.logger import setup_logger


class CMBNetValueScraper:
    """招商银行产品净值爬虫类"""

    def __init__(self, headless=True, config=None):
        """
        初始化爬虫

        Args:
            headless: 是否使用无头模式
            config: 配置对象
        """
        self.config = config or Config()
        self.headless = headless
        self.driver = None
        self.logger = setup_logger(log_dir=self.config.OUTPUT_DIR)
        self.data = []

    def setup_driver(self):
        """配置并初始化Chrome WebDriver"""
        try:
            chrome_options = Options()

            if self.headless:
                chrome_options.add_argument('--headless')
                chrome_options.add_argument('--disable-gpu')
                chrome_options.add_argument('--no-sandbox')

            chrome_options.add_argument(f'--window-size={self.config.WINDOW_SIZE}')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

            # 使用webdriver-manager自动管理ChromeDriver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)

            # 设置页面加载超时
            self.driver.set_page_load_timeout(self.config.PAGE_LOAD_TIMEOUT)

            self.logger.info("WebDriver初始化成功")
            return True

        except Exception as e:
            self.logger.error(f"WebDriver初始化失败: {str(e)}")
            return False

    def load_page(self, url=None):
        """
        加载目标页面

        Args:
            url: 目标URL，默认使用配置中的URL
        """
        target_url = url or self.config.TARGET_URL

        try:
            self.logger.info(f"正在加载页面: {target_url}")
            self.driver.get(target_url)

            # 等待页面基本加载完成
            time.sleep(3)

            self.logger.info("页面加载成功")
            return True

        except TimeoutException:
            self.logger.error(f"页面加载超时: {target_url}")
            return False
        except Exception as e:
            self.logger.error(f"页面加载失败: {str(e)}")
            return False

    def wait_for_table(self):
        """等待表格元素加载"""
        try:
            self.logger.info("等待表格元素加载...")

            # 尝试等待表格元素
            wait = WebDriverWait(self.driver, self.config.ELEMENT_WAIT_TIMEOUT)

            # 尝试多种可能的表格定位方式
            table_selectors = [
                (By.CSS_SELECTOR, self.config.TABLE_SELECTOR),
                (By.TAG_NAME, "table"),
                (By.CSS_SELECTOR, ".data-table"),
                (By.CSS_SELECTOR, ".net-value-table"),
                (By.CSS_SELECTOR, "[class*='table']"),
            ]

            for by, selector in table_selectors:
                try:
                    wait.until(EC.presence_of_element_located((by, selector)))
                    self.logger.info(f"找到表格元素: {selector}")
                    return True
                except TimeoutException:
                    continue

            # 如果没有找到标准表格，尝试查找任何包含数据的div结构
            self.logger.warning("未找到标准表格，尝试查找数据容器...")
            return self._check_for_data_container()

        except Exception as e:
            self.logger.error(f"等待表格失败: {str(e)}")
            return False

    def _check_for_data_container(self):
        """检查是否存在数据容器（非标准表格）"""
        try:
            # 尝试查找可能包含数据的元素
            data_selectors = [
                ".data-list",
                ".value-list",
                ".netvalue-list",
                "[class*='list']",
                "[class*='data']",
            ]

            for selector in data_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        self.logger.info(f"找到数据容器: {selector}")
                        return True
                except:
                    continue

            self.logger.warning("未找到明显的数据容器")
            return False

        except Exception as e:
            self.logger.error(f"检查数据容器失败: {str(e)}")
            return False

    def extract_table_data(self):
        """提取表格数据"""
        try:
            self.logger.info("开始提取表格数据...")

            # 尝试从标准表格提取数据
            data = self._extract_from_table()

            if not data:
                # 如果标准表格为空，尝试从列表结构提取
                self.logger.info("尝试从列表结构提取数据...")
                data = self._extract_from_list()

            if data:
                self.data = data
                self.logger.info(f"成功提取 {len(data)} 行数据")
                return True
            else:
                self.logger.warning("未能提取到数据")
                return False

        except Exception as e:
            self.logger.error(f"提取数据失败: {str(e)}")
            return False

    def _extract_from_table(self):
        """从标准表格结构提取数据"""
        try:
            # 查找所有表格
            tables = self.driver.find_elements(By.TAG_NAME, "table")

            if not tables:
                self.logger.warning("未找到任何表格")
                return []

            # 选择最大的表格（通常是主数据表格）
            main_table = max(tables, key=lambda t: len(t.find_elements(By.TAG_NAME, "tr")))
            self.logger.info(f"选择包含 {len(main_table.find_elements(By.TAG_NAME, 'tr'))} 行的表格")

            rows = main_table.find_elements(By.TAG_NAME, "tr")

            if not rows:
                return []

            data = []
            headers = []

            # 提取表头
            try:
                header_row = rows[0]
                header_cells = header_row.find_elements(By.CSS_SELECTOR, self.config.CELL_SELECTOR)
                headers = [cell.text.strip() for cell in header_cells]
                data.append(headers)
                self.logger.info(f"表头: {headers}")
            except Exception as e:
                self.logger.warning(f"提取表头失败: {str(e)}")

            # 提取数据行
            for row in rows[1:]:
                try:
                    cells = row.find_elements(By.CSS_SELECTOR, self.config.CELL_SELECTOR)
                    if cells:
                        row_data = [cell.text.strip() for cell in cells]
                        if any(row_data):  # 确保不是空行
                            data.append(row_data)
                except Exception as e:
                    self.logger.warning(f"提取行数据失败: {str(e)}")
                    continue

            return data

        except Exception as e:
            self.logger.error(f"从表格提取数据失败: {str(e)}")
            return []

    def _extract_from_list(self):
        """从列表结构提取数据"""
        try:
            # 尝试多种列表选择器
            list_selectors = [
                ".data-list .item",
                ".netvalue-list .item",
                ".list-item",
                "[class*='list'] > div",
                "tbody tr",
                ".row",
            ]

            all_data = []

            for selector in list_selectors:
                try:
                    items = self.driver.find_elements(By.CSS_SELECTOR, selector)

                    if len(items) > 1:  # 至少要有几个元素才认为找到了数据
                        self.logger.info(f"从选择器 {selector} 找到 {len(items)} 个数据项")

                        for item in items:
                            text = item.text.strip()
                            if text:
                                all_data.append([text])

                        if all_data:
                            return all_data

                except Exception as e:
                    continue

            return []

        except Exception as e:
            self.logger.error(f"从列表提取数据失败: {str(e)}")
            return []

    def handle_pagination(self):
        """处理分页或无限滚动"""
        try:
            self.logger.info("检查分页...")

            # 尝试滚动页面以加载更多数据
            last_height = self.driver.execute_script("return document.body.scrollHeight")

            for i in range(self.config.MAX_SCROLL_TIMES):
                # 滚动到页面底部
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(self.config.SCROLL_DELAY)

                # 检查页面高度是否变化
                new_height = self.driver.execute_script("return document.body.scrollHeight")

                if new_height == last_height:
                    self.logger.info(f"页面已加载完成，滚动次数: {i + 1}")
                    break

                last_height = new_height
                self.logger.info(f"继续滚动，当前滚动次数: {i + 1}")

            # 检查是否有分页按钮
            self.logger.info("检查分页按钮...")
            self._check_pagination_buttons()

        except Exception as e:
            self.logger.warning(f"处理分页时出错: {str(e)}")

    def _check_pagination_buttons(self):
        """检查并点击分页按钮"""
        try:
            # 常见的分页按钮选择器
            pagination_selectors = [
                "a.next",
                ".next-page",
                "button:contains('下一页')",
                ".pagination .next",
                "[aria-label*='next']",
            ]

            for selector in pagination_selectors:
                try:
                    buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for button in buttons:
                        if button.is_enabled() and button.is_displayed():
                            self.logger.info(f"找到下一页按钮: {selector}")
                            button.click()
                            time.sleep(3)
                            self.handle_pagination()
                            return
                except:
                    continue

        except Exception as e:
            self.logger.warning(f"检查分页按钮失败: {str(e)}")

    def save_to_csv(self, filename=None):
        """
        保存数据到CSV文件

        Args:
            filename: 文件名，如果不指定则使用默认命名

        Returns:
            str: 保存的文件路径，失败返回None
        """
        try:
            if not self.data:
                self.logger.warning("没有数据可保存")
                return None

            # 确保输出目录存在
            import os
            os.makedirs(self.config.OUTPUT_DIR, exist_ok=True)

            # 生成文件名
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = self.config.CSV_FILENAME_FORMAT.format(timestamp=timestamp)

            filepath = os.path.join(self.config.OUTPUT_DIR, filename)

            # 写入CSV文件
            with open(filepath, 'w', newline='', encoding=self.config.CSV_ENCODING) as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(self.data)

            self.logger.info(f"数据已保存到: {filepath}")
            return filepath

        except Exception as e:
            self.logger.error(f"保存CSV文件失败: {str(e)}")
            return None

    def scrape(self, url=None):
        """
        执行完整的爬取流程

        Args:
            url: 目标URL

        Returns:
            str: 保存的文件路径，失败返回None
        """
        try:
            # 初始化WebDriver
            if not self.setup_driver():
                return None

            # 加载页面
            if not self.load_page(url):
                return None

            # 等待表格加载
            if not self.wait_for_table():
                self.logger.warning("表格未加载，尝试继续...")

            # 处理分页
            self.handle_pagination()

            # 提取数据
            if not self.extract_table_data():
                return None

            # 保存到CSV
            filepath = self.save_to_csv()
            return filepath

        except Exception as e:
            self.logger.error(f"爬取过程出错: {str(e)}")
            return None

    def close(self):
        """关闭浏览器"""
        if self.driver:
            self.driver.quit()
            self.logger.info("浏览器已关闭")

    def __enter__(self):
        """支持with语句"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """支持with语句"""
        self.close()
