from django.template.loader import render_to_string
from weasyprint import HTML
from src.voting.application.voting_finder import VotingFinder
from src.voting.infrastructure.mysql_voting_repository import MySQLVotingRepository
from src.voting.infrastructure.builders.voting_builder import VotingBuilder
from django.template import Template, Context

def generate_votacion_pdf(voting_id):
    builder = VotingBuilder()
    repository = MySQLVotingRepository(builder)
    finder = VotingFinder(repository)
    votacion = finder.find_voting_by_id(builder.build({"id": voting_id}))
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
                                                    <p><strong>Tipo de Votación:</strong> {{ tipo_votacion }}</p>
                                                    <p><strong>Sistema de Votación:</strong> {{ sistema_votacion }}</p>
                                                    <p><strong>N° de Votos Emitidos:</strong> {{ votos_emitidos }}</p>
                                                    <p><strong>Votos Válidos:</strong> {{ votos_validos }}</p>
                                                    <p><strong>Votos en Blanco:</strong> {{ votos_blanco }}</p>
                                                </div>
                                                <div class="resultados">
                                                    <h2>RESULTADOS</h2>
                                                    <ul>
                                                        {% for candidato in candidatos %}
                                                        <li>
                                                            <strong>{{ candidato.nombre }}</strong> 
                                                            <span class="stars">
                                                                {% for i in range(candidato.estrellas) %}
                                                                    ★
                                                                {% endfor %}
                                                            </span>
                                                            <span class="stars-empty">
                                                                {% for i in range(5 - candidato.estrellas) %}
                                                                    ★
                                                                {% endfor %}
                                                            </span>
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
    context = {'nombre': votacion.name, 'tipo_votacion': votacion.winners, 'sistema_votacion': votacion.voting_system, 'fecha_inicio': votacion.start_date, 'fecha_fin': votacion.end_date, 'votacion_id': votacion.id }
    template = Template(template_string)
    rendered_string = template.render(Context(context))
    html = HTML(string=rendered_string)
    with open(f'/home/jesus/TFG/{votacion.id}.pdf', 'wb') as f:
        f.write(html)
    print(f'PDF generado para la votación {voting_id}')