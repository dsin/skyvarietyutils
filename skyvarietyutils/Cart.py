class Cart:
  def __init__(self):
    pass

  def add(self, item):
    cart = self.get()

    cart.append(item)

    self.set(cart)
    return cart

  def update(self, index, item):
    cart = self.get()

    for key, value in item.items():
      cart[index][key] = value

    self.set(cart)
    return cart

  def delete(self, index):
    cart = self.get()

    del cart[index]

    self.set(cart)
    return cart

  def clear(self):
    pass

  def set(self, cart):
    pass

  def get(self):
    pass
