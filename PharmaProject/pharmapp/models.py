from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/')
    



class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    parent_category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')
    parent_subcategory = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')

    def __str__(self):
        return self.name








# class Category(models.Model):
#     name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.name


# class SubCategory(models.Model):
#     name = models.CharField(max_length=100)
#     parent_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
#     parent_subcategory = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')

#     def __str__(self):
#         return self.name





################# new current model #################

# class Menu(models.Model):
#     name = models.CharField(max_length=255)
#     parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)

#     @property
#     def depth(self):
#         depth = 0
#         node = self
#         while node.parent is not None:
#             depth += 1
#             node = node.parent
#         return depth

#     def __str__(self):
#         return self.name
    
 

