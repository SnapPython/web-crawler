# ASOA网站数据爬取工具

这是一个使用Python和Selenium爬取ASOA网站数据的工具。

## 项目介绍

本工具设计用于自动化爬取ASOA网站上的各类数据，并将其保存为CSV和JSON格式的文件，方便后续分析和使用。

## 安装依赖

首先需要安装项目所需的依赖包：

```bash
pip install -r requirements.txt
```

## 使用方法

1. 确保已经安装了Chrome浏览器
2. 运行主爬虫脚本：

```bash
python asoa_scraper.py
```

## 项目结构

- `asoa_scraper.py`：主爬虫程序，包含所有爬取逻辑
- `requirements.txt`：项目依赖列表
- `asoa_data.csv`：爬取的数据保存为CSV格式（运行后生成）
- `asoa_data.json`：爬取的数据保存为JSON格式（运行后生成）

## 配置说明

爬虫程序包含以下可配置项（位于`asoa_scraper.py`文件中）：

1. **Chrome选项**：可以根据需要启用或禁用无头模式
2. **爬取的页面**：可以在`specific_pages`列表中添加或修改要爬取的页面
3. **等待时间**：可以调整`time.sleep()`和`WebDriverWait`的等待时间

## 注意事项

1. 请确保您的爬取行为符合网站的robots.txt规则和相关法律法规
2. 过于频繁的请求可能会导致IP被网站封禁，建议合理设置爬取间隔
3. 本工具默认使用有头模式运行Chrome，可以看到浏览器操作过程
4. 由于网站结构可能会发生变化，可能需要根据实际情况调整爬虫代码中的选择器

## 自定义扩展

如果您需要爬取特定类型的数据，可以修改`_extract_data_from_page`方法中的代码，根据页面的HTML结构使用合适的CSS选择器或XPath来提取数据。

## 故障排除

- 如果遇到ChromeDriver相关的错误，请确保安装了与您的Chrome浏览器版本匹配的ChromeDriver
- 如果网站加载缓慢，可以尝试增加等待时间
- 如果遇到登录限制，可能需要在代码中添加登录逻辑

## 许可证

本项目仅供学习和研究使用。