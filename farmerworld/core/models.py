from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class User_Details(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    profile_picture = models.URLField(
        null=True, 
        default='/static/images/logo/logo1.png'
    )
    role = models.CharField(max_length=10)
    district = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=10, null=True)
    email = models.EmailField(null=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Seller(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15, null=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    flat_details = models.CharField(max_length=255, null=True, blank=True)
    area_details = models.CharField(max_length=255, null=True, blank=True)
    landmark = models.CharField(max_length=255, null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True, blank=True)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.name}"

class Crop(models.Model):
    name = models.CharField(max_length=1000)
    soil_type = models.CharField( max_length=1000,blank=True, null=True)
    season = models.CharField(max_length=100)
    image = models.ImageField(upload_to='crops/')
    description = models.TextField(max_length=1000)

    def __str__(self):
        return self.name

class VegetableRate(models.Model):
    name = models.CharField(max_length=250)
    min_rate = models.DecimalField(max_digits=10, decimal_places=2)
    max_rate = models.DecimalField(max_digits=10, decimal_places=2)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    location = models.CharField(max_length=100)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.user.username

class Product(models.Model):
    seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.CharField(max_length=50)
    image = models.ImageField(upload_to='products/')
    posted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Scheme(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    link = models.URLField(blank=True, null=True)
    published_on = models.DateField()

    def __str__(self):
        return self.title

class TipArticle(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='tips/articles/', null=True, blank=True)
    published_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class TipVideo(models.Model):
    caption = models.CharField(max_length=200)
    video_url = models.URLField()
    thumbnail = models.ImageField(upload_to='tips/videos/', null=True, blank=True)
    published_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.caption

class CommunityPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='community/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.user.username} at {self.created_at}"

class Comment(models.Model):
    post = models.ForeignKey(CommunityPost, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} on Post {self.post.id}"


class Month(models.Model):
    name = models.CharField(max_length=20)  

    def __str__(self):
        return self.name

class Season(models.Model):
    name = models.CharField(max_length=50)  
    months = models.ManyToManyField(Month)

    def __str__(self):
        return self.name


class SoilType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    best_crops = models.TextField(help_text="List of crops that grow well in this soil")
    water_usage = models.CharField(
        max_length=50,
        choices=[
            ('Low', 'Low'),
            ('Medium', 'Medium'),
            ('High', 'High')
        ]
    )
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    source = models.CharField(max_length=100, blank=True)
    link = models.URLField(blank=True, null=True)
    published_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.name} ({self.email})"




# Do NOT define this yourself — this is just for reference

class UserSocialAuth(models.Model):
    crop = models.ForeignKey(User, on_delete=models.CASCADE)
    provider = models.CharField(max_length=32)
    uid = models.CharField(max_length=255)
    extra_data = models.JSONField(default=dict)

    class Meta:
        unique_together = ('provider', 'uid')



class PhoneOTP(models.Model):
    phone = models.CharField(max_length=15, unique=True)
    otp = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.phone


class MobileOTP(models.Model):
    mobile = models.CharField(max_length=10, unique=True)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Dispatched', 'Dispatched'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Order #{self.id} - {self.customer.username}"

class DeliveryPerson(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(blank=True, null=True)
    location = models.CharField(max_length=100)
    vehicle_number = models.CharField(max_length=20)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name
class Transaction(models.Model):
    TRANSACTION_STATUS_CHOICES = [
        ('Success', 'Success'),
        ('Failed', 'Failed'),
        ('Pending', 'Pending'),
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100, unique=True)
    payment_method = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=TRANSACTION_STATUS_CHOICES)
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Txn {self.transaction_id} - {self.status}"
class DeliveryInfo(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    delivery_person = models.ForeignKey(DeliveryPerson, on_delete=models.SET_NULL, null=True)
    assigned_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(blank=True, null=True)
    delivery_status = models.CharField(
        max_length=20,
        choices=[('Assigned', 'Assigned'), ('Out for Delivery', 'Out for Delivery'), ('Delivered', 'Delivered')],
        default='Assigned'
    )
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Delivery for Order #{self.order.id}"
