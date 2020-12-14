class Seat:
    def __init__(self, block, row, place, price=0):
        self.block = block
        self.row = row
        self.place = place
        self.price = 20 * block + 3 * row + 0.99 if price == 0 else price

    def __str__(self):
        return "Block: {}, Row: {}, Place: {}, Price: {} $".format(self.block, self.row, self.place, self.price)
