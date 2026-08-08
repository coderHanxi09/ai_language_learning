from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    Index,
    DateTime,
    UniqueConstraint
)

from sqlalchemy.orm import relationship

from datetime import datetime

from .db import Base



# =====================================================
# Dictionary Entry
# =====================================================

class DictionaryEntryDB(Base):

    __tablename__ = "dictionary_entries"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    # original word
    # e.g. Entscheidung
    word = Column(
        String(128),
        nullable=False,
        index=True
    )


    # base form
    # e.g. Entscheidung
    lemma = Column(
        String(128),
        nullable=False,
        index=True
    )


    # language of word
    # en / de
    language = Column(
        String(16),
        nullable=False,
        default="en"
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


    translations = relationship(
        "DictionaryTranslationDB",
        back_populates="dictionary",
        cascade="all, delete-orphan"
    )


    __table_args__ = (

        UniqueConstraint(
            "lemma",
            "language",
            name="unique_dictionary_language_lemma"
        ),

    )





# =====================================================
# Dictionary Translation
# =====================================================

class DictionaryTranslationDB(Base):

    __tablename__ = "dictionary_translations"


    id = Column(
        Integer,
        primary_key=True
    )


    dictionary_id = Column(
        Integer,
        ForeignKey(
            "dictionary_entries.id"
        ),
        nullable=False
    )


    # target language
    # en / zh
    language = Column(
        String(16),
        nullable=False
    )


    translation = Column(
        Text,
        nullable=False
    )


    examples = Column(
        Text
    )


    dictionary = relationship(
        "DictionaryEntryDB",
        back_populates="translations"
    )


    __table_args__ = (

        UniqueConstraint(
            "dictionary_id",
            "language",
            name="unique_dictionary_translation_language"
        ),

    )






# =====================================================
# Reading
# =====================================================

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


    # language of article
    # en / de
    source_language = Column(
        String(16),
        nullable=False,
        default="en"
    )


    # translation language
    # zh / en
    translation_language = Column(
        String(16),
        nullable=False,
        default="zh"
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


    vocabulary_items = relationship(
        "VocabularyDB",
        back_populates="reading"
    )






# =====================================================
# Reading Sentence
# =====================================================

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
        Text
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






# =====================================================
# Reading Word
# =====================================================

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
        String(128),
        nullable=False,
        index=True
    )


    pos = Column(
        String(32)
    )


    position = Column(
        Integer,
        nullable=False
    )


    sentence = relationship(
        "ReadingSentenceDB",
        back_populates="words"
    )






# =====================================================
# Workspace
# =====================================================

class WorkspaceDB(Base):

    __tablename__ = "workspaces"


    id = Column(
        Integer,
        primary_key=True
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







# =====================================================
# User Vocabulary
# =====================================================

class VocabularyDB(Base):

    __tablename__ = "vocabulary"


    id = Column(
        Integer,
        primary_key=True
    )


    # displayed word
    # Entscheidung
    word = Column(
        String(128),
        nullable=False
    )


    # learning key
    # Entscheidung
    lemma = Column(
        String(128),
        nullable=False,
        index=True
    )


    source_language = Column(
        String(16),
        nullable=False,
        default="en"
    )


    dictionary_id = Column(
        Integer,
        ForeignKey(
            "dictionary_entries.id"
        ),
        nullable=True
    )


    cefr = Column(
        String(8)
    )


    source = Column(
        String(32),
        default="reading"
    )


    reading_id = Column(
        Integer,
        ForeignKey(
            "readings.id"
        ),
        nullable=True
    )


    workspace_id = Column(
        Integer,
        ForeignKey(
            "workspaces.id"
        ),
        nullable=True
    )


    reading = relationship(
        "ReadingDB",
        back_populates="vocabulary_items"
    )


    workspace = relationship(
        "WorkspaceDB",
        back_populates="vocabulary_items"
    )


    dictionary = relationship(
        "DictionaryEntryDB"
    )


    translations = relationship(
        "VocabularyTranslationDB",
        back_populates="vocabulary",
        cascade="all, delete-orphan"
    )


    flashcards = relationship(
        "FlashcardDB",
        back_populates="vocabulary",
        cascade="all, delete-orphan"
    )


    __table_args__ = (

        UniqueConstraint(
            "lemma",
            "source_language",
            name="unique_vocab_language_lemma"
        ),

    )






# =====================================================
# Vocabulary Translation
# =====================================================

class VocabularyTranslationDB(Base):

    __tablename__ = "vocabulary_translations"


    id = Column(
        Integer,
        primary_key=True
    )


    vocabulary_id = Column(
        Integer,
        ForeignKey(
            "vocabulary.id"
        ),
        nullable=False
    )


    language = Column(
        String(16),
        nullable=False
    )


    translation = Column(
        Text,
        nullable=False
    )


    vocabulary = relationship(
        "VocabularyDB",
        back_populates="translations"
    )


    __table_args__ = (

        UniqueConstraint(
            "vocabulary_id",
            "language",
            name="unique_vocab_translation_language"
        ),

    )






# =====================================================
# Flashcards
# =====================================================

class FlashcardDB(Base):

    __tablename__ = "flashcards"


    id = Column(
        Integer,
        primary_key=True
    )


    # front:
    # German word
    front = Column(
        Text
    )


    # back:
    # English translation
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
        )
    )


    vocabulary = relationship(
        "VocabularyDB",
        back_populates="flashcards"
    )







# =====================================================
# User
# =====================================================

class UserDB(Base):

    __tablename__ = "users"


    id = Column(
        Integer,
        primary_key=True
    )


    username = Column(
        String(128),
        unique=True,
        nullable=False
    )


    hashed_password = Column(
        String(256),
        nullable=False
    )