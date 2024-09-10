from django.template.loader import render_to_string
from weasyprint import HTML
from src.voting.application.voting_finder import VotingFinder
from src.voting.infrastructure.mysql_voting_repository import MySQLVotingRepository
from src.voting.infrastructure.builders.voting_builder import VotingBuilder
from weasyprint import HTML
from jinja2 import Template

from src.vote.application.vote_finder import VoteFinder
from src.vote.infrastructure.mongo_vote_repository import MongoVoteRepository
from src.voting_systems.scoring import scoring_with_direct_points
from src.voting_systems.mayoritario import mayority_with_direct_points
from src.voting_systems.schuzle import schulze_method

def generate_votacion_pdf(voting_id):
    builder = VotingBuilder()
    repository = MySQLVotingRepository(builder)
    finder = VotingFinder(repository)
    vote_repository = MongoVoteRepository()
    vote_finder = VoteFinder(vote_repository)
    votacion = finder.find_voting_by_id(builder.build({"id": voting_id}))
    votes = vote_finder.find_all_votes(votacion)
    options = finder.find_options_by_voting_id(votacion)
    if votacion.voting_system == "scoring":
        winners, validos, blancos = scoring_with_direct_points(votes, options["options"])
    elif votacion.voting_system == "mayority":
        winners, validos, blancos = mayority_with_direct_points(votes,options["options"])
    elif votacion.voting_system == "schuzle":
        winners, validos, blancos = schulze_method(votes, options["options"])
    print(winners)
    print(type(winners))
    for winner in winners:
        print(winner)
        print(type(winner))
    template_string = """<!DOCTYPE html>
                                    <html lang="es">
                                    <head>
                                        <meta charset="UTF-8">
                                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                                        <title>Informe sobre Votaciones</title>
                                        <style>
                                            body {
                                                font-family: Arial, sans-serif;
                                                color: #000;
                                                margin: 0;
                                                padding: 0;
                                                display: flex;
                                                justify-content: center;
                                            }
                                            .container {
                                                width: 600px;
                                                border: 1px solid #ccc;
                                                padding: 20px;
                                            }
                                            .header {
                                                background-color: #D8D8D8;
                                                padding: 10px;
                                                text-align: center;
                                                margin-bottom: 20px;
                                            }
                                            .header h1 {
                                                margin: 0;
                                                font-size: 24px;
                                            }
                                            .content {
                                                text-align: left;
                                            }
                                            .logo {
                                                width: 50px;
                                                margin-bottom: 10px;
                                            }
                                            .stars {
                                                color: #FFD700;
                                            }
                                            .stars-empty {
                                                color: #d3d3d3;
                                            }
                                            .info {
                                                margin-bottom: 20px;
                                            }
                                            .info p {
                                                margin: 5px 0;
                                            }
                                            .resultados {
                                                margin-bottom: 20px;
                                            }
                                            .resultados h2 {
                                                margin-bottom: 10px;
                                            }
                                            .resultados ul {
                                                list-style-type: none;
                                                padding: 0;
                                            }
                                            .resultados ul li {
                                                margin-bottom: 10px;
                                            }
                                            .fecha {
                                                margin-bottom: 20px;
                                            }
                                            .nota {
                                                font-style: italic;
                                                font-size: 12px;
                                            }
                                        </style>
                                    </head>
                                    <body>
                                        <div class="container">
                                            <div class="header">
                                                        <img src="https://jesusescribano.net/logovotuco.png" alt="UCO Logo" class="logo">
                                                <h1>INFORME SOBRE VOTACIONES</h1>
                                            </div>
                                            <div class="content">
                                                <div class="info">
                                                    <p><strong>Nombre:</strong> {{ nombre }}</p>
                                                    <p><strong>Número de Ganadores:</strong> {{ tipo_votacion }}</p>
                                                    <p><strong>Sistema de Votación:</strong> {{ sistema_votacion }}</p>
                                                    <p><strong>N° de Votos Emitidos:</strong> {{ votos_emitidos }}</p>
                                                    <p><strong>Votos Válidos:</strong> {{ votos_validos }}</p>
                                                    <p><strong>Votos en Blanco:</strong> {{ votos_blanco }}</p>
                                                </div>
                                                <div class="resultados">
                                                    <h2>RESULTADOS</h2>
                                                    <ul>
                                                        {% for nombre, valor in candidatos %}
                                                        <li>
                                                            <strong>{{ nombre }}</strong> - {{ valor }}
                                                        </li>
                                                        {% endfor %}
                                                    </ul>
                                                </div>
                                                <div class="fecha">
                                                    <p><strong>Fecha de Inicio de la Votación:</strong> {{ fecha_inicio }}</p>
                                                    <p><strong>Fecha de Finalización de la Votación:</strong> {{ fecha_fin }}</p>
                                                </div>
                                                <div class="nota">
                                                    <p>Id de la votación {{votacion_id}} </p>
                                                </div>
                                            </div>
                                        </div>
                                    </body>
                                    </html> """
    context = {'nombre': votacion.name, 'tipo_votacion': votacion.winners, 'sistema_votacion': votacion.voting_system, 'votos_emitidos': validos+blancos, 'votos_validos': validos, 'votos_blanco': blancos, 'candidatos': winners,'fecha_inicio': votacion.start_date, 'fecha_fin': votacion.end_date, 'votacion_id': votacion.id }
    template = Template(template_string)
    rendered_string = template.render(context)
    html = HTML(string=rendered_string)
    output_path=f'{votacion.id}.pdf'
    html.write_pdf(output_path)

    print(f'PDF generado para la votación {voting_id}')