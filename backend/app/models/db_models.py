from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class User(Base):
    """User model for storing user preferences and authentication information"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    preferences = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationships
    conversations = relationship('Conversation', back_populates='user')
    provider_configs = relationship('ProviderConfig', back_populates='user')
    
    def __repr__(self):
        return f'<User {self.username}>'


class ProviderConfig(Base):
    """Model for storing AI provider configuration information"""
    __tablename__ = 'provider_configs'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    provider_id = Column(String(64), nullable=False)  # e.g., 'openai', 'anthropic'
    api_key = Column(String(256), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Relationships
    user = relationship('User', back_populates='provider_configs')
    
    def __repr__(self):
        return f'<ProviderConfig {self.provider_id}>'


class Conversation(Base):
    """Model for storing conversation information"""
    __tablename__ = 'conversations'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(256), default='New Conversation')
    provider_id = Column(String(64))  # The provider used for this conversation
    model_id = Column(String(128))    # The model used for this conversation
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Relationships
    user = relationship('User', back_populates='conversations')
    messages = relationship('Message', back_populates='conversation', order_by='Message.created_at')
    
    def __repr__(self):
        return f'<Conversation {self.title}>'


class Message(Base):
    """Model for storing message content"""
    __tablename__ = 'messages'
    
    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, ForeignKey('conversations.id'), nullable=False)
    role = Column(String(32), nullable=False)  # 'user', 'assistant', 'system'
    content = Column(Text, nullable=False)
    model = Column(String(128))  # The model that generated this message (for assistant messages)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Metadata about the message
    metadata = Column(JSON, default={})  # For storing things like tokens used, etc.
    
    # Relationships
    conversation = relationship('Conversation', back_populates='messages')
    attachments = relationship('Attachment', back_populates='message')
    
    def __repr__(self):
        return f'<Message {self.id}: {self.role}>'


class Attachment(Base):
    """Model for storing message attachments (images, documents, audio)"""
    __tablename__ = 'attachments'
    
    id = Column(Integer, primary_key=True)
    message_id = Column(Integer, ForeignKey('messages.id'), nullable=False)
    file_type = Column(String(32), nullable=False)  # 'image', 'document', 'audio'
    file_path = Column(String(256), nullable=False)  # Path to the stored file
    file_name = Column(String(256), nullable=False)  # Original filename
    content_type = Column(String(128))  # MIME type
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationships
    message = relationship('Message', back_populates='attachments')
    
    def __repr__(self):
        return f'<Attachment {self.file_name}>'
