from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import StaleElementReferenceException
import time

class AirDefense:
    def __init__(self):
        self.web_url = 'https://adr.npa.gov.tw/'
        
        chrome_options = Options()

        # 啟用顯示驅動程序（將瀏覽器視窗顯示在桌面）
        # chrome_options.add_argument("--headless")  # 在後台運行
        # chrome_options.add_argument("--disable-gpu")  # 禁用 GPU 加速

        # 禁用圖像和 CSS
        prefs = {
            "profile.managed_default_content_settings.images": 2, # 2: 禁用圖像
            "profile.managed_default_content_settings.stylesheet": 2 # 2: 禁用 CSS
        }
        chrome_options.add_experimental_option("prefs", prefs)
        # 初始化 WebDriver 並應用選項
        self.driver = webdriver.Chrome(options=chrome_options)

        self.city_urls = {
            'Taipei_1': 'https://www.google.com/maps/d/edit?mid=1ceQ5gitm3HnFVXVwhzroV7uLM_obkDdd&amp;usp=sharing&amp;z=18',
            'Taipei_2': 'https://www.google.com/maps/d/viewer?usp=sharing&z=18&mid=1gi1uuzzCxL8pKev6TXvgJU9KdA2ZLpyJ',
            'Taipei_3': 'https://www.google.com/maps/d/viewer?mid=1bYwHYsY9FAcsWApuXcuAZtbJkzjJ-KLG',
            'New_Taipei': 'https://www.google.com/maps/d/viewer?mid=16mK1e8ahEkNDFDxLTc4HITkffnxYKUUx',
        }
    
    def find_list(self, type, head, element):
        parent_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((type, head))
        )
        child_elements = WebDriverWait(parent_element, 10).until(
            EC.visibility_of_all_elements_located((type, element))
        )

        return child_elements

    def run(self):

        for city, url in self.city_urls.items():
            url = self.city_urls['Taipei_2']
            # print(city,url)
            self.driver.get(url)

            wait = WebDriverWait(self.driver, 10)

            try:
                
                #selection = wait.until(EC.element_to_be_clickable((
                #    By.XPATH, 
                #    '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[1]/div/div[3]/div[2]/div/div'))
                #)
                #self.driver.execute_script("arguments[0].click();", selection)

                # //*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[1]/div/div[3]/div[2]/div/div

                child_elements = self.find_list(By.CSS_SELECTOR, 'div.i4ewOd-pbTTYe-haAclf', 'div.HzV7m-pbTTYe')

                # for child_element in child_elements:
                #     print(child_element.text)
                #     selection = WebDriverWait(child_element, 10).until(
                #         EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.HzV7m-pbTTYe-KoToPc-ornU0b'))
                #     )
                #     self.driver.execute_script("arguments[0].click();", selection)
                for i in range(0, len(child_elements)):
                    
                    driver = child_elements[i]
                    pref_x_path = '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[{}]'.format(i + 1)
                    # print(driver.text)
                    if driver.text.split('\n')[0] == '署屬機關':
                        items = self.find_list(By.XPATH, pref_x_path + '/div/div[3]', './/div[@class="HzV7m-pbTTYe-ibnC6b pbTTYe-ibnC6b-d6wfac"]')
                        for item in items:
                            target = item.find_element(By.XPATH, './/div[@class="suEOdc"]')
                            self.driver.execute_script("arguments[0].click();", target)

                            infos = self.find_list(By.XPATH, '//*[@id="featurecardPanel"]/div/div/div[4]/div[1]', './/div[@class="qqvbed-p83tee"]')
                            for info in infos:
                                title = WebDriverWait(info, 10).until(EC.presence_of_element_located(
                                    (By.XPATH, './/div[@class="qqvbed-p83tee-V1ur5d"]')
                                ))
                                content = WebDriverWait(info, 10).until(EC.presence_of_element_located(
                                    (By.XPATH, './/div[@class="qqvbed-p83tee-lTBxed"]')
                                ))
                                
                                title_text = title.text
                                content_text = content.text
                                print("{}: {}".format(title_text, content_text))
                                # result_dict[title_text] = content_text
                            print("---------------------------------")
                            time.sleep(2)

                    else: # if v selection list is clickable
                        selection_x_path = pref_x_path + '/div/div[3]/div[2]/div/div'
                        selection = self.driver.find_element(By.XPATH, selection_x_path)
                        self.driver.execute_script("arguments[0].click();", selection)

                        #//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]
                        unit = self.find_list(By.XPATH, pref_x_path + '/div/div[3]', './/div[@class="HzV7m-pbTTYe-JNdkSc"]')
                        for j in range(3,3+len(unit)):
                            targets = self.find_list(By.XPATH, pref_x_path + '/div/div[3]/div[{}]/div[2]'.format(j), './/div[@class="suEOdc"]')
                            # print([target.text for target in targets])
                            for target in targets:
                                self.driver.execute_script("arguments[0].click();", target)

                                infos = self.find_list(By.XPATH, '//*[@id="featurecardPanel"]/div/div/div[4]/div[1]', './/div[@class="qqvbed-p83tee"]')
                                for info in infos:
                                    title = WebDriverWait(info, 10).until(EC.presence_of_element_located(
                                        (By.XPATH, './/div[@class="qqvbed-p83tee-V1ur5d"]')
                                    ))
                                    content = WebDriverWait(info, 10).until(EC.presence_of_element_located(
                                        (By.XPATH, './/div[@class="qqvbed-p83tee-lTBxed"]')
                                    ))

                                    title_text = title.text
                                    content_text = content.text
                                    print("{}: {}".format(title_text, content_text))
                                    # result_dict[title_text] = content_text
                                print("---------------------------------")
                                time.sleep(2)

            except Exception as e:
                print("其他錯誤: {}".format(e))
                self.driver.quit()

            break

        time.sleep(1000000)

ad = AirDefense()
ad.run()