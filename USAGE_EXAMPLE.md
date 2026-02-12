# 使用示例

## 安装依赖

```bash
pip install -r requirements.txt
```

## 基本使用

### 1. 使用默认配置

```bash
python main.py
```

### 2. 使用自定义 URL

```bash
python main.py "https://www.cmbchina.com/cfweb/personal/proddetail?productCode=XXXX"
```

## 代码示例

### 示例 1: 基本使用

```python
from scraper import CMBNetValueScraper

# 创建爬虫实例（无头模式）
with CMBNetValueScraper(headless=True) as scraper:
    filepath = scraper.scrape()
    print(f"数据已保存到: {filepath}")
```

### 示例 2: 自定义 URL

```python
from scraper import CMBNetValueScraper

url = "https://www.cmbchina.com/cfweb/personal/proddetail?productCode=123456"

with CMBNetValueScraper(headless=True) as scraper:
    filepath = scraper.scrape(url=url)
    print(f"数据已保存到: {filepath}")
```

### 示例 3: 调试模式（显示浏览器窗口）

```python
from scraper import CMBNetValueScraper

# 设置为非无头模式，可以看到浏览器操作过程
with CMBNetValueScraper(headless=False) as scraper:
    filepath = scraper.scrape()
    print(f"数据已保存到: {filepath}")
```

### 示例 4: 自定义配置

```python
from scraper import CMBNetValueScraper
from config import Config

# 修改配置
Config.HEADLESS = False
Config.PAGE_LOAD_TIMEOUT = 60
Config.MAX_SCROLL_TIMES = 20

with CMBNetValueScraper(headless=Config.HEADLESS) as scraper:
    filepath = scraper.scrape()
    print(f"数据已保存到: {filepath}")
```

### 示例 5: 处理爬取的数据

```python
from scraper import CMBNetValueScraper
import pandas as pd

with CMBNetValueScraper(headless=True) as scraper:
    filepath = scraper.scrape()

    if filepath:
        # 使用 pandas 读取 CSV 文件
        df = pd.read_csv(filepath, encoding='utf-8-sig')

        # 显示前几行数据
        print("数据预览:")
        print(df.head())

        # 显示数据统计信息
        print(f"\n总行数: {len(df)}")
        print(f"总列数: {len(df.columns)}")
        print(f"列名: {list(df.columns)}")
```

### 示例 6: 带错误处理的完整示例

```python
import sys
from scraper import CMBNetValueScraper
from utils.logger import setup_logger

logger = setup_logger()

def scrape_cmb_data(url=None):
    """
    爬取招商银行产品净值数据

    Args:
        url: 目标URL，如果为None则使用配置中的默认URL

    Returns:
        bool: 爬取是否成功
    """
    try:
        logger.info("开始爬取...")

        with CMBNetValueScraper(headless=True) as scraper:
            filepath = scraper.scrape(url=url)

            if filepath:
                logger.info(f"爬取成功! 文件保存到: {filepath}")
                logger.info(f"数据行数: {len(scraper.data)}")
                return True
            else:
                logger.error("爬取失败: 未获取到数据")
                return False

    except KeyboardInterrupt:
        logger.warning("用户中断程序")
        return False
    except Exception as e:
        logger.error(f"爬取过程出错: {str(e)}", exc_info=True)
        return False

if __name__ == "__main__":
    # 使用自定义URL
    url = "https://www.cmbchina.com/cfweb/personal/proddetail"

    success = scrape_cmb_data(url)
    sys.exit(0 if success else 1)
```

## 输出文件格式

CSV 文件示例:

| 日期 | 净值 | 累计净值 | 日增长率 |
|------|------|----------|----------|
| 2026-02-12 | 1.2345 | 1.5678 | 0.12% |
| 2026-02-11 | 1.2330 | 1.5663 | 0.08% |
| ... | ... | ... | ... |

## 常见使用场景

### 场景 1: 定时任务爬取

创建一个定时任务脚本 `scheduled_scraper.py`:

```python
import schedule
import time
from scraper import CMBNetValueScraper

def job():
    """定时执行的任务"""
    with CMBNetValueScraper(headless=True) as scraper:
        scraper.scrape()

# 每天早上8点执行
schedule.every().day.at("08:00").do(job)

print("定时任务已启动...")
while True:
    schedule.run_pending()
    time.sleep(60)
```

### 场景 2: 爬取多个产品

```python
from scraper import CMBNetValueScraper

# 产品代码列表
product_codes = ["001", "002", "003"]

for code in product_codes:
    url = f"https://www.cmbchina.com/cfweb/personal/proddetail?productCode={code}"

    with CMBNetValueScraper(headless=True) as scraper:
        filepath = scraper.scrape(url=url)
        print(f"产品 {code}: {filepath}")
```

### 场景 3: 数据分析和可视化

```python
import pandas as pd
import matplotlib.pyplot as plt

# 读取爬取的数据
df = pd.read_csv('output/cmb_product_netvalue_20260212_080000.csv', encoding='utf-8-sig')

# 转换日期列
df['日期'] = pd.to_datetime(df['日期'])

# 绘制净值走势图
plt.figure(figsize=(12, 6))
plt.plot(df['日期'], df['净值'], marker='o')
plt.title('产品净值走势')
plt.xlabel('日期')
plt.ylabel('净值')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.savefig('output/net_value_trend.png')
plt.show()
```

## 故障排查

### 问题 1: 找不到表格元素

**解决方案:**
1. 检查 URL 是否正确
2. 设置 `HEADLESS = False` 查看浏览器操作
3. 增加超时时间配置
4. 查看日志文件获取详细错误信息

### 问题 2: 数据不完整

**解决方案:**
```python
# 在 config.py 中调整以下配置
Config.MAX_SCROLL_TIMES = 20  # 增加滚动次数
Config.SCROLL_DELAY = 3       # 增加滚动延迟
```

### 问题 3: 浏览器驱动问题

**解决方案:**
程序已使用 `webdriver-manager` 自动管理 ChromeDriver，通常不会出现问题。如果仍有问题：

```bash
# 手动安装 ChromeDriver
# 访问 https://chromedriver.chromium.org/downloads
# 下载与 Chrome 版本匹配的 ChromeDriver
# 将其放到 PATH 中
```

### 问题 4: 网络连接问题

**解决方案:**
1. 检查网络连接
2. 确认能够访问目标网站
3. 如果使用代理，需要在代码中配置代理设置
4. 检查防火墙设置
