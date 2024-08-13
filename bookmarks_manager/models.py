# author: Gustavo Sopena
# date started: 2024-08-11 at 1730

from sqlalchemy import Column, DateTime, Integer, String, Boolean
from bookmarks_manager.db import Base

class URL_Text(Base):
    __tablename__ = 'bm_url_text'
    url_id = Column(Integer, primary_key=True, autoincrement=True)
    date_added = Column(DateTime, unique=True)
    # name = Column(String(100), nullable=False)
    url_text = Column(String(256), unique=True, nullable=False)
    has_image = Column(Boolean, unique=False, nullable=False)
    
    def __repr__(self) -> str:
        ''''''
    
        return f'''
        URL_Text:
        - created at: {self.date_added}
        - url: {self.url_text}
        - has image: {self.has_image}'''

    @staticmethod
    def contains_image_extension(url: str | None) -> bool:
        '''This function checks if the string argument contains one of the valid extensions.'''
    
        valid_extensions: list[str] = ['.png', '.jpg', '.jpeg']
        
        for ext in valid_extensions:
            if ext in url:
                return True
        
        return False
