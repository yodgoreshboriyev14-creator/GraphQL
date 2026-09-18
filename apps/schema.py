from pyexpat.errors import messages

import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User
from apps.models import Category, Product


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = '__all__'

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = '__all__'

# Query -> Malumotlarni bazadan olish qismi QUERY deyiladi
class Query(graphene.ObjectType):
    all_categories = graphene.List(CategoryType)
    all_product = graphene.List(ProductType)

    def resolve_all_categories(self, info):
        return Category.objects.all()

    def resolve_all_product(self, info):
        return Product.objects.all()

# # Mutation ->  Malumotlarni o'zgartirish saqlash o'chirish MUTATION deyiladi
class CreateCategory(graphene.Mutation):
    # Response argument
    message = graphene.String()
    status = graphene.Int()

    class Arguments:
        title = graphene.String(required=True)

    def mutate(self, info, title):
        Category.objects.create(title=title)
        return CreateCategory(message = "yaratildi",  status = 201)


class UpdateCategory(graphene.Mutation):
    message = graphene.String()
    status = graphene.Int()

    class Arguments:
        id = graphene.Int(required=True)
        title = graphene.String()

    def mutate(self, info, id, title=None):
        category = Category.objects.get(pk=id)
        if title:
            category.title = title

        category.save()
        return UpdateCategory(message="Post o'zgartirildi", status = 200)

class UpdateProduct(graphene.Mutation):
    message = graphene.String()
    status = graphene.Int()

    class Arguments:
        id = graphene.Int(required=True)
        title = graphene.String()
        price = graphene.Decimal()

    def mutate(self, info, id, title=None, price=None):
        product = Product.objects.get(pk=id)

        if title:
            product.title = title

        if price:
            product.price = price

        product.save()
        return UpdateProduct(message="Product o'zgartirildi", status = 200)

class DeleteCategory(graphene.Mutation):
    message = graphene.String()
    status = graphene.Int()

    class Arguments:
        id = graphene.Int(required=True)

    def mutate(self, info, id):
        query = Category.objects.filter(pk=id)
        if query.exists():
            query.delete()

        return UpdateCategory(message="Post o'chirildi", status = 200)



class DeleteProduct(graphene.Mutation):
    message = graphene.String()
    status = graphene.Int()

    class Arguments:
        id = graphene.Int(required=True)

    def mutate(self, info, id):
        query = Product.objects.filter(pk=id)
        if query.exists():
            query.delete()

        return UpdateProduct(message="Post o'chirildi", status = 200)


class Mutation(graphene.ObjectType):
    create_category = CreateCategory.Field()
    update_category = UpdateCategory.Field()
    update_product = UpdateProduct.Field()
    delete_category = DeleteCategory.Field()
    delete_product = DeleteProduct.Field()


# Asosiy schema
schema = graphene.Schema(query=Query, mutation=Mutation)