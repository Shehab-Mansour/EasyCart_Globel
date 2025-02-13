
from django.db.models import Avg
from product.models import Product ,Rate

def update_product_rating(product):
    total_ratings = Rate.objects.filter(ProductName=product).aggregate(avg_rate=Avg('RateValue'))
    avg_rating = total_ratings['avg_rate'] or 0
    Product.objects.filter(id=product.id).update(ProductTotalRate=avg_rating)