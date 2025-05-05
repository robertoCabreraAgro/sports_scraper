import requests
from bs4 import BeautifulSoup
import logging
import time
from datetime import datetime

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("scraper.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TennisScraper:
    """
    Clase para manejar el scraping de datos de partidos de tenis.
    """
    def __init__(self, url):
        """
        Inicializa el scraper con la URL de la página de tenis.
        
        Args:
            url: URL de la página de tenis a scrapear
        """
        self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def _get_page_content(self):
        """
        Realiza la petición HTTP y obtiene el contenido de la página.
        
        Returns:
            Contenido HTML de la página o None si hay un error
        """
        try:
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()  # Lanza excepción si la petición no es exitosa
            return response.text
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al obtener la página: {e}")
            return None
    
    def _parse_player_names(self, match_element):
        """
        Extrae los nombres de los jugadores de un elemento de partido.
        
        Args:
            match_element: Elemento HTML que contiene la información del partido
            
        Returns:
            Tupla con los nombres de los jugadores (player_1, player_2)
        """
        try:
            # Esta implementación es genérica y debe adaptarse a la estructura real de la página
            players = match_element.select('.player-name')
            player_1 = players[0].text.strip() if len(players) > 0 else "Unknown"
            player_2 = players[1].text.strip() if len(players) > 1 else "Unknown"
            return player_1, player_2
        except Exception as e:
            logger.error(f"Error al extraer nombres de jugadores: {e}")
            return "Unknown", "Unknown"
    
    def _parse_scores(self, match_element):
        """
        Extrae las puntuaciones de un elemento de partido.
        
        Args:
            match_element: Elemento HTML que contiene la información del partido
            
        Returns:
            Tupla con las puntuaciones (score_1, score_2, score_total)
        """
        try:
            # Esta implementación es genérica y debe adaptarse a la estructura real de la página
            scores = match_element.select('.score')
            score_1 = scores[0].text.strip() if len(scores) > 0 else "0"
            score_2 = scores[1].text.strip() if len(scores) > 1 else "0"
            
            # Calcular el puntaje total (puede variar según cómo se calcule en el tenis)
            try:
                score_total = str(int(score_1) + int(score_2))
            except ValueError:
                # Si los scores no son números enteros simples
                score_total = f"{score_1}-{score_2}"
                
            return score_1, score_2, score_total
        except Exception as e:
            logger.error(f"Error al extraer puntuaciones: {e}")
            return "0", "0", "0"
    
    def _parse_tournament(self, match_element):
        """
        Extrae el nombre del torneo de un elemento de partido.
        
        Args:
            match_element: Elemento HTML que contiene la información del partido
            
        Returns:
            Nombre del torneo
        """
        try:
            # Esta implementación es genérica y debe adaptarse a la estructura real de la página
            tournament_element = match_element.select_one('.tournament-name')
            return tournament_element.text.strip() if tournament_element else "Unknown Tournament"
        except Exception as e:
            logger.error(f"Error al extraer nombre del torneo: {e}")
            return "Unknown Tournament"
    
    def _parse_timestamp(self, match_element):
        """
        Extrae la fecha y hora del partido.
        
        Args:
            match_element: Elemento HTML que contiene la información del partido
            
        Returns:
            Fecha y hora del partido en formato string
        """
        try:
            # Esta implementación es genérica y debe adaptarse a la estructura real de la página
            time_element = match_element.select_one('.match-time')
            return time_element.text.strip() if time_element else datetime.now().strftime("%Y-%m-%d %H:%M")
        except Exception as e:
            logger.error(f"Error al extraer timestamp: {e}")
            return datetime.now().strftime("%Y-%m-%d %H:%M")
    
    def scrape_matches(self):
        """
        Realiza el scraping de los partidos de tenis.
        
        Returns:
            Lista de diccionarios con los datos de los partidos
        """
        logger.info(f"Iniciando scraping en {self.url}")
        html_content = self._get_page_content()
        
        if not html_content:
            logger.error("No se pudo obtener el contenido de la página")
            return []
        
        soup = BeautifulSoup(html_content, 'html.parser')
        matches_data = []
        
        try:
            # Buscar todas las tablas o elementos que contienen partidos
            # Esta selección debe adaptarse a la estructura real de la página
            match_elements = soup.select('.match-container')
            
            logger.info(f"Se encontraron {len(match_elements)} partidos")
            
            for match in match_elements:
                player_1, player_2 = self._parse_player_names(match)
                score_1, score_2, score_total = self._parse_scores(match)
                tournament = self._parse_tournament(match)
                timestamp = self._parse_timestamp(match)
                
                match_data = {
                    'player_1': player_1,
                    'player_2': player_2,
                    'score_1': score_1,
                    'score_2': score_2,
                    'score_total': score_total,
                    'timestamp': timestamp,
                    'tournament': tournament,
                    'sport_type': 'tennis'
                }
                
                matches_data.append(match_data)
                logger.info(f"Partido procesado: {player_1} vs {player_2}")
                
                # Espera entre peticiones para evitar sobrecarga
                time.sleep(0.5)
                
        except Exception as e:
            logger.error(f"Error durante el scraping: {e}")
        
        logger.info(f"Scraping completado. Se obtuvieron {len(matches_data)} partidos")
        return matches_data


# Definimos una fábrica de scrapers para facilitar la escalabilidad a otros deportes
class ScraperFactory:
    """
    Fábrica para crear diferentes tipos de scrapers según el deporte.
    """
    @staticmethod
    def get_scraper(sport_type, url):
        """
        Devuelve el scraper adecuado según el tipo de deporte.
        
        Args:
            sport_type: Tipo de deporte ('tennis', 'basketball', 'football', etc.)
            url: URL de la página a scrapear
            
        Returns:
            Instancia del scraper apropiado
        """
        if sport_type == 'tennis':
            return TennisScraper(url)
        # En el futuro, se pueden agregar más deportes
        # elif sport_type == 'basketball':
        #     return BasketballScraper(url)
        # elif sport_type == 'football':
        #     return FootballScraper(url)
        else:
            logger.warning(f"Tipo de deporte no soportado: {sport_type}. Usando TennisScraper como fallback.")
            return TennisScraper(url)
