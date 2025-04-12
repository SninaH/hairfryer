from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class GameSession(Base):
    __tablename__ = "game_sessions"

    id: Mapped[str] = mapped_column(primary_key=True)  # UUID
    status: Mapped[str] = mapped_column(nullable=False)  # e.g. 'waiting-coordinates', 'processing', 'done', 'error'
    error_message: Mapped[str] = mapped_column(nullable=True)  # Error message if status is 'error'
    youtube_url: Mapped[str] = mapped_column(nullable=False)
    preview_image_url: Mapped[str] = mapped_column(nullable=True)

    coordinates_throw_order: Mapped[list[int]] = mapped_column(JSONB, nullable=True)
    coordinates_pins_fallen_in_throw: Mapped[list[int]] = mapped_column(JSONB, nullable=True)
    coordinates_pins_fallen_on_lane: Mapped[list[int]] = mapped_column(JSONB, nullable=True)
    coordinates_pin_1: Mapped[list[int]] = mapped_column(JSONB, nullable=True)
    coordinates_pin_2: Mapped[list[int]] = mapped_column(JSONB, nullable=True)
    coordinates_pin_3: Mapped[list[int]] = mapped_column(JSONB, nullable=True)
    coordinates_pin_4: Mapped[list[int]] = mapped_column(JSONB, nullable=True)
    coordinates_pin_5: Mapped[list[int]] = mapped_column(JSONB, nullable=True)
    coordinates_pin_6: Mapped[list[int]] = mapped_column(JSONB, nullable=True)
    coordinates_pin_7: Mapped[list[int]] = mapped_column(JSONB, nullable=True)
    coordinates_pin_8: Mapped[list[int]] = mapped_column(JSONB, nullable=True)
    coordinates_pin_9: Mapped[list[int]] = mapped_column(JSONB, nullable=True)

    total_throws: Mapped[int] = mapped_column(nullable=True)  # Total number of throws in the session
    total_pins_fallen: Mapped[int] = mapped_column(nullable=True)  # Total number of pins fallen in the session
    throws: Mapped[list[dict]] = mapped_column(JSONB, nullable=True)  # List of dictionaries containing throw results

    def __repr__(self):
        return f"<Session(id={self.id})>"
