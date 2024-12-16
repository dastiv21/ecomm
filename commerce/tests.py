import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Category, Product, Order
from django.contrib.auth.models import User

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_admin_user():
    admin_user = User.objects.create_superuser(username="admin", email="admin@example.com", password="password", is_superuser=True, is_staff=True)
    return admin_user

@pytest.fixture
def create_user():
    user = User.objects.create_user(username="user", email="user@example.com", password="password")
    return user

@pytest.fixture
def create_category():
    category = Category.objects.create(name="Test Category")
    return category

@pytest.fixture
def create_product(create_category, create_user):
    product = Product.objects.create(
        name="Test Product",
        description="Test Description",
        price=99.99,
        stock=10,
        category=create_category,
        created_by=create_user,
    )
    return product

@pytest.mark.django_db
def test_category_list(api_client, create_category):
    response = api_client.get(reverse("category-list"))
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) > 0

@pytest.mark.django_db
def test_category_creation(api_client, create_admin_user):
    api_client.force_authenticate(user=create_admin_user)
    data = {"name": "New Category"}
    response = api_client.post(reverse("category-list"), data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Category.objects.filter(name="New Category").exists()

@pytest.mark.django_db
def test_product_list(api_client, create_product):
    response = api_client.get(reverse("product-list"))
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) > 0

@pytest.mark.django_db
def test_product_creation(api_client, create_admin_user, create_category):
    api_client.force_authenticate(user=create_admin_user)
    data = {
        "name": "Another Product",
        "description": "Another Description",
        "price": "49.99",
        "stock": 5,
        "category": create_category.id,
        "created_by":create_admin_user.id
    }
    response = api_client.post(reverse("product-list"), data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Product.objects.filter(name="Another Product").exists()

# @pytest.mark.django_db
# def test_order_creation(api_client, create_admin_user, create_product):
#     api_client.force_authenticate(user=create_admin_user)
#     data = {
#         "products": [create_product.id],
#         "total_price": "99.99",
#         "user": create_admin_user.id
#     }
#     response = api_client.post(reverse("order-list"), data)
#     assert response.status_code == status.HTTP_201_CREATED
#     assert Order.objects.filter(user=create_admin_user).exists()
#
# @pytest.mark.django_db
# def test_order_list(api_client):
#     response = api_client.get(reverse("order-list"))
#     assert response.status_code == status.HTTP_200_OK
#     assert len(response.data) > 0
