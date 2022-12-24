import folium
from django.http import HttpResponseNotFound
from django.shortcuts import render
from pokemon_entities.models import Pokemon, PokemonEntity
from django.utils.timezone import localtime


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    current_time = localtime()
    entity_pokemons = PokemonEntity.objects.filter(
        appeared_at__lte=current_time,
        disappeared_at__gte=current_time
    )
    pokemons = Pokemon.objects.all()
    pokemons_on_page = []
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in entity_pokemons:
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon_entity.pokemon.image.url)
        )
    for pokemon in pokemons:
        if pokemon.image:
            pokemons_on_page.append({
                'pokemon_id': pokemon.pk,
                'img_url': request.build_absolute_uri(pokemon.image.url),
                'title_ru': pokemon.title,
            })
    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    current_time = localtime()
    pokemon_entitys = PokemonEntity.objects.filter(
        appeared_at__lte=current_time,
        disappeared_at__gte=current_time
    )
    requested_pokemon = Pokemon.objects.filter(id=pokemon_id).first()
    if not requested_pokemon:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')
    previous_evolution = requested_pokemon.previous_evolution
    next_evolution = requested_pokemon.next_evolutions.first()
    pokemon = {
            "pokemon_id": pokemon_id,
            "title_ru": requested_pokemon,
            "title_en": requested_pokemon.title_en,
            "title_jp": requested_pokemon.title_jp,
            "description": requested_pokemon.text,
            "img_url": request.build_absolute_uri(
                requested_pokemon.image.url
            )
        }
    if previous_evolution:
        pokemon["previous_evolution"] = {
            "title_ru": previous_evolution,
            "pokemon_id": previous_evolution.id,
            "img_url": request.build_absolute_uri(
                previous_evolution.image.url
            )
        }
    if next_evolution:
        pokemon["next_evolution"] = {
            "title_ru": next_evolution.title,
            "pokemon_id": next_evolution.id,
            "img_url": request.build_absolute_uri(next_evolution.image.url)
            }
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entitys.filter(pokemon=pokemon_id):
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon_entity.pokemon.image.url)
        )
    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })
