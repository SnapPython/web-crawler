import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AsosScraper:
    def __init__(self):
        # 设置Chrome选项
        self.chrome_options = Options()
        #self.chrome_options.add_argument("--headless")  # 无头模式，不显示浏览器窗口
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
        # 初始化WebDriver（使用Selenium 4内置的ChromeDriver管理）
        self.driver = webdriver.Chrome(
            service=Service(),
            options=self.chrome_options
        )
        self.wait = WebDriverWait(self.driver, 10)
        
        # 存储爬取的数据
        self.all_data = []
        
        # ASOS特定商品类别URL
        self.category_url_template = "https://www.asos.com/men/multipacks/cat/?cid=20831&page={}"  
    
    def start_scraping(self, start_page=1, end_page=1):
        try:
            print(f"开始爬取ASOS网站男装多件装商品数据，从第{start_page}页到第{end_page}页...")
            
            # 遍历指定的页面范围
            for page_num in range(start_page, end_page + 1):
                page_url = self.category_url_template.format(page_num)
                try:
                    self.driver.get(page_url)
                    print(f"正在爬取页面 {page_num}: {page_url}")
                    
                    # 等待页面加载完成 - 使用更通用的选择器
                    try:
                        # 尝试多种可能的页面加载指示元素
                        load_indicators = [
                            (By.CSS_SELECTOR, "div.product-grid-container"),
                            (By.CSS_SELECTOR, "div.product-grid"),
                            (By.CSS_SELECTOR, "article.product-tile"),
                            (By.TAG_NAME, "body")
                        ]
                        
                        for by, selector in load_indicators:
                            try:
                                self.wait.until(EC.presence_of_element_located((by, selector)))
                                print(f"页面 {page_num} 加载完成，使用选择器: {selector}")
                                break
                            except:
                                continue
                        
                        # 页面加载后滚动到底部，确保所有商品都加载
                        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(2)
                    except Exception as load_e:
                        print(f"页面 {page_num} 加载超时，继续尝试提取数据: {str(load_e)}")
                    
                    # 提取当前页面的商品数据
                    items_count = self._extract_data_from_page(page_url)
                    print(f"已从页面 {page_num} 提取了 {items_count} 个商品数据")
                    
                except Exception as e:
                    print(f"爬取页面 {page_num} 时出错: {str(e)}")
                    continue
            
            # 保存数据
            self._save_data()
            
        except Exception as e:
            print(f"爬取过程中出错: {str(e)}")
        finally:
            # 关闭浏览器
            self.driver.quit()
            print("爬取完成，浏览器已关闭")
    
    def _extract_data_from_page(self, page_url):
        """从页面提取商品数据的方法，仅在列表页提取商品名称、价格和图片信息"""
        try:
            # 添加更详细的调试信息，打印页面标题和URL
            print(f"当前页面标题: {self.driver.title}")
            print(f"当前页面URL: {self.driver.current_url}")
            
            # 查找商品信息容器
            product_info_containers = []
            try:
                product_info_containers = self.driver.find_elements(By.CSS_SELECTOR, "div.productInfo_rwyH5")
                print(f"找到 {len(product_info_containers)} 个商品信息容器")
            except Exception as e:
                print(f"查找商品信息容器时出错: {str(e)}")
                
            # 查找商品图片容器
            product_image_containers = []
            try:
                product_image_containers = self.driver.find_elements(By.CSS_SELECTOR, "div.productMediaContainer_kmkXR")
                print(f"找到 {len(product_image_containers)} 个商品图片容器")
            except Exception as e:
                print(f"查找商品图片容器时出错: {str(e)}")
            
            # 查找商品链接容器
            product_link_containers = []
            try:
                product_link_containers = self.driver.find_elements(By.CSS_SELECTOR, "a.productLink_KM4PI")
                print(f"找到 {len(product_link_containers)} 个商品链接容器")
            except Exception as e:
                print(f"查找商品链接容器时出错: {str(e)}")
            
            # 确保三种容器数量一致
            min_containers = min(len(product_info_containers), len(product_image_containers), len(product_link_containers))
            print(f"将处理 {min_containers} 个商品")
            
            items_count = 0
            
            # 先处理前5个商品进行测试
            for i in range(min_containers):
                print(f"\n处理第 {i+1} 个商品")
                try:
                    # 首先初始化所有数据变量
                    title = ""
                    price = ""
                    image_url = ""
                    product_link = ""
                    
                    # 从商品链接容器中提取链接
                    try:
                        product_link = product_link_containers[i].get_attribute("href") or ""
                        print(f"提取到商品链接: {product_link}")
                    except Exception as e:
                        print(f"提取商品链接时出错: {str(e)}")
                    
                    # 从商品信息容器中提取标题，尝试多种可能的选择器
                    title_selectors = [
                        "h2.productDescription_sryaw",
                        "h3.productDescription_sryaw",
                        "div.productTitle",
                        "a.product-title",
                        "h2",
                        "h3"
                    ]
                    
                    for selector in title_selectors:
                        try:
                            title_element = product_info_containers[i].find_element(By.CSS_SELECTOR, selector)
                            raw_title = title_element.text.strip() if title_element else ""
                            if raw_title:
                                # 清理标题，只保留第一行作为商品名称
                                title_lines = raw_title.split('\n')
                                title = title_lines[0].strip() if title_lines else ""
                                print(f"使用选择器 {selector} 提取到标题: {title}")
                                break
                        except Exception as e:
                            print(f"使用选择器 {selector} 提取标题时出错: {str(e)}")
                            continue
                    
                    # 如果还是没找到标题，尝试从链接文本中提取
                    if not title and product_link:
                        try:
                            raw_link_text = product_link_containers[i].text.strip()
                            if raw_link_text:
                                # 清理链接文本，只保留第一行作为商品名称
                                link_text_lines = raw_link_text.split('\n')
                                title = link_text_lines[0].strip() if link_text_lines else ""
                                print(f"从链接文本提取到标题: {title}")
                        except Exception as e:
                            print(f"从链接文本提取标题时出错: {str(e)}")
                    
                    # 从商品信息容器中提取价格
                    try:
                        price_element = product_info_containers[i].find_element(By.CSS_SELECTOR, "span.originalPrice_jEWt1 span.price__B9LP")
                        price = price_element.text.strip() if price_element else ""
                        print(f"提取到价格: {price}")
                    except Exception as e:
                        print(f"提取价格时出错: {str(e)}")
                    
                    # 从商品图片容器中提取图片URL
                    try:
                        image_element = product_image_containers[i].find_element(By.CSS_SELECTOR, "div.productHeroContainer_dVvdX img")
                        image_url = image_element.get_attribute("src") or image_element.get_attribute("data-src") or ""
                        if image_url and not image_url.startswith("http"):
                            image_url = "https:" + image_url
                        print(f"提取到图片URL: {image_url}")
                    except Exception as e:
                        print(f"提取图片URL时出错: {str(e)}")
                    
                    # 创建商品数据字典
                    product_data = {
                        "product_name": title,
                        "price": price,
                        "image_url": image_url,
                        "product_link": product_link,
                        "source_page": page_url
                    }
                    
                    # 将数据添加到列表中 - 如果标题为空但其他关键信息存在，也添加
                    if title or price or image_url or product_link:
                        self.all_data.append(product_data)
                        items_count += 1
                        print(f"已提取商品: {title or '无标题产品'}")
                    
                except Exception as e:
                    print(f"提取单个商品数据时出错: {str(e)}")
                    continue
            
            return items_count
            
        except Exception as e:
            print(f"提取页面数据时出错: {str(e)}")
            return 0
    
    def _save_data(self):
        """保存爬取的数据到CSV和JSON文件"""
        if not self.all_data:
            print("没有数据可保存")
            return
        
        try:
            # 创建DataFrame
            df = pd.DataFrame(self.all_data)
            
            # 保存为CSV文件
            csv_file = "asos_multipack_products.csv"
            df.to_csv(csv_file, index=False, encoding="utf-8-sig")
            print(f"数据已保存到 {csv_file}")
            
            # 保存为JSON文件
            json_file = "asos_multipack_products.json"
            df.to_json(json_file, orient="records", force_ascii=False, indent=2)
            print(f"数据已保存到 {json_file}")
            print(f"总共爬取了 {len(self.all_data)} 个商品数据")
            
        except Exception as e:
            print(f"保存数据时出错: {str(e)}")

if __name__ == "__main__":
    # 创建爬虫实例并开始爬取数据
    # 可以通过参数控制爬取的页面范围，默认只爬取第1页进行测试
    scraper = AsosScraper()
    scraper.start_scraping(start_page=1, end_page=1)