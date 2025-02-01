def get_data (url):
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from pymongo import MongoClient
    from datetime import datetime
    import re
    import time

    # MongoDB 연결
    client = MongoClient('mongodb://localhost:27017/')
    db = client['latib_db']

    # 웹드라이버 설정
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)

    # URL 설정 및 페이지 로딩
    # url = "https://latib.co.kr/product/list.html?cate_no=60"
    driver.get(url)

    # 상품 기본 정보 먼저 가져오기
    product_name = driver.find_element(By.CSS_SELECTOR, "#prdDetailPage > div > div.detailArea > div.infoArea > div > div > div > div.infoArea__inner.infoArea__inner--top > h2.prd__name").text
    price_raw = driver.find_element(By.CSS_SELECTOR, "#prdDetailPage > div > div.detailArea > div.infoArea > div > div > div > div.infoArea__inner.infoArea__inner--top > div.xans-element-.xans-product.xans-product-detaildesign.price > table > tbody > tr.product_price_css.xans-record-").text
    price = int(re.sub(r'[^0-9]', '', price_raw))
    try:
        review_button = driver.find_element(By.CSS_SELECTOR, "#prdDetail > ul > li:nth-child(2) > a")
        review_button.click()    
    except:
        action = webdriver.ActionChains(driver)
        action.move_by_offset(200, 200).click().perform()
        action.reset_actions()
        time.sleep(2)
        review_button = driver.find_element(By.CSS_SELECTOR, "#prdDetail > ul > li:nth-child(2) > a")
        review_button.click()

    time.sleep(2)
    # sort_button = driver.find_element(By.CSS_SELECTOR, "#content > div > div > div.filter_sort_basic.menu > ul > li.filter_sort_basic__sort > ul > li:nth-child(2)")
    # sort_button.click()

    # time.sleep(2)        
    # 현재 페이지의 리뷰들 수집 및 저장

    iframe = driver.find_element(By.ID, "crema-product-reviews-2")
    driver.switch_to.frame(iframe)
    time.sleep(1)

    test_time = 2

    while True:
    # for i in range(test_time):
        review_elements = driver.find_elements(By.CSS_SELECTOR, "#content > div > div > div.widget_reviews__body.products_reviews_list__body > div > ul > li")
        
        for review in review_elements:
            try:
                content = review.find_element(By.CSS_SELECTOR, "div.review_list_v2__review_lcontent > div > div.review_list_v2__content_section > div").text
            except:
                content = ''
            
            try:
                option = review.find_element(By.CSS_SELECTOR, "div.review_list_v2__review_rcontent > div.review_list_v2__options_section > div > div > span.review_options_v2__value").text
            except:
                option = ''
            try:
                date = review.find_element(By.CSS_SELECTOR, "div.review_list_v2__review_lcontent > div > div.review_list_v2__score_section > div.review_list_v2__edit_container").text
            except:
                date = ''
            
            score_mapping = {
            '아주 좋아요': 5,
            '맘에 들어요': 4,
            '보통이에요': 3,
            '그냥 그래요': 2,
            '별로예요': 1
        }
            try:
                rating_text = review.find_element(By.CSS_SELECTOR, "div.review_list_v2__review_lcontent > div > div.review_list_v2__score_section > div.review_list_v2__score_container > div.review_list_v2__score_text").text
                rating = score_mapping[rating_text]

            except:
                rating = ''

            # MongoDB에 바로 저장
            review_data = {
                'product_name': product_name,
                'product_price': price,
                'content': content,
                'option': option,
                'date': date,
                'rating': rating
            }
            
            db.reviews.insert_one(review_data)

        
        # 다음 페이지 버튼 찾기
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, "div > div > div.products_reviews__footer > div > div > a.pagination__button.pagination__button--next")
            next_button.click()
            time.sleep(1)
        except:
            action = webdriver.ActionChains(driver)
            action.move_by_offset(200, 200).click().perform()
            action.reset_actions()
            time.sleep(2)
            try:
                next_button = driver.find_element(By.CSS_SELECTOR, "div > div > div.products_reviews__footer > div > div > a.pagination__button.pagination__button--next")
                next_button.click()
            except:
                break  # 다음 페이지가 없으면 종료
            




    # 브라우저 종료
    driver.quit()