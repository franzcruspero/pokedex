import requests
from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify

from pokedex.models import Pokemon, Type, Ability

class Command(BaseCommand):
    help = 'Downloads and stores Generation 1 Pokemon into the pokedex database.'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        pokedex_id = 1
        while pokedex_id <= 151:
            type_id_list = []
            ability_id_list = []

            pokemon_url = f"https://pokeapi.co/api/v2/pokemon/{pokedex_id}"
            pokemon_species_url = f"https://pokeapi.co/api/v2/pokemon-species/{pokedex_id}"

            response = requests.get(
                pokemon_url,
                headers={"Accept": "application/json"}
            )
            species_response = requests.get(
                pokemon_species_url,
                headers={"Accept": "application/json"}
            )

            pokemon = response.json()
            pokemon_species = species_response.json()
            species_url = pokemon_species['evolution_chain']['url'].split("/")
            evolution_chain_id = species_url[6]

            pokemon_evolution_url = f"https://pokeapi.co/api/v2/evolution-chain/{evolution_chain_id}"

            evolution_chain_response = requests.get(
                pokemon_evolution_url,
                headers={"Accept": "application/json"}
            )
            evolution_chain_data = evolution_chain_response.json()

            # Stores pokemon types into Type table
            for poketype in pokemon['types']:
                type_url = f"https://pokeapi.co/api/v2/type/{poketype['type']['name']}"
                type_response = requests.get(
                    type_url,
                    headers={"Accept": "application/json"}
                )
                type_data = type_response.json()
                type_name = type_data['name']

                filter_type = str(Type.objects.filter(name=type_name).first())
                # Checks if type is already in the table
                if type_name != filter_type:
                    ddf_list = [elem['name'] for elem in type_data[
                        "damage_relations"]["double_damage_from"]]
                    hdf_list = [elem['name'] for elem in type_data[
                        "damage_relations"]["half_damage_from"]]
                    ndf_list = [elem['name'] for elem in type_data[
                        "damage_relations"]["no_damage_from"]]
                    ddf = ','.join([str(elem) for elem in ddf_list])
                    hdf = ','.join([str(elem) for elem in hdf_list])
                    ndf = ','.join([str(elem) for elem in ndf_list])
                    Type.objects.create(
                        name=type_name, 
                        double_damage_from=ddf,
                        half_damage_from=hdf,
                        no_damage_from=ndf,
                    )
                type_id_list.append(Type.objects.filter(name=type_name).values_list('id'))

            # Stores pokemon abilities into Ability table
            for ability in pokemon['abilities']:
                ability_url = f"https://pokeapi.co/api/v2/ability/{ability['ability']['name']}"
                ability_response = requests.get(
                    ability_url,
                    headers={"Accept": "application/json"}
                )
                ability_data = ability_response.json()
                ability_name = ability_data['names'][2]['name']
                description = ability_data['flavor_text_entries'][2]['flavor_text']
                filter_ability = str(Ability.objects.filter(name=ability_name).first())

                # Checks if ability is already in the table
                if ability_name != filter_ability:
                    Ability.objects.create(name=ability_name, description=description)

                ability_id_list.append(Ability.objects.filter(name=ability_name).values_list('id'))

            #Conditions for evolution order
            evolves_to_len = len(evolution_chain_data['chain']['evolves_to'])
            if pokemon['name'] == evolution_chain_data['chain']['species']['name']:
                evolution_order = 1
            for index in range(evolves_to_len):
                if pokemon['name'] == evolution_chain_data[
                        'chain']['evolves_to'][index]['species']['name']:
                    evolution_order = 2
                if len(evolution_chain_data['chain']['evolves_to'][index]['evolves_to']) > 0:
                    final_evolves_to_len = len(evolution_chain_data[
                        'chain']['evolves_to'][index]['evolves_to'])
                    for index2 in range(final_evolves_to_len):
                        if pokemon['name'] == evolution_chain_data['chain'][
                                'evolves_to'][index]['evolves_to'][index2]['species']['name']:
                            evolution_order = 3

            instance = Pokemon.objects.create(
                pokedex_id=pokemon['id'],
                name=pokemon['name'].title(),
                height=pokemon['height']/10,
                weight=pokemon['weight']/10,
                description=pokemon_species['flavor_text_entries'][1]['flavor_text'],
                slug=slugify(pokemon['name']),
                image_url=pokemon['sprites']['front_default'],
                evolution_id=evolution_chain_id,
                evolution_order=evolution_order,
                speed=pokemon['stats'][0]['base_stat'],
                special_defense=pokemon['stats'][1]['base_stat'],
                special_attack=pokemon['stats'][2]['base_stat'],
                defense=pokemon['stats'][3]['base_stat'],
                attack=pokemon['stats'][4]['base_stat'], hp=pokemon['stats'][5]['base_stat']
            )

            for item in type_id_list:
                instance.types.add(item)
            for item in ability_id_list:
                instance.abilities.add(item)
            print(pokedex_id)
            pokedex_id += 1
        