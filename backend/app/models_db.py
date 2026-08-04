from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    Index,
    DateTime
)

from sqlalchemy.orm import relationship

from datetime import datetime

from .db import Base



# =========================
# Dictionary
# =========================

class DictionaryEntryDB(Base):

    __tablename__ = "dictionary_entries"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    word = Column(
        String(128),
        unique=True,
        index=True,
        nullable=False
    )


    lemma = Column(
        String(128)
    )


    definition = Column(
        Text
    )


    pos = Column(
        String(32)
    )


    cefr = Column(
        String(8)
    )


    ipa = Column(
        String(64)
    )


    examples = Column(
        Text
    )





# =========================
# Reading
# =========================

class ReadingDB(Base):

    __tablename__ = "readings"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    title = Column(
        String(255)
    )


    topic = Column(
        String(255)
    )


    difficulty = Column(
        String(32),
        default="B2"
    )


    content = Column(
        Text
    )


    vocabulary = Column(
        Text
    )


    status = Column(
        String(32),
        default="pending"
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


    sentences = relationship(
        "ReadingSentenceDB",
        back_populates="reading",
        cascade="all, delete-orphan"
    )





# =========================
# Reading Sentences
# =========================

class ReadingSentenceDB(Base):

    __tablename__ = "reading_sentences"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    reading_id = Column(
        Integer,
        ForeignKey(
            "readings.id"
        ),
        nullable=False
    )


    sentence_order = Column(
        Integer,
        nullable=False
    )


    original = Column(
        Text,
        nullable=False
    )


    translation = Column(
        Text,
        nullable=True
    )


    reading = relationship(
        "ReadingDB",
        back_populates="sentences"
    )


    words = relationship(
        "ReadingWordDB",
        back_populates="sentence",
        cascade="all, delete-orphan"
    )





# =========================
# Reading Words
# =========================

class ReadingWordDB(Base):

    __tablename__ = "reading_words"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    sentence_id = Column(
        Integer,
        ForeignKey(
            "reading_sentences.id"
        ),
        nullable=False
    )


    word = Column(
        String(128),
        nullable=False
    )


    lemma = Column(
        String(128)
    )


    position = Column(
        Integer,
        nullable=False
    )


    sentence = relationship(
        "ReadingSentenceDB",
        back_populates="words"
    )





# =========================
# Workspace
# =========================

class WorkspaceDB(Base):

    __tablename__ = "workspaces"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    title = Column(
        String(255),
        nullable=False
    )


    description = Column(
        Text
    )


    vocabulary_items = relationship(
        "VocabularyDB",
        back_populates="workspace"
    )





# =========================
# Vocabulary
# =========================

class VocabularyDB(Base):

    __tablename__ = "vocabulary"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    word = Column(
        String(128),
        nullable=False,
        index=True
    )


    lemma = Column(
        String(128)
    )


    definition = Column(
        Text
    )


    cefr = Column(
        String(8)
    )


    frequency = Column(
        Integer,
        default=0
    )


    workspace_id = Column(
        Integer,
        ForeignKey(
            "workspaces.id"
        ),
        nullable=True
    )


    workspace = relationship(
        "WorkspaceDB",
        back_populates="vocabulary_items"
    )


    __table_args__ = (
        Index(
            "ix_vocabulary_word_workspace",
            "word",
            "workspace_id"
        ),
    )





# =========================
# Flashcards
# =========================

class FlashcardDB(Base):

    __tablename__ = "flashcards"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    front = Column(
        Text
    )


    back = Column(
        Text
    )


    status = Column(
        String(32),
        default="learning"
    )


    vocabulary_id = Column(
        Integer,
        ForeignKey(
            "vocabulary.id"
        ),
        nullable=True
    )


    vocabulary = relationship(
        "VocabularyDB"
    )





# =========================
# User
# =========================

class UserDB(Base):

    __tablename__ = "users"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    username = Column(
        String(128),
        unique=True,
        index=True,
        nullable=False
    )


    hashed_password = Column(
        String(256),
        nullable=False
    )