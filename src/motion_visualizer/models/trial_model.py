from sqlalchemy import Column, DateTime, Float, Integer, String

from ..database.db_client import Base


class Trial(Base):
    __tablename__ = 'trials'

    id = Column(Integer, primary_key=True)
    scenario_name = Column(String(100))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    duration = Column(Float)
    distance = Column(Float)
    status = Column(String(20))

    def to_dict(self):
        return {
            "id": self.id,
            "scenario": self.scenario_name,
            "start": self.start_time.isoformat() if self.start_time else None,
            "end": self.end_time.isoformat() if self.end_time else None,
            "duration": self.duration,
            "distance": self.distance,
            "status": self.status
        }