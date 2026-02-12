# 招商银行产品净值爬虫

使用 Selenium 爬取招商银行产品净值页面的每日净值数据表格，并生成 CSV 文件输出。

## 功能特性

- 使用 Selenium WebDriver 自动化浏览器操作
- 支持动态加载内容的页面
- 自动检测和处理分页/滚动加载
- 导出数据为 CSV 格式（支持中文）
- 支持无头模式运行
- 完善的日志记录功能

## 系统要求

- Python 3.7+
- Chrome/Chromium 浏览器

## 安装

1. 克隆或下载项目代码

2. 安装依赖包：

```bash
pip install -r requirements.txt
```

## 使用方法

### 基本使用

直接运行主程序：

```bash
python main.py
```

程序会使用配置文件中默认的 URL 进行爬取。

### 使用自定义 URL

如果需要爬取其他页面，可以指定 URL：

```bash
python main.py "https://www.cmbchina.com/cfweb/personal/proddetail?xxxx"
```

### 配置选项

编辑 `config.py` 文件可以修改以下配置：

- `TARGET_URL`: 目标页面 URL
- `HEADLESS`: 是否使用无头模式（默认 True）
- `WINDOW_SIZE`: 浏览器窗口大小
- `PAGE_LOAD_TIMEOUT`: 页面加载超时时间（秒）
- `ELEMENT_WAIT_TIMEOUT`: 元素等待超时时间（秒）
- `OUTPUT_DIR`: CSV 文件输出目录
- `MAX_SCROLL_TIMES`: 最大滚动次数
- `SCROLL_DELAY`: 滚动延迟时间（秒）

## 输出

爬取的数据会保存到 `output` 目录下，文件名格式为：

```
cmb_product_netvalue_YYYYMMDD_HHMMSS.csv
```

CSV 文件使用 UTF-8-BOM 编码，可以在 Excel 中直接打开并正确显示中文。

## 项目结构

```
.
├── main.py              # 主程序入口
├── scraper.py           # 爬虫核心逻辑
├── config.py            # 配置文件
├── requirements.txt     # Python 依赖
├── README.md            # 项目说明
├── .gitignore           # Git 忽略规则
├── utils/
│   ├── __init__.py
│   └── logger.py        # 日志工具
└── output/              # 输出目录
    ├── *.csv            # CSV 文件
    └── *.log            # 日志文件
```

## 注意事项

1. **目标 URL 配置**：请根据实际的招商银行产品净值页面 URL 更新 `config.py` 中的 `TARGET_URL`。

2. **反爬措施**：
   - 程序已添加随机 User-Agent
   - 避免频繁请求
   - 如遇到验证码，可能需要手动处理

3. **页面结构变化**：如果网站页面结构发生变化，可能需要调整 `scraper.py` 中的选择器。

4. **网络环境**：确保网络连接正常，能够访问目标网站。

## 常见问题

### 1. 找不到表格元素

如果程序提示"未找到标准表格"，可能需要：

- 检查页面 URL 是否正确
- 查看日志文件了解详细错误
- 调整 `config.py` 中的超时时间
- 检查页面是否需要登录或其他验证

### 2. ChromeDriver 版本不匹配

程序使用 `webdriver-manager` 自动管理 ChromeDriver 版本，通常不会出现此问题。

如果仍有问题，可以手动下载对应版本的 ChromeDriver 并添加到系统 PATH。

### 3. 数据不完整

如果数据不完整，可以尝试：

- 增加 `MAX_SCROLL_TIMES` 配置
- 增加 `SCROLL_DELAY` 配置
- 检查页面是否需要点击"加载更多"按钮

## 开发说明

### 调试模式

设置为非无头模式可以看到浏览器操作过程：

```python
# config.py
HEADLESS = False
```

### 日志

日志文件保存在 `output` 目录，文件名格式：`scraper_YYYYMMDD.log`

### 扩展功能

- 继承 `CMBNetValueScraper` 类可以实现自定义爬虫
- 修改 `extract_table_data()` 方法可以适配不同的数据结构
- 添加数据处理逻辑可以清洗和转换数据

## 许可证

本项目仅供学习研究使用。使用本工具爬取网站数据时，请遵守相关法律法规和网站使用条款。

## 免责声明

本工具仅用于学习研究目的。使用者需自行承担使用本工具的风险和责任，并遵守目标网站的 robots.txt 和服务条款。开发者不对因使用本工具导致的任何问题负责。
