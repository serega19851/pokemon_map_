from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(verbose_name="название", max_length=200)
    title_en = models.CharField(
        verbose_name="название анг", max_length=200, blank=True
    )
    title_jp = models.CharField(
        verbose_name="название яп", max_length=200, blank=True
    )
    image = models.ImageField(
        verbose_name="картинка", upload_to='pokemons', blank=True
    )
    text = models.TextField(
        verbose_name="описание", blank=True
    )
    previous_evolution = models.ForeignKey(
        'self',
        verbose_name="предыдущая эволюция",
        related_name="next_evolutions",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon, verbose_name="покемон",
        related_name="entities",
        on_delete=models.CASCADE
    )
    lat = models.FloatField(verbose_name="широта", blank=True, null=True)
    lon = models.FloatField(verbose_name="долгота", blank=True, null=True)
    appeared_at = models.DateTimeField(
        verbose_name="появление", blank=True, null=True
    )
    disappeared_at = models.DateTimeField(
        verbose_name="исчезновение", blank=True, null=True
    )
    level = models.IntegerField(verbose_name="уровень", blank=True, null=True)
    health = models.IntegerField(
        verbose_name="здоровье", blank=True, null=True
    )
    strength = models.IntegerField(verbose_name="сила", blank=True, null=True)
    defence = models.IntegerField(verbose_name="защита", blank=True, null=True)
    stamina = models.IntegerField(
        verbose_name="выносливость", blank=True, null=True
    )

    def __str__(self):
        return self.pokemon.title
