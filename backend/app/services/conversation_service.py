from sqlalchemy.orm import Session

from app.models.conversation import Conversation
from app.models.message import Message


class ConversationService:

    @staticmethod
    def create_conversation(
        db: Session,
        title: str = "New conversation"
    ) -> Conversation:

        conversation = Conversation(title=title)

        db.add(conversation)
        db.commit()
        db.refresh(conversation)

        return conversation


    @staticmethod
    def get_conversations(
        db: Session
    ) -> list[Conversation]:

        return (
            db.query(Conversation)
            .order_by(Conversation.updated_at.desc())
            .all()
        )


    @staticmethod
    def get_conversation(
        db: Session,
        conversation_id: int
    ) -> Conversation | None:

        return (
            db.query(Conversation)
            .filter(Conversation.id == conversation_id)
            .first()
        )
    @staticmethod
    def delete_conversation(
    db: Session,
    conversation_id: int
    ) -> bool:

        conversation = (
        db.query(Conversation)
        .filter(Conversation.id == conversation_id)
        .first()
    )

        if conversation is None:
            return False

        db.delete(conversation)
        db.commit()

        return True
    @staticmethod
    def rename_conversation(
        db: Session,
        conversation_id: int,
        title: str
    ) -> Conversation | None:

        conversation = (
            db.query(Conversation)
            .filter(Conversation.id == conversation_id)
            .first()
    )

        if conversation is None:
            return None

        conversation.title = title

        db.commit()
        db.refresh(conversation)

        return conversation
    @staticmethod
    def get_messages(
        db: Session,
        conversation_id: int
    ) -> list[Message]:

        return (
            db.query(Message)
            .filter(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
            .all()
        )


    @staticmethod
    def add_message(
        db: Session,
        conversation_id: int,
        role: str,
        content: str
    ) -> Message:

        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content
        )

        db.add(message)

        conversation = (
            db.query(Conversation)
            .filter(Conversation.id == conversation_id)
            .first()
        )

        if conversation:
            from datetime import datetime
            conversation.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(message)

        return message