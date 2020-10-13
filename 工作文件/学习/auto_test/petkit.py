#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import unittest,os,sys,time
import redis
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
sys.path.append(os.path.dirname(__file__))


def sms_login(driver):
    #点击手机验证码登录
    login_header_mobile = driver.find_element_by_class_name('saas-common-login-detail-inactive')
    print(login_header_mobile)
    login_header_mobile.click()
    time.sleep(10)

    #输入手机号
    mobile_input = driver.find_element_by_id('mat-input-0')
    mobile_input.send_keys('15618655559')
    #点击输入验证码
    generate_code = driver.find_element_by_class_name('saas-common-login-detail__mobile-code')
    generate_code.click()

    #获取redius拿缓存
    r = redis.Redis(host='sandbox.food.petkit.cn',password='Petkit123', port=6379, db=0)
    all_code = r.keys('code:storePrograme:15618655559:*')
    print(all_code[0].decode())
    str_code = all_code[0].decode()
    print("短信的验证码是"+str_code[-4:])
    code = str_code[-4:]
    valication = driver.find_element_by_id('mat-input-1')
    valication.send_keys(code)
    time.sleep(20)

    #点击确认按钮
    mobile_login_btn = driver.find_element_by_class_name('saas-common-login-detail__button')
    mobile_login_btn.click()
    #开始计时
    login_before_time = time.time()

    # #等待直到出现我知道了
    # try:
    #     element = WebDriverWait(driver,100).until(
    #         EC.presence_of_element_located((By.XPATH, '//div[@class="ant-modal"]'))
    #     )
    # finally:
    #     driver.quit()

    #点击我知道了
    login_after_time = time.time()
    # print('登录用了'+login_after_time-login_before_time+'秒')

    btn_know = driver.find_element_by_class_name('ant-btn ng-star-inserted ant-btn-primary')
    btn_know.click()

def qrcode_login(driver):
    #10秒扫码
    time.sleep(10)
    login_before_time = time.time()
    try:
        btn_know = WebDriverWait(driver, 600).until(
            EC.presence_of_element_located((By.XPATH,"//*[@href='#/workspace/booking/calendar']"))
        )
        print(btn_know)
    finally:
        driver.quit()


    # # 点击我知道了
    # login_after_time = time.time()
    # print('登录用了' + login_after_time - login_before_time + '秒')
    #
    # btn_know.click()

def load_driver():
    driver_path = os.getcwd() + '/driver/mac/chromedriver'
    driver = webdriver.Chrome(executable_path = driver_path)
    return driver

def open_url(driver,url):
    driver.get(url)

def run(driver):
    #qrcode_login(driver)
    sms_login(driver)


if __name__ =="__main__":
    #1.加载驱动
    driver = load_driver()

    #2.打开URL
    url = 'https://sandbox-chain.petkit.cn/'
    open_url(driver,url)

    #3.查看文件源码
    #print(driver.page_source)

    #4.run
    run(driver)
    #4.关闭浏览器
    # driver.close()

