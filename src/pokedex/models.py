from django.db import models

class Type(models.Model):
    TYPES = (
        ("normal", "Normal"), ("fighting", "Fighting"), ("flying", "Flying"),
        ("poison", "Poison"), ("ground", "Ground"), ("rock", "Rock"), ("bug", "Bug"),
        ("ghost", "Ghost"), ("steel", "Steel"), ("fire", "Fire"), ("water", "Water"),
        ("grass", "Grass"), ("electric", "Electric"), ("psychic", "Psychic"), ("ice", "Ice"),
        ("dragon", "Dragon"), ("dark", "Dark"), ("fairy", "Fairy")
    )
    name = models.CharField(max_length=100, unique=True, null=True)
    double_damage_from = models.CharField(max_length=100, null=True)
    half_damage_from = models.CharField(max_length=100, null=True)
    no_damage_from = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name

class Ability(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True)
    description = models.TextField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

class Pokemon(models.Model):
    pokedex_id = models.IntegerField()
    name = models.CharField(max_length=100, unique=True)
    height = models.IntegerField(null=True, blank=True, default=1)
    weight = models.IntegerField(null=True, blank=True, default=1)
    description = models.TextField(max_length=300, null=True, blank=True)
    types = models.ManyToManyField(Type)
    abilities = models.ManyToManyField(Ability)
    evolution_id = models.IntegerField(null=True)
    evolution_order = models.CharField(max_length=20, null=True, blank=True)
    speed = models.IntegerField(null=True, blank=True)
    special_defense = models.IntegerField(null=True, blank=True)
    special_attack = models.IntegerField(null=True, blank=True)
    defense = models.IntegerField(null=True, blank=True)
    attack = models.IntegerField(null=True, blank=True)
    hp = models.IntegerField(null=True, blank=True)
    image_url = models.CharField(max_length=100, null=True, blank=True)
    slug = models.SlugField(null=True)

    def __str__(self):
        return self.name
