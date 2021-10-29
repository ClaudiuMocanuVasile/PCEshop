from django.db import models
from django.contrib.auth.models import User
from django import forms



class Customer(models.Model):

    """Customer table, one to one relation with User table
    """

    user = models.OneToOneField(User, on_delete = models.CASCADE,  null = True, blank = True)
    email = models.CharField(max_length = 200, null = True)
    first_name = models.CharField(max_length = 200, null = True)
    last_name = models.CharField(max_length = 200, null = True)
    image = models.ImageField(null = True, blank = True)

    @property
    def imageURL(self):

        """This property makes it so that the page won't
           throw an error when the image doesn't exist
        """

        try:
            url = self.image.url
        except:
            url = ''
        return url

    def __str__(self):

        return str(self.first_name) + " " + str(self.last_name)


class Product(models.Model):

    """Product table, some attributes are restricted up to a couple of choices
    """

    discount_opt = (
        (0, 0),
        (10, 10),
        (20, 20),
        (30, 30),
        (40, 40),
        (50, 50),
    )

    processor_type_opt = (
        ("i3", "i3"),
        ("i5", "i5"),
        ("i7", "i7"),
        ("i9", "i9"),
        ("Ryzen 3", "Ryzen 3"),
        ("Ryzen 5", "Ryzen 5"),
        ("Ryzen 7", "Ryzen 7"),
        ("Ryzen 9", "Ryzen 9"),
    )

    processor_manufacturer_opt = (
        ("Intel", "Intel"),
        ("AMD", "AMD"),
    )

    gpu = (
        ("Integrated", "Integrated"),
        ("Dedicated", "Dedicated"),
    )

    gpu_manufacturer_opt = (
        ("NVIDIA", "NVIDIA"),
        ("AMD", "AMD"),
    )

    gpu_vram_type_opt = (
        ("DDR5", "DDR5"),
        ("DDR6", "DDR6"),
    )

    ram_type_opt = (
        ("DDR3", "DDR3"),
        ("DDR4", "DDR4"),
    )

    ram_frequency_opt = (
        ("1600", "1600"),
        ("2133", "2133"),
        ("2400", "2400"),
        ("2600", "2600"),
        ("2666", "2666"),
        ("3200", "3200"),
        ("3600", "3600"),
    )

    ram_memory_opt = (
        ("4", "4"),
        ("8", "8"),
        ("16", "16"),
        ("32", "32"),
        ("64", "64"),
    )

    storage_type_opt = (
        ("HDD", "HDD"),
        ("SSD", "SSD"),
    )

    name = models.CharField(max_length = 200, null = True)

    price = models.DecimalField(max_digits = 7, decimal_places = 2)
    discount = models.IntegerField(choices = discount_opt, default = 0)

    brand = models.CharField(max_length = 200, null = True)

    processor_manufacturer = models.CharField(max_length = 200, choices = processor_manufacturer_opt, null = True, blank = True)
    processor_type = models.CharField(max_length = 200, choices = processor_type_opt, null = True, blank = True)
    processor_model = models.CharField(max_length = 200, null = True, blank = True)

    gpu = models.CharField(max_length = 200, choices = gpu, null = True, blank = True)
    gpu_manufacturer = models.CharField(max_length = 200, choices = gpu_manufacturer_opt, null = True, blank = True)
    gpu_model = models.CharField(max_length = 200, null = True, blank = True)
    gpu_vram_type = models.CharField(max_length = 200, choices = gpu_vram_type_opt, null = True, blank=True)

    ram_type = models.CharField(max_length = 200, choices = ram_type_opt, null = True, blank = True)
    ram_memory = models.CharField(max_length = 200, choices = ram_memory_opt, null = True, blank = True)
    ram_frequency = models.CharField(max_length = 200, choices = ram_frequency_opt, null = True, blank = True)

    storage_type = models.CharField(max_length = 200, choices = storage_type_opt, null = True, blank = True)
    storage = models.CharField(max_length = 200, null = True, blank = True)

    image = models.ImageField(null = True, blank = True)
    image2 = models.ImageField(null = True, blank = True)
    image3 = models.ImageField(null = True, blank = True)

    def __str__(self):

        return self.name

    @property
    def discounted_price(self):

        """This property calculates and returns price
           product price after discount
        """

        return self.price - self.price * self.discount / 100

    @property
    def image1URL(self):

        """This property makes it so that the page won't
           throw an error when the image doesn't exist
        """

        try:
            url = self.image.url
        except:
            url = ''
        return url

    @property
    def image2URL(self):
        
        """This property makes it so that the page won't
           throw an error when the image doesn't exist
        """

        try:
            url = self.image2.url
        except:
            url = ''
        return url

    @property
    def image3URL(self):
        
        """This property makes it so that the page won't
           throw an error when the image doesn't exist
        """
        
        try:
            url = self.image3.url
        except:
            url = ''
        return url


class Order(models.Model):

    """Order table, one to many relationship with Customer table
    """

    customer = models.ForeignKey(Customer, on_delete = models.SET_NULL, null = True, blank = True)
    date_ordered = models.DateTimeField(auto_now_add = True)
    complete = models.BooleanField(default = False, null = True, blank = False)
    transaction_id = models.CharField(max_length = 200, null = True)

    @property
    def get_cart_items(self):

        """This property returns the number of items in the cart"""

        orderproducts = self.orderproduct_set.all()
        total = sum([item.quantity for item in orderproducts])

        return total

    @property
    def get_cart_total(self):

        """This property returns the total price of all items in the cart"""

        orderproducts = self.orderproduct_set.all()
        total = sum([item.get_total for item in orderproducts])

        return total

    def __str__(self):

        return str(self.id)


class OrderProduct(models.Model):

    """OrderProducts table, with a foreign key to Product and Order tables
    """

    product = models.ForeignKey(Product, on_delete = models.SET_NULL, blank = True, null = True)
    order = models.ForeignKey(Order, on_delete = models.SET_NULL, blank = True, null = True)
    quantity = models.IntegerField(default = 0, null = True, blank = True)
    date_added = models.DateTimeField(auto_now_add = True)

    @property
    def get_total(self):

        total = self.product.discounted_price * self.quantity

        return total

    def __str__(self):

        return str(self.product) + "_Order_" + str(self.id)


class ShippingInfo(models.Model):

    """ShippingInfo table"""

    customer = models.ForeignKey(Customer, on_delete = models.SET_NULL, null = True, blank = True)
    order = models.ForeignKey(Order, on_delete = models.SET_NULL, null = True, blank = True)
    address = models.CharField(max_length = 200, null = True)
    city = models.CharField(max_length = 200, null = True)
    county = models.CharField(max_length = 200, null = True)
    zipcode = models.CharField(max_length = 200, null = True)
    date_added = models.DateTimeField(auto_now_add = True)

    def __str__(self):

        return self.address
