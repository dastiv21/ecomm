import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from faker import Faker
from commerce.models import Category, Product, Order  # Replace 'shop' with your app name

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed the database with sample data'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Predefined category names
        category_names = ["Electronics", "Books", "Clothing", "Home & Kitchen", "Toys"]
        categories = []

        # Create 5 Categories
        for name in category_names:
            category, created = Category.objects.get_or_create(name=name)
            categories.append(category)
            self.stdout.write(self.style.SUCCESS(f'Category created: {name}'))

        # Create 10 Products
        products = []
        users = User.objects.all()
        if not users.exists():
            self.stderr.write("No users found! Create at least one user before running this command.")
            return

        product_data = [
            {"name": "Smartphone", "description": "High-end smartphone with advanced features.", "price": 699.99},
            {"name": "Laptop", "description": "Lightweight laptop for professionals.", "price": 999.99},
            {"name": "Headphones", "description": "Noise-cancelling over-ear headphones.", "price": 199.99},
            {"name": "Cookware Set", "description": "Non-stick cookware set for your kitchen.", "price": 89.99},
            {"name": "Desk Lamp", "description": "LED desk lamp with adjustable brightness.", "price": 29.99},
            {"name": "T-shirt", "description": "Cotton t-shirt available in various sizes.", "price": 19.99},
            {"name": "Book", "description": "Bestselling novel by a renowned author.", "price": 14.99},
            {"name": "Toy Car", "description": "Remote-controlled toy car for kids.", "price": 49.99},
            {"name": "Blender", "description": "High-speed blender for smoothies and more.", "price": 59.99},
            {"name": "Board Game", "description": "Fun board game for the whole family.", "price": 39.99}
        ]

        for data in product_data:
            product = Product.objects.create(
                name=data["name"],
                description=data["description"],
                price=Decimal(data["price"]).quantize(Decimal('0.01')),
                stock=random.randint(10, 100),
                image=fake.image_url(),  # You might need to update this based on your ImageField config
                category=random.choice(categories),
                created_by=random.choice(users)
            )
            products.append(product)
            self.stdout.write(self.style.SUCCESS(f'Product created: {data["name"]}'))

        # Create 20 Orders
        for i in range(20):
            user = random.choice(users)
            selected_products = random.sample(products, k=random.randint(1, 5))
            total_price = sum([product.price for product in selected_products])

            order = Order.objects.create(
                user=user,
                total_price=total_price
            )
            order.products.set(selected_products)
            self.stdout.write(self.style.SUCCESS(f'Order created for user {user.username} with total price {total_price}'))

        self.stdout.write(self.style.SUCCESS('Seeding completed successfully!'))
