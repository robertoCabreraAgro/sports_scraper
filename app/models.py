from datetime import datetime
from app import db

class PartidoFutbol(db.Model):
    """Modelo para almacenar información de partidos de fútbol."""
    id = db.Column(db.Integer, primary_key=True)
    competencia = db.Column(db.String(100), nullable=False)
    equipo_local = db.Column(db.String(100), nullable=False)
    equipo_visitante = db.Column(db.String(100), nullable=False)
    goles_local = db.Column(db.Integer, nullable=False)
    goles_visitante = db.Column(db.Integer, nullable=False)
    hora = db.Column(db.String(10), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    url_detalles = db.Column(db.String(255), nullable=True)  # URL para más detalles del partido

    def __repr__(self):
        return f'<Partido {self.competencia} {self.equipo_local} vs {self.equipo_visitante}>'
    
    def to_dict(self):
        """Convierte el modelo a un diccionario para ser devuelto como JSON."""
        return {
            'id': self.id,
            'competencia': self.competencia,
            'equipo_local': self.equipo_local,
            'equipo_visitante': self.equipo_visitante,
            'goles_local': self.goles_local,
            'goles_visitante': self.goles_visitante,
            'hora': self.hora,
            'fecha': self.fecha.strftime('%Y-%m-%d %H:%M:%S'),
            'url_detalles': self.url_detalles
        }

class PartidoTenis(db.Model):
    """Modelo para almacenar información de partidos de tenis."""
    id = db.Column(db.Integer, primary_key=True)
    torneo = db.Column(db.String(100), nullable=False)
    jugador1 = db.Column(db.String(100), nullable=False)
    jugador2 = db.Column(db.String(100), nullable=False)
    sets_jugador1 = db.Column(db.Integer, nullable=False)
    sets_jugador2 = db.Column(db.Integer, nullable=False)
    hora = db.Column(db.String(10), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    url_detalles = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f'<Partido {self.torneo} {self.jugador1} vs {self.jugador2}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'torneo': self.torneo,
            'jugador1': self.jugador1,
            'jugador2': self.jugador2,
            'sets_jugador1': self.sets_jugador1,
            'sets_jugador2': self.sets_jugador2,
            'hora': self.hora,
            'fecha': self.fecha.strftime('%Y-%m-%d %H:%M:%S'),
            'url_detalles': self.url_detalles
        }

class PartidoBaloncesto(db.Model):
    """Modelo para almacenar información de partidos de baloncesto."""
    id = db.Column(db.Integer, primary_key=True)
    liga = db.Column(db.String(100), nullable=False)
    equipo_local = db.Column(db.String(100), nullable=False)
    equipo_visitante = db.Column(db.String(100), nullable=False)
    puntos_local = db.Column(db.Integer, nullable=False)
    puntos_visitante = db.Column(db.Integer, nullable=False)
    hora = db.Column(db.String(10), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    url_detalles = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f'<Partido {self.liga} {self.equipo_local} vs {self.equipo_visitante}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'liga': self.liga,
            'equipo_local': self.equipo_local,
            'equipo_visitante': self.equipo_visitante,
            'puntos_local': self.puntos_local,
            'puntos_visitante': self.puntos_visitante,
            'hora': self.hora,
            'fecha': self.fecha.strftime('%Y-%m-%d %H:%M:%S'),
            'url_detalles': self.url_detalles
        }