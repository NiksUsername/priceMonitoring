def is_big_discount(product):
    price = product.get('price', 0)
    old_price = product.get('old_price', 1)
    discount_percentage = (old_price - price) / old_price

    if old_price < 17 and discount_percentage >= 0.7:
        return True
    elif 17 <= old_price <= 31 and discount_percentage >= 0.6:
        return True
    elif 31 < old_price <= 46 and discount_percentage >= 0.5:
        return True
    elif 46 < old_price <= 100 and discount_percentage >= 0.4:
        return True
    elif old_price > 100 and discount_percentage >= 0.3:
        return True

    return False