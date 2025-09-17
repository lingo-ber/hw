from sqlalchemy.orm import Mapped, mapped_column

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
    id: Mapped[int] = mapped_column(primary_key=True)
    dish_name: Mapped[str] = mapped_column(String(100), index=True, nullable=False, unique=True)
    cooking_time: Mapped[int] = mapped_column(index=True)
    ingredients: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column(Text)
    views: Mapped[int] = mapped_column(index=True, default=0)
