import requests
import time
import pandas as pd
import json

domain = 'https://www.lazada.co.id'
def inisialisasi(search_item):    
    data_splits = search_item.split(' ')
    keyword = '%20'.join(data_splits)
    # print(keyword)    
    url = f'https://www.lazada.co.id/catalog/?ajax=true&page=1&q={keyword}'    

    headers = {
        'User-Agent' : 'Mozilla/5.0 (Linux; Android 13; SM-S901U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
        'Cache-Control' : 'no-cache'
    }
    response = requests.session()
    data = response.get(url=url, headers=headers).text    
    conv_data = json.loads(data)
    response.cookies.clear()
    # response.close()

    total = int(conv_data['mainInfo']['totalResults'])
    items_page = int(conv_data['mainInfo']['pageSize'])

    total_page = int(total/ items_page)
    print(items_page)
    print(f'ada {total} jumlah barang ditemukan, total {total_page} halaman bisa ditampilkan')
    return {
        'keyword' : keyword,
        'data' : conv_data
    }

def saved_data(products, nama_file):
    data = pd.DataFrame(products)    
    data.to_excel(f'{nama_file}.xlsx', index=None)
    print(data)

def callback_page(pages, search):
    url = f'https://www.lazada.co.id/catalog/?ajax=true&page={pages}&q={search}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Cache-Control' : 'no-cache'
    }
    response = requests.session()
    data = response.get(url=url, headers=headers).text    
    conv_data = json.loads(data)
    response.cookies.clear()
    # response.close()
    return conv_data

def product_items(products_lib):
    products = products_lib['mods']['listItems']
    items=[]
    for product in products:
        #nama-produk
        try:
            item =product['name']
        except KeyError:
            item = '-'            

        #harga-before    
        try:
            harga_before = int(product['originalPrice'])
        except KeyError:
            harga_before = '-'        

        #diskon
        try:
            diskon = product['discount'][:-3]
        except KeyError:
            diskon = '-'            
        
        #harga-tertampil
        try:
            harga = product['priceShow'][2:]
            conv_harga = harga.split('.')
            harga = int(''.join(conv_harga))
        except KeyError:
            harga = '-'                                
        
        #sold items
        try:
            terjual = product['itemSoldCntShow'][:-7]
        except KeyError:
            terjual = '-' 

        #rating
        try:
            rating = float(product['ratingScore'])
            rating = round(rating, 1)
        except KeyError:
            rating ='-'

        items.append({
            'nama' : item,
            'harga-before' : harga_before,
            'harga' : harga,
            'diskon' : diskon,
            'terjual' : terjual,
            'rating' : rating
        })
    return items

run = True
while run:
    keyword_search = input('masukkan produk yang dicari: ')
    searching_item = inisialisasi(keyword_search)
    page=int(input('tampilkan berapa halaman?: '))
    x=1
    print('loading...')
    time.sleep(75)
    products = []
    for halaman in range(1,page+1):        
        if halaman == 1:
            loadpage = searching_item['data']            
        else:
            loadpage = callback_page(pages=halaman, search=searching_item['keyword'])            
        items = product_items(loadpage)
        products.extend(items)
        for item in items:    
            print(f'({x}) {item}')
            x= x+1
        time.sleep(75)

    save_confirm = input('simpan data (y/n):')
    while save_confirm != 'y' and save_confirm !='n':
        print('jawab hanya dengan "y" untuk iya atau "n" untuk tidak')
        save_confirm = input('simpan data (y/n):')
    if save_confirm=='y':
        nama_file = input('masukkan nama file: ')
        saved_data(products, nama_file)
        print('finished')
    
    run_again = input('cari produk lagi (y/n): ')
    if run_again =='y':
        run =True
    else:
        run =False

print('closing application...')
time.sleep(2)


#it will be good if using rotation proxy to avoid being banned by system
#and accelling your data scraping
#but honestly, free proxy are bad
# list_proxies= [         
#     '20.44.206.138:80',             #bisa        
#     '36.77.44.233:8080',             #bisa , indonesia
#     '103.168.44.167:9191',              #bisa, indonesia    
# ]
# 
# proxy={
#     'http': list_proxies[2],
#     'https': list_proxies[2]
# }

# keyword = 'gitar%20akustik'
# url = f'https://www.lazada.co.id/catalog/?ajax=true&page=1&q={keyword}'    

# headers = {
#     'User-Agent' : 'Mozilla/5.0 (Linux; Android 13; SM-S901U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
#     # 'Cache-Control' : 'no-cache'
# }
# response = requests.get(url=url, headers=headers, proxies=proxy)
# data = response
# print(data)


