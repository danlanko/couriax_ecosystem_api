import random
import string
from apis.products.models import Product


def generate_product_sku(num):
    return ''.join(random.choice(string.digits) for i in range(num))