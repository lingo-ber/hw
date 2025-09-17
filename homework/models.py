from sqlalchemy import Column, Integer, String, Text

from .database import Base


class Recipe(Base):
    """
    Модель SQLAlchemy для таблицы 'Recipe', представляющая данные рецепта.

    Attributes:
        id (int): идентификатор рецепта, первичный ключ
        dish_name (str): название блюда (ограничение длины - 100 символов)
        cooking_time (int): время приготовления в минутах
        ingredients (str): список ингредиентов
        description (str): описание рецепта (без ограничения длины)
        views (int): количество просмотров
    """

    __tablename__ = "Recipe"
    id = Column(Integer, primary_key=True)
    dish_name = Column(String(100), index=True, nullable=False, unique=True)
    cooking_time = Column(Integer, index=True)
    ingredients = Column(String)
    description = Column(Text)
    views = Column(Integer, index=True, default=0)
