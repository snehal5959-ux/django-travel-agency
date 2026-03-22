from django.db import models
from django.contrib.auth.models import User



class TravelPackage(models.Model):
    """
    Represents a travel package with details like name, destination, price, and rating.
    Can have multiple tags for categorization.
    """
    name = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    package_type = models.CharField(max_length=50, choices=[
        ('Beach', 'Beach'),
        ('Adventure', 'Adventure'),
        ('Cultural', 'Cultural'),
        ('Family', 'Family'),
        ('Relaxation', 'Relaxation'),
        ('City', 'City'),
    ])
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.CharField(max_length=50)  
    rating = models.DecimalField(max_digits=3, decimal_places=1)  
    description = models.TextField()
    available = models.BooleanField(default=True)  
    tags = models.ManyToManyField('Tag', related_name='travel_packages', blank=True)
    image = models.ImageField(upload_to="packages/", null=True, blank=True)
    Hault_details = models.CharField(max_length=255, blank=True, null=True)
    mode_of_travelling = models.CharField(max_length=255, blank=True, null=True)
    food_services = models.CharField(max_length=255, blank=True, null=True)
    supervisor = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name 



class Booking(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookings',
        db_index=True  # ✅ ADD INDEX FOR FASTER QUERIES
    )

    name = models.CharField(max_length=255)
    email = models.EmailField()
    address = models.TextField(blank=True, null=True)

    gender = models.CharField(
        max_length=10,
        choices=[('Male', 'Male'), ('Female', 'Female'), ('None', 'None')],
        default='None'
    )

    datetime = models.DateTimeField()

    num_adults = models.PositiveIntegerField(default=0)
    num_children = models.PositiveIntegerField(default=0)

    payment_method = models.CharField(
        max_length=20,
        choices=[('Online', 'Online'), ('On Site', 'On Site')],
        default='On Site'
    )

    package = models.ForeignKey(
        TravelPackage,
        on_delete=models.CASCADE,
        related_name='bookings',
        db_index=True  # ✅ ADD INDEX FOR FASTER QUERIES
    )

    payment_status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Paid', 'Paid'),
            ('Cancelled', 'Cancelled')
        ],
        default='Pending'
    )

    booking_status = models.CharField(
    max_length=20,
    choices=[
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    ],
    default='Pending'
    )

    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)

    cancel_reason = models.TextField(blank=True, null=True)
    cancelled_at = models.DateTimeField(blank=True, null=True)

    refund_status = models.CharField(
        max_length=20,
        choices=[
            ('Not Applicable', 'Not Applicable'),
            ('Pending', 'Pending'),
            ('Refunded', 'Refunded'),
        ],
        default='Not Applicable'
    )

    refund_requested = models.BooleanField(default=False)
    refund_requested_at = models.DateTimeField(null=True, blank=True)

    # ✅ RAZORPAY FIELDS (INSIDE THE CLASS)
    razorpay_order_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    transaction_id = models.CharField(
    max_length=200,
    blank=True,
    null=True
)

    payment_screenshot = models.ImageField(
    upload_to="payment_screenshots/",
    blank=True,
    null=True
)

    razorpay_signature = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    def __str__(self):
        # ✅ OPTIMIZED: Avoid accessing user.username which triggers separate query
        # Use the already-loaded self.name instead
        return f"{self.name} - {self.package.name}"

class InboxMessage(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="inbox_messages"
    )
    subject = models.CharField(max_length=200)
    message = models.TextField()
    sent_by_admin = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"To {self.user.username} - {self.subject}"
    

class ContactMessage(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    name = models.CharField(max_length=100)
    email = models.EmailField()
    screenshot = models.ImageField(
        upload_to="payment_screenshots/",
        blank=True,
        null=True
    )
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class Tag(models.Model):
    """
    Represents a tag for categorizing travel packages (e.g., 'Romantic', 'Adventure').
    """
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Userdetails(models.Model):
    name= models.CharField(max_length= 200)
    email=models.CharField(max_length=50)
    passwd=models.CharField(max_length=6)
    
    def __str__(self):
        return self.name
    


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    gender = models.CharField(
        max_length=10,
        choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')],
        blank=True
    )
    company=models.CharField(max_length=300, blank=True)

    def __str__(self):
        return self.user.username
    
class Gallery(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='gallery/')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='blogs/')
    short_desc = models.TextField()
    full_content = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.ForeignKey(TravelPackage, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    people = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('Upcoming','Upcoming'),('Completed','Completed'),('Cancelled','Cancelled')])

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.ForeignKey(TravelPackage, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255)
    message = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)  # 1-5 stars
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.package} ({self.rating}★)"
    
class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)  # ✅ ADD INDEX
    package = models.ForeignKey(TravelPackage, on_delete=models.CASCADE, db_index=True)  # ✅ ADD INDEX
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'package')

    def __str__(self):
        # ✅ OPTIMIZED: Just use IDs instead of fetching related objects
        return f"Favorite: User {self.user_id} - Package {self.package_id}"
    

class Country(models.Model):
    name = models.CharField(max_length=100, db_index=True)  # ✅ ADD INDEX
    cover_image = models.ImageField(upload_to='countries/', blank=True, null=True)

    place1_name = models.CharField(max_length=100, blank=True, null=True)
    place1_image = models.ImageField(upload_to='places/', blank=True, null=True)
    place1_description = models.TextField(blank=True, null=True)

    place2_name = models.CharField(max_length=100, blank=True, null=True)
    place2_image = models.ImageField(upload_to='places/', blank=True, null=True)
    place2_description = models.TextField(blank=True, null=True)

    place3_name = models.CharField(max_length=100, blank=True, null=True)
    place3_image = models.ImageField(upload_to='places/', blank=True, null=True)
    place3_description = models.TextField(blank=True, null=True)

    place4_name = models.CharField(max_length=100, blank=True, null=True)
    place4_image = models.ImageField(upload_to='places/', blank=True, null=True)
    place4_description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    


class Place(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='places', db_index=True)  # ✅ ADD INDEX
    name = models.CharField(max_length=150)
    description = models.TextField()
    image = models.ImageField(upload_to='places/')
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    



