from spyne import Application, rpc, ServiceBase, Integer, Unicode, Array, Boolean, ComplexModel
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication


class Product(ComplexModel):
    id = Integer
    name = Unicode
    price = Integer

    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price


# database
products = [
    Product(1, "Худи черного цвета с монограммами adidas Originals", 6090),
    Product(2, "Синяя куртка The North Face", 23725),
    Product(3, "Коричневый спортивный oversized-топ ASOS DESIGN", 3390),
    Product(4, "Черный рюкзак Nike Heritage", 2340),
    Product(5, "Черные туфли на платформе с 3 парами люверсов Dr Martens 1461 Bex", 13590),
    Product(6, "Темно-синие широкие строгие брюки ASOS DESIGN", 2890)
]


class ProductService(ServiceBase):
    # creating
    @rpc(Integer, Unicode, Integer, _returns=Unicode)
    def add_product(ctx, id, name, price):
        if id not in [product.id for product in products]:
            new_product = Product(id, name, price)
            products.append(new_product)
            str = f'Создан новый продукт: \n{new_product.id} - {new_product.name} - {new_product.price}\n'
            return str
        else:
            return "Error! Product with this id already exist!\n"

    # updating
    @rpc(Integer, Unicode, Integer, _returns=Unicode)
    def update_product(ctx, id, name, price):
        for product in products:
            if product.id == id:
                product.name = name
                product.price = price
                str = f'Обновленный продукт: \n{product.id} - {product.name} - {product.price}'
                return str
        return "Error! Product with this id doesnt exist!\n"

    # all products list
    @rpc(_returns=Array(Product))
    def get_all_products(ctx):
        return products

    # deleting
    @rpc(Integer, _returns=Unicode)
    def delete_product(ctx, id):
        for i, product in enumerate(products):
            if product.id == id:
                del products[i]
                str = f'\nУдален продукт: \n{product.id} - {product.name} - {product.price}\n'
                return str
        return "\nError! Product with this id doesnt exist!\n"


application = Application([ProductService], 'http://localhost:8000/',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())

wsgi_application = WsgiApplication(application)

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    server = make_server('localhost', 8000, wsgi_application)
    server.serve_forever()
    print('server is working')
