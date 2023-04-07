from suds.client import Client

client = Client('http://localhost:8000/?wsdl')


# Добавление нового продукта
response = client.service.add_product(7, 'Product ', 100)
print(response)

# Обновление продукта
response = client.service.update_product(7, 'Product  (updated)', 200)
print(response)

# Получение всех продуктов
response = client.service.get_all_products()
print("\nСписок всех продуктов:")
for product in response.Product:
    print(f'{product.id} - {product.name} - {product.price}')

# Удаление продукта
response = client.service.delete_product(1)
print(response)

# Documentation
for i in client.sd:
    wsdl = str(i.wsdl)

with open('wsdl_otput.txt', 'w') as file:
    file.write(wsdl)






