from flask import jsonify, request, Blueprint
from app import db
from app.scraper import realizar_scraping_futbol, realizar_scraping_tenis, realizar_scraping_baloncesto
from app.models import PartidoFutbol, PartidoTenis, PartidoBaloncesto
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear un Blueprint para las rutas del scraper
scraper_bp = Blueprint('scraper', __name__, url_prefix='/scraper')

@scraper_bp.route('/futbol', methods=['POST'])
def scraper_futbol():
    """
    Endpoint para realizar scraping de partidos de fútbol.
    
    Returns:
        JSON: Mensaje de resultado y número de partidos procesados.
    """
    try:
        resultado = realizar_scraping_futbol()
        return jsonify(resultado), 200 if resultado['status'] == 'success' else 500
    except Exception as e:
        logger.error(f"Error en el endpoint de scraping de fútbol: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Error inesperado: {str(e)}'
        }), 500

@scraper_bp.route('/tenis', methods=['POST'])
def scraper_tenis():
    """
    Endpoint para realizar scraping de partidos de tenis.
    
    Returns:
        JSON: Mensaje de resultado y número de partidos procesados.
    """
    try:
        resultado = realizar_scraping_tenis()
        return jsonify(resultado), 200 if resultado['status'] == 'success' else 500
    except Exception as e:
        logger.error(f"Error en el endpoint de scraping de tenis: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Error inesperado: {str(e)}'
        }), 500

@scraper_bp.route('/baloncesto', methods=['POST'])
def scraper_baloncesto():
    """
    Endpoint para realizar scraping de partidos de baloncesto.
    
    Returns:
        JSON: Mensaje de resultado y número de partidos procesados.
    """
    try:
        resultado = realizar_scraping_baloncesto()
        return jsonify(resultado), 200 if resultado['status'] == 'success' else 500
    except Exception as e:
        logger.error(f"Error en el endpoint de scraping de baloncesto: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Error inesperado: {str(e)}'
        }), 500

# Crear un Blueprint para las rutas de consulta
api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/futbol', methods=['GET'])
def get_partidos_futbol():
    """
    Endpoint para obtener los partidos de fútbol almacenados.
    
    Query Parameters:
        equipo (str, opcional): Filtrar por nombre de equipo (local o visitante).
        competencia (str, opcional): Filtrar por nombre de competencia.
        
    Returns:
        JSON: Lista de partidos de fútbol.
    """
    try:
        query = PartidoFutbol.query
        
        # Aplicar filtros si están presentes
        equipo = request.args.get('equipo')
        if equipo:
            query = query.filter((PartidoFutbol.equipo_local.ilike(f'%{equipo}%')) | 
                                (PartidoFutbol.equipo_visitante.ilike(f'%{equipo}%')))
        
        competencia = request.args.get('competencia')
        if competencia:
            query = query.filter(PartidoFutbol.competencia.ilike(f'%{competencia}%'))
        
        # Ordenar por fecha descendente
        partidos = query.order_by(PartidoFutbol.fecha.desc()).all()
        
        return jsonify({
            'status': 'success',
            'data': [partido.to_dict() for partido in partidos],
            'count': len(partidos)
        }), 200
    
    except Exception as e:
        logger.error(f"Error al obtener partidos de fútbol: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Error al obtener datos: {str(e)}'
        }), 500

@api_bp.route('/tenis', methods=['GET'])
def get_partidos_tenis():
    """
    Endpoint para obtener los partidos de tenis almacenados.
    
    Query Parameters:
        jugador (str, opcional): Filtrar por nombre de jugador.
        torneo (str, opcional): Filtrar por nombre de torneo.
        
    Returns:
        JSON: Lista de partidos de tenis.
    """
    try:
        query = PartidoTenis.query
        
        # Aplicar filtros si están presentes
        jugador = request.args.get('jugador')
        if jugador:
            query = query.filter((PartidoTenis.jugador1.ilike(f'%{jugador}%')) | 
                                (PartidoTenis.jugador2.ilike(f'%{jugador}%')))
        
        torneo = request.args.get('torneo')
        if torneo:
            query = query.filter(PartidoTenis.torneo.ilike(f'%{torneo}%'))
        
        # Ordenar por fecha descendente
        partidos = query.order_by(PartidoTenis.fecha.desc()).all()
        
        return jsonify({
            'status': 'success',
            'data': [partido.to_dict() for partido in partidos],
            'count': len(partidos)
        }), 200
    
    except Exception as e:
        logger.error(f"Error al obtener partidos de tenis: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Error al obtener datos: {str(e)}'
        }), 500

@api_bp.route('/baloncesto', methods=['GET'])
def get_partidos_baloncesto():
    """
    Endpoint para obtener los partidos de baloncesto almacenados.
    
    Query Parameters:
        equipo (str, opcional): Filtrar por nombre de equipo (local o visitante).
        liga (str, opcional): Filtrar por nombre de liga.
        
    Returns:
        JSON: Lista de partidos de baloncesto.
    """
    try:
        query = PartidoBaloncesto.query
        
        # Aplicar filtros si están presentes
        equipo = request.args.get('equipo')
        if equipo:
            query = query.filter((PartidoBaloncesto.equipo_local.ilike(f'%{equipo}%')) | 
                                (PartidoBaloncesto.equipo_visitante.ilike(f'%{equipo}%')))
        
        liga = request.args.get('liga')
        if liga:
            query = query.filter(PartidoBaloncesto.liga.ilike(f'%{liga}%'))
        
        # Ordenar por fecha descendente
        partidos = query.order_by(PartidoBaloncesto.fecha.desc()).all()
        
        return jsonify({
            'status': 'success',
            'data': [partido.to_dict() for partido in partidos],
            'count': len(partidos)
        }), 200
    
    except Exception as e:
        logger.error(f"Error al obtener partidos de baloncesto: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Error al obtener datos: {str(e)}'
        }), 500

# Blueprint para página principal y rutas adicionales
main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def index():
    """Página principal con información del API."""
    return jsonify({
        'name': 'API de Scraper Deportivo',
        'description': 'API para obtener datos de partidos deportivos mediante scraping.',
        'endpoints': {
            'scraper': {
                'futbol': '/scraper/futbol [POST]',
                'tenis': '/scraper/tenis [POST]',
                'baloncesto': '/scraper/baloncesto [POST]'
            },
            'api': {
                'futbol': '/api/futbol [GET]',
                'tenis': '/api/tenis [GET]',
                'baloncesto': '/api/baloncesto [GET]'
            }
        },
        'version': '1.0.0'
    }), 200