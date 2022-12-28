import json
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction
from django.core.files.base import ContentFile

from urllib import request
import csv
import os
import secrets
import random
from deep_translator import GoogleTranslator

from concurrent import futures

from manager.models.produtos import Produto, Categoria, ProdutoImagem, Tag


class Command(BaseCommand):
    help = 'Populate database with fake data'

    def add_arguments(self, parser):
        parser.add_argument('n', type=int, help='Number of records to create')

    def read_file(limit):
        with open(os.path.dirname(os.path.realpath(__file__)) + '/../../data/steam.csv', 'r', encoding='utf8') as csv_file:
            reader = csv.DictReader(csv_file, delimiter=',')
            list = [line for (i, line) in enumerate(reader)]

        offset = random.randint(0, len(list) - limit)

        return list[offset:offset + limit]

    def download_asserts(appid: int):
        if not os.path.exists(settings.MEDIA_ROOT / 'produtos'):
            os.makedirs(settings.MEDIA_ROOT / 'produtos')

        files = [
            f'thumbnail_{appid}_{secrets.token_hex(16)}.jpg',
            f'slider_1_{appid}_{secrets.token_hex(16)}.jpg'
        ]

        [thumbnail, header] = [settings.MEDIA_ROOT /
                               'produtos' / file for file in files]

        try:
            request.urlretrieve(
                f"https://cdn.cloudflare.steamstatic.com/steam/apps/{appid}/hero_capsule.jpg", thumbnail)
            request.urlretrieve(
                f"https://cdn.cloudflare.steamstatic.com/steam/apps/{appid}/capsule_616x353.jpg", header)
        except Exception as e:
            raise e

        return ['produtos/' + file for file in files]

    def put_asserts(game):
        game['assets'] = Command.download_asserts(game['appid'])

    def handle(self, *args, **options):
        n = options['n']

        self.stdout.write(self.style.NOTICE(
            f'💾 | Tentando criar {n} produtos no banco de dados...'))
        data = Command.read_file(n)

        for game in data:
            game['categories'] = game['categories'].split(';')
            game['steamspy_tags'] = game['steamspy_tags'].split(';')
            game['genres'] = game['genres'].split(';')

        categories = set(
            [tag for record in data for tag in record['steamspy_tags']])
        genres = set(
            [genre for record in data for genre in record['genres']])

        lang = settings.LANGUAGE_CODE \
            if settings.LANGUAGE_CODE.find('-') == -1 \
            else settings.LANGUAGE_CODE.split('-')[0]

        # Junta categories, tags e genres em uma lista e traduz
        to_translate = set(list(categories) + list(genres))
        self.stdout.write(self.style.NOTICE(
            f'🌐 | Traduzindo {len(to_translate)} categorias, tags e gêneros para {lang}...'))
        translator = GoogleTranslator(source='auto', target=lang)
        translated = dict(
            zip(to_translate, translator.translate_batch(list(to_translate))))

        self.stdout.write(self.style.SUCCESS(
            f'✅ | Foram realizados {len(to_translate)} traduções'))

        self.stdout.write(self.style.NOTICE(
            f'🌐 | Baixando imagens para {n} produtos...'))
        # Irá baixar em paralelo as imagens

        with futures.ThreadPoolExecutor() as executor:
            executor.map(Command.put_asserts, data)

        data = [game for game in data if 'assets' in game]

        self.stdout.write(self.style.SUCCESS(
            f'🖼 | Foram baixadas {len(data)*2} imagens'))

        with transaction.atomic():
            translated_values = list(translated.values())
            translated_keys = list(translated.keys())

            Categoria.objects.bulk_create([
                Categoria(nome=translated[category]) for category in categories
            ], ignore_conflicts=True)

            categorias = {
                translated_keys[translated_values.index(categoria.nome)]: categoria for categoria in Categoria.objects.filter(nome__in=[translated[category] for category in categories])
            }

            ProdutoImagem.objects.bulk_create([
                ProdutoImagem(imagem=game['assets'][1]) for game in data
            ])

            first_imagens = {
                game["appid"]: ProdutoImagem.objects.filter(imagem=game['assets'][1])[0] for game in data
            }

        with transaction.atomic():
            Produto.objects.bulk_create([
                Produto(
                    nome=game['name'],
                    slogan=f'Venha curtir o {game["name"]}',
                    descricao='Esse jogo de %s é o melhor para você!' % translated[
                        game['genres'][0]],
                    estoque=random.randint(5, 100),
                    preco=float(game['price']) * 5.30,
                    thumbnail=game['assets'][0],
                ) for game in data])

            for game in data:
                produto = Produto.objects.get(nome=game['name'])
                produto.imagens.add(*[first_imagens[game['appid']]] + [ProdutoImagem.objects.create(
                    imagem=game['assets'][1]) for _ in range(random.randint(0, 5))])
                produto.categorias.add(*[categorias[tag]
                                       for tag in game['steamspy_tags']])
                produto.save()

        self.stdout.write(self.style.SUCCESS(
            f'✅ | Foram criados {len(data)} produtos'))
