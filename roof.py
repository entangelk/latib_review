from main import get_data

url =[
    'https://latib.co.kr/product/detail.html?product_no=21&cate_no=60&display_group=1'
    ,'https://latib.co.kr/product/detail.html?product_no=88&cate_no=60&display_group=1'
    ,'https://latib.co.kr/product/detail.html?product_no=72&cate_no=60&display_group=1'
    ,'https://latib.co.kr/product/detail.html?product_no=15&cate_no=60&display_group=1'
    ,'https://latib.co.kr/product/detail.html?product_no=13&cate_no=60&display_group=1'
    ,'https://latib.co.kr/product/detail.html?product_no=57&cate_no=60&display_group=1'
    ,'https://latib.co.kr/product/detail.html?product_no=66&cate_no=60&display_group=1'
    ,'https://latib.co.kr/product/detail.html?product_no=54&cate_no=60&display_group=1'
    ,'https://latib.co.kr/product/detail.html?product_no=67&cate_no=60&display_group=1'
    ,'https://latib.co.kr/product/detail.html?product_no=47&cate_no=60&display_group=1'
    ,'https://latib.co.kr/product/detail.html?product_no=18&cate_no=60&display_group=1'
    ,'https://latib.co.kr/product/detail.html?product_no=17&cate_no=60&display_group=1'
    ]

for i in url:
    get_data(i)