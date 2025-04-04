from .models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity=1):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] += quantity
        else:
            self.cart[product_id] = {
                'id': product.id,
                'name': product.name,
                'price': str(product.price),
                'quantity': quantity,
                'image': product.image.url,
                'slug': product.slug,
            }
        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        self.session['cart'] = {}
        self.session.modified = True

    def save(self):
        self.session.modified = True

    def __iter__(self):
        from .models import Product
        product = Product.objects.get(id=product_id)  # 👈 fetch actual product instance
        item['id'] = product_id
        item['product_obj'] = product  # 👈 this line is key for saving the order!
        item['total'] = float(item['price']) * item['quantity']
        yield item

    def get_total_price(self):
        return sum(float(item['price']) * item['quantity'] for item in self.cart.values())

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
