import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from django.contrib.auth.models import User
from core.models import (Card)
import datetime
#GraphQl Type for Cards
class CardType(DjangoObjectType):
    class Meta:
        model = Card

class Query(ObjectType):
    card = graphene.Field(CardType, id=graphene.Int())
    cards = graphene.List(CardType)

    def resolve_card(self, info, *kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Card.objects.get(pk=id)
        return None

    def resolve_cards(self, info, *kwargs):
        return Card.objects.all()

class CardInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    description = graphene.String()
    importance = graphene.Int()
    limit = graphene.String()
    finished = graphene.Boolean()
    author = graphene.Int()

class CreateCard(graphene.Mutation):
    class Arguments:
        input = CardInput(required=True)

    ok = graphene.Boolean()
    card = graphene.Field(CardType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        print(input.author)
        print(User.objects.get(pk=input.author))
        card_instance = Card(
            name=input.name,
            description=input.description,
            importance=input.importance,
            limit=datetime.datetime.strptime(input.limit, "%Y-%m-%d %H:%M"),
            author=User.objects.get(pk=input.author)
        )
        card_instance.save()
        return CreateCard(ok=ok, card=card_instance)

class UpdateCard(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = CardInput(required=True)

    ok = graphene.Boolean()
    card = graphene.Field(CardType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        card_instance = Card.objects.get(pk=id)
        if card_instance:
            ok = True
            card_instance.name = input.name
            card_instance.description = input.description
            card_instance.importance = input.importance
            card_instance.limit = datetime.datetime.strptime(input.limit, "%Y-%m-%d %H:%M")
            card_instance.finished = input.finished
            card_instance.save()
            return UpdateCard(ok=ok, card=card_instance)
        return UpdateCard(ok=ok, card=None)

class DeleteCard(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    ok = graphene.Boolean()

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        card_instance = Card.objects.get(pk=id)
        if card_instance:
            ok = True
            card_instance.delete()
            return DeleteCard(ok=ok)
        return DeleteCard(ok=ok)

class Mutation(graphene.ObjectType):
    create_card = CreateCard.Field()
    update_card = UpdateCard.Field()
    delete_card = DeleteCard.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
