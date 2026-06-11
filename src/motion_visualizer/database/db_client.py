import os
from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Trial(Base):
    __tablename__ = 'trials'
    
    id = Column(Integer, primary_key=True)
    scenario_name = Column(String(100), default="default")
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=True)
    duration = Column(Float, nullable=True)  # секунды
    distance = Column(Float, nullable=True)   # пиксели / метры
    status = Column(String(20), default="RUNNING")  # RUNNING, FINISHED, RESET

class DatabaseClient:
    def __init__(self, db_path="motion_visualizer.db"):
        self.engine = create_engine(f'sqlite:///{db_path}', echo=False)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
    
    def create_trial(self, scenario_name="default"):
        """Создать новую запись испытания, вернуть ID"""
        session = self.Session()
        trial = Trial(
            scenario_name=scenario_name,
            start_time=datetime.now(),
            status="RUNNING"
        )
        session.add(trial)
        session.commit()
        trial_id = trial.id
        session.close()
        return trial_id
    
    def finish_trial(self, trial_id, duration, distance):
        """Завершить испытание: записать время окончания, дистанцию, статус"""
        session = self.Session()
        trial = session.query(Trial).filter_by(id=trial_id).first()
        if trial:
            trial.end_time = datetime.now()
            trial.duration = duration
            trial.distance = distance
            trial.status = "FINISHED"
            session.commit()
        session.close()
    
    def reset_trial(self, trial_id):
        """Отметить испытание как сброшенное (опционально)"""
        session = self.Session()
        trial = session.query(Trial).filter_by(id=trial_id).first()
        if trial:
            trial.status = "RESET"
            session.commit()
        session.close()
    
    def get_all_trials(self):
        """Получить все испытания для статистики"""
        session = self.Session()
        trials = session.query(Trial).all()
        session.close()
        return trials