from si_to_int import convert_si_to_number
import os
def get_shares(dict):
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    login = 'https://app.buzzsumo.com/login?from_page=homepage'
    link = 'https://app.buzzsumo.com/research/content'
    prefix = 'https://app.buzzsumo.com/research/content?logged_in=1&num_days=365&result_type=total&general_article&infographic&video&how_to_article&what_post&why_post&list&tab=0&page=1&q='
    #Catch any errors when paging through the browser
    payload = {}
    payload['shares']=[]
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("window-size=1024x768")
        options.add_argument('headless')
        driver = webdriver.Chrome(options = options)
        driver.get(login)
        loginfield = driver.find_element_by_xpath("//*[@id=\"login-bg\"]/body/div[1]/div[1]/div/form/input[1]")
        passfield = driver.find_element_by_xpath("//*[@id=\"login-bg\"]/body/div[1]/div[1]/div/form/input[3]")
        loginfield.send_keys(os.environ.get('buzz_user'))
        passfield.send_keys(os.environ.get('buzz_pass'))
        passfield.send_keys(Keys.ENTER)
        '''Below are comments parts becuase we are updating FB and RD from Django server before they are visible to user on google sheet'''
        for url in dict['urls']:
            driver.get(prefix + url)
            driver.implicitly_wait(4)
            #fb = driver.find_element_by_xpath("//*[@id=\"content-table\"]/tbody/tr[1]/td[3]/div/span").text
            tw = driver.find_element_by_xpath("//*[@id=\"content-table\"]/tbody/tr[1]/td[4]/div/span").text
            #rd = driver.find_element_by_xpath("//*[@id=\"content-table\"]/tbody/tr[1]/td[6]/div/span").text
            #s = [fb,tw,rd]
            s = convert_si_to_number(tw)
            s = "{:,}".format(s) 
            payload['shares'].append(s)
    except Exception as e:
        print("Something went wrong with Chrome and or Selenium.\nI'm going to give you the sentinel value.\nSee Exception:\n%s" %e)
        #payload['shares'].append(['<<IIPgetsSocial>>', '<<IIPgetsSocial>>', '<<IIPgetsSocial>>'])
        payload['shares'].append('<<IIPgetsSocial>>')
    finally:
        driver.quit()
        return payload
