from datetime import datetime
from app import db

class MatchStats(db.Model):
    """
    Modelo para almacenar estadísticas de partidos de tenis.
    La estructura es flexible para adaptarse a otros deportes en el futuro.
    """
    __tablename__ = 'match_stats'
    
    id = db.Column(db.Integer, primary_key=True)
    player_1 = db.Column(db.String(100), nullable=False)
    player_2 = db.Column(db.String(100), nullable=False)
    score_1 = db.Column(db.String(10), nullable=False)
    score_2 = db.Column(db.String(10), nullable=False)
    score_total = db.Column(db.String(10), nullable=False)
    timestamp = db.Column(db.String(50), nullable=False)
    tournament = db.Column(db.String(100), nullable=False)
    sport_type = db.Column(db.String(50), default='tennis')  # Para escalabilidad
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Match {self.player_1} vs {self.player_2} at {self.tournament}>'
    
    def to_dict(self):
        """
        Convierte el modelo a un diccionario.
        Útil para devolver respuestas JSON en las APIs.
        """
        return {
            'id': self.id,
            'player_1': self.player_1,
            'player_2': self.player_2,
            'score_1': self.score_1,
            'score_2': self.score_2,
            'score_total': self.score_total,
            'timestamp': self.timestamp,
            'tournament': self.tournament,
            'sport_type': self.sport_type,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
