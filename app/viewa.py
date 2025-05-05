from flask import Blueprint, jsonify, request, current_app
import logging
from functools import wraps
from app import db
from app.models import MatchStats
from app.scraper import ScraperFactory

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear blueprint para las rutas
main_bp = Blueprint('main', __name__)

def require_api_key(f):
    """
    Decorador para proteger los endpoints con una clave API.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if api_key and api_key == current_app.config['API_KEY']:
            return f(*args, **kwargs)
        else:
            return jsonify({'error': 'API key inválida o no proporcionada'}), 401
    return decorated_function

@main_bp.route('/', methods=['GET'])
def index():
    """
    Ruta principal para verificar que la API está funcionando.
    """
    return jsonify({
        'message': 'API de Scraper Deportivo',
        'version': '1.0.0',
        'status': 'online'
    })

@main_bp.route('/scrape', methods=['GET'])
@require_api_key
def scrape():
    """
    Endpoint para realizar el scraping de datos deportivos y almacenarlos en la base de datos.
    
    Query parameters:
        - url: URL del sitio a scrapear (obligatorio)
        - sport_type: Tipo de deporte (opcional, default: tennis)
    
    Returns:
        Respuesta JSON con el resultado de la operación
    """
    url = request.args.get('url')
    sport_type = request.args.get('sport_type', 'tennis')
    
    if not url:
        return jsonify({'error': 'URL no proporcionada. Use ?url=<url_del_sitio>'}), 400
    
    try:
        # Obtener el scraper adecuado según el tipo de deporte
        scraper = ScraperFactory.get_scraper(sport_type, url)
        
        # Realizar el scraping
        matches_data = scraper.scrape_matches()
        
        if not matches_data:
            return jsonify({'message': 'No se encontraron datos de partidos'}), 404
        
        # Guardar los datos en la base de datos
        saved_count = 0
        for match_data in matches_data:
            match_stats = MatchStats(**match_data)
            db.session.add(match_stats)
            saved_count += 1
        
        db.session.commit()
        
        return jsonify({
            'message': 'Datos obtenidos y guardados correctamente',
            'matches_saved': saved_count
        })
        
    except Exception as e:
        logger.error(f"Error en el scraping: {str(e)}")
        db.session.rollback()
        return jsonify({'error': f'Error al procesar la solicitud: {str(e)}'}), 500

@main_bp.route('/matches', methods=['GET'])
def get_matches():
    """
    Endpoint para obtener los partidos almacenados en la base de datos.
    
    Query parameters:
        - sport_type: Filtrar por tipo de deporte (opcional)
        - tournament: Filtrar por torneo (opcional)
        - player: Filtrar por jugador (opcional)
        - limit: Limitar número de resultados (opcional, default: 50)
        
    Returns:
        Lista de partidos en formato JSON
    """
    try:
        # Obtener parámetros de consulta
        sport_type = request.args.get('sport_type')
        tournament = request.args.get('tournament')
        player = request.args.get('player')
        limit = int(request.args.get('limit', 50))
        
        # Construir consulta
        query = MatchStats.query
        
        if sport_type:
            query = query.filter_by(sport_type=sport_type)
        
        if tournament:
            query = query.filter_by(tournament=tournament)
        
        if player:
            query = query.filter((MatchStats.player_1.ilike(f'%{player}%')) | 
                                (MatchStats.player_2.ilike(f'%{player}%')))
        
        # Limitar y ordenar resultados
        matches = query.order_by(MatchStats.created_at.desc()).limit(limit).all()
        
        return jsonify({
            'matches': [match.to_dict() for match in matches],
            'count': len(matches)
        })
        
    except Exception as e:
        logger.error(f"Error al obtener partidos: {str(e)}")
        return jsonify({'error': f'Error al procesar la solicitud: {str(e)}'}), 500

@main_bp.route('/matches/<int:match_id>', methods=['GET'])
def get_match(match_id):
    """
    Endpoint para obtener un partido específico por su ID.
    
    Args:
        match_id: ID del partido a buscar
        
    Returns:
        Datos del partido en formato JSON
    """
    try:
        match = MatchStats.query.get(match_id)
        
        if not match:
            return jsonify({'error': 'Partido no encontrado'}), 404
        
        return jsonify(match.to_dict())
        
    except Exception as e:
        logger.error(f"Error al obtener partido {match_id}: {str(e)}")
        return jsonify({'error': f'Error al procesar la solicitud: {str(e)}'}), 500
