"""
Database Connection Utilities
Centralized database connection and query execution
"""

from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
from db_config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD


class DatabaseConnection:
    """Singleton database connection manager"""
    
    _engine = None
    
    @classmethod
    def get_engine(cls):
        """Get or create database engine"""
        if cls._engine is None:
            connection_string = f"postgresql://{DB_USER}:{quote_plus(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
            cls._engine = create_engine(connection_string)
        return cls._engine
    
    @classmethod
    def execute_query(cls, query):
        """Execute a SELECT query and return results"""
        engine = cls.get_engine()
        try:
            with engine.connect() as conn:
                result = conn.execute(text(query))
                return result.fetchall()
        except Exception as e:
            raise Exception(f"Query execution failed: {str(e)}")
    
    @classmethod
    def execute_scalar(cls, query):
        """Execute a query and return single value"""
        engine = cls.get_engine()
        try:
            with engine.connect() as conn:
                result = conn.execute(text(query))
                return result.scalar()
        except Exception as e:
            raise Exception(f"Query execution failed: {str(e)}")
    
    @classmethod
    def execute_procedure(cls, procedure_call):
        """Execute a stored procedure"""
        engine = cls.get_engine()
        try:
            with engine.connect() as conn:
                conn.execute(text(procedure_call))
                conn.commit()
                return True
        except Exception as e:
            raise Exception(f"Procedure execution failed: {str(e)}")
    
    @classmethod
    def test_connection(cls):
        """Test database connection"""
        engine = cls.get_engine()
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except Exception as e:
            return False
