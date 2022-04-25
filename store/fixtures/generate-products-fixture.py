import json

f = open('products-database.json')
data = json.load(f)
data_filtered = []


for product in data[0:4000]:
    # Create product dict
    product_dict = {}
    fields = {}
    
    fields['name'] = product['name']
    fields['description'] = product['description']
    fields['brand'] = product['brand']
    fields['price'] = product['price']
    fields['rating'] = product['rating']
    fields['image'] = product['image']
    fields['category'] = product['categories'][0]

    product_dict['model'] = 'store.Item'
    product_dict['pk'] = product['objectID']
    product_dict['fields'] = fields

    data_filtered.append(product_dict)

with open('products_4000.json', 'w') as outfile:
    json.dump(data_filtered, outfile)


    


