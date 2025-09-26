import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class AsoaScraper:
    def __init__(self):
        # 设置Chrome选项
        self.chrome_options = Options()
        #self.chrome_options.add_argument("--headless")  # 无头模式，不显示浏览器窗口
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
        # 初始化WebDriver（使用最新版本的webdriver_manager处理Chrome 139版本）
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=self.chrome_options
        )
        self.wait = WebDriverWait(self.driver, 10)
        
        # 存储爬取的数据
        self.all_data = []
        
        # 基础URL（需要根据实际网站调整）
        self.base_url = "https://www.asos.com/"  # 假设的基础URL，实际可能不同
    
    def start_scraping(self):
        try:
            # 访问网站首页
            self.driver.get(self.base_url)
            print(f"已访问网站: {self.base_url}")
            
            # 等待页面加载
            time.sleep(3)
            
            # 这里应该根据网站的具体结构和要爬取的数据类型来实现爬取逻辑
            # 下面是一个通用的示例，需要根据实际网站进行修改
            
            # 1. 获取所有主要导航链接
            # nav_links = self.driver.find_elements(By.CSS_SELECTOR, "nav a")
            
            # 2. 示例：爬取特定页面的数据
            # 这里需要替换为实际要爬取的页面URL
            specific_pages = [
                "https://www.asos.com/men/multipacks/cat/?cid=20831&page=1", 
            ]
            
            for page in specific_pages:
                try:
                    self.driver.get(page)
                    print(f"正在爬取页面: {page}")
                    time.sleep(2)
                    
                    # 根据页面结构提取数据
                    # 这里是通用的示例代码，需要根据实际页面结构修改
                    self._extract_data_from_page(page)
                    
                except Exception as e:
                    print(f"爬取页面 {page} 时出错: {str(e)}")
                    continue
            
            # 3. 处理分页（如果有）
            # self._handle_pagination()
            
            # 4. 保存数据
            self._save_data()
            
        except Exception as e:
            print(f"爬取过程中出错: {str(e)}")
        finally:
            # 关闭浏览器
            self.driver.quit()
            print("爬取完成，浏览器已关闭")
    
    def _extract_data_from_page(self, page_url):
        """从页面提取数据的方法，需要根据实际页面结构进行修改"""
        try:
            # 示例：提取所有文章标题和链接
            # articles = self.driver.find_elements(By.CSS_SELECTOR, "article")
            # for article in articles:
            #     title = article.find_element(By.CSS_SELECTOR, "h2").text
            #     link = article.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            #     self.all_data.append({"title": title, "link": link})
            
            # 这里提供一个更通用的方法，尝试提取页面上的所有文本数据
            page_title = self.driver.title
            page_text = self.driver.find_element(By.TAG_NAME, "body").text[:200]  # 只取前200个字符作为示例
            
            # 添加到数据列表
            self.all_data.append({
                "url": page_url,
                "title": page_title,
                "sample_text": page_text
            })
            
            print(f"已从页面提取数据，当前数据总量: {len(self.all_data)}")
            
        except Exception as e:
            print(f"提取页面数据时出错: {str(e)}")
    
    def _handle_pagination(self):
        """处理分页的方法，如果网站有分页结构"""
        try:
            # 这里是处理分页的示例代码，需要根据实际网站的分页结构进行修改
            # while True:
            #     try:
            #         # 查找下一页按钮并点击
            #         next_button = self.wait.until(EC.element_to_be_clickable(
            #             (By.CSS_SELECTOR, "a.next-page")
            #         ))
            #         next_button.click()
            #         time.sleep(2)
            #         
            #         # 提取当前页面数据
            #         self._extract_data_from_page(self.driver.current_url)
            #         
            #     except:
            #         # 没有下一页或点击失败，退出循环
            #         break
            print("分页处理功能待实现")
            
        except Exception as e:
            print(f"处理分页时出错: {str(e)}")
    
    def _save_data(self):
        """保存爬取的数据到CSV和JSON文件"""
        if not self.all_data:
            print("没有数据可保存")
            return
        
        try:
            # 创建DataFrame
            df = pd.DataFrame(self.all_data)
            
            # 保存为CSV文件
            csv_file = "asoa_data.csv"
            df.to_csv(csv_file, index=False, encoding="utf-8-sig")
            print(f"数据已保存到 {csv_file}")
            
            # 保存为JSON文件
            json_file = "asoa_data.json"
            df.to_json(json_file, orient="records", force_ascii=False, indent=2)
            print(f"数据已保存到 {json_file}")
            
        except Exception as e:
            print(f"保存数据时出错: {str(e)}")

if __name__ == "__main__":
    print("开始爬取asos网站数据...")
    scraper = AsoaScraper()
    scraper.start_scraping()