from django.conf import settings
from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey


# Create your models here.

class Category(MPTTModel):
    name = models.CharField(verbose_name="Category Name", help_text="Required and unique", max_length=255, unique=True)
    slug = models.SlugField(verbose_name="Category Safe Url", max_length=255, unique=True)
    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")
    is_active = models.BooleanField(default=True)
    icon = models.ImageField(verbose_name="Icon", help_text="Upload an icon for the category", upload_to="category_icons/", null=True, blank=True)
    category_image = models.ImageField(verbose_name="Category Image", help_text="Upload an image for the category", upload_to="category_images/", null=True, blank=True)

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def get_absolute_url(self):
        return reverse('store:category_list', args=[self.slug])

    def __str__(self):
        return self.name


class ProductType(models.Model):
    name = models.CharField(verbose_name="Product Name", help_text="Required and unique", max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Product Type"
        verbose_name_plural = "Products Types"

    def __str__(self):
        return self.name


class ProductSpecification(models.Model):
    product_type = models.ForeignKey(ProductType, on_delete=models.RESTRICT)
    name = models.CharField(verbose_name="Name", help_text="Required and unique", max_length=255)

    class Meta:
        verbose_name = "Product Specification"
        verbose_name_plural = "Product Specifications"

    def __str__(self):
        return self.name


class Product(models.Model):
    product_type = models.ForeignKey(ProductType, on_delete=models.RESTRICT)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)

    product_title = models.CharField(verbose_name="Product Title Name", help_text="Required and unique", max_length=255,
                                     unique=True)
    description = models.TextField(verbose_name="Description", help_text="Not Required", blank=True)
    long_description = models.TextField(verbose_name="Long Description", help_text="Not Required", blank=True)
    brand = models.CharField(verbose_name="Brand name", max_length=255, blank=True)
    sku = models.CharField(verbose_name="SKU", max_length=255, blank=True)
    slug = models.SlugField(max_length=255)
    regular_price = models.DecimalField(verbose_name="Regular Price", help_text="Maximum 999.99", max_digits=5,
                                        decimal_places=2, error_messages={
            "name": {"max_length": "The price must be between 0 and 999.99 €"}})
    discount_price = models.DecimalField(verbose_name="Discount Price", help_text="Maximum 999.99", max_digits=5,
                                         decimal_places=2, error_messages={
            "name": {"max_length": "The price must be between 0 and 999.99 €"}})
    is_active = models.DateTimeField(verbose_name="Created at", auto_now_add=True, editable=False)
    created_at = models.DateTimeField("Created at", auto_now_add=True, editable=False)
    updated_at = models.DateTimeField("Updated at", auto_now=True)
    user_wishlist = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="user_wishlist", blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def get_absolute_url(self):
        return reverse("store:product", args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_title


class ProductSpecificationValue(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    specification = models.ForeignKey(ProductSpecification, on_delete=models.RESTRICT)
    value = models.CharField(verbose_name="Value", help_text="Product specification value (maximum of 255 words",
                             max_length=255)

    class Meta:
        verbose_name = "Product Specification Value"
        verbose_name_plural = "Product Specification Values"

    def __str__(self):
        return self.value


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_image")
    image = models.ImageField(verbose_name="image", help_text="Upload a product image", upload_to="images/",
                              default='images/default.png')
    alt_text = models.CharField(verbose_name="Alternative Text", help_text="Please add alternative text",
                                max_length=255, null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"
