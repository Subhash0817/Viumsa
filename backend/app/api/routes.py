from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.services.ai_service import AIService
from app.services.conversation_service import ConversationService
from app.services.gemini_provider import GeminiProvider


router = APIRouter()

ai_service = AIService(GeminiProvider())


class ChatRequest(BaseModel):
    message: str
    conversation_id: int | None = None


class ChatResponse(BaseModel):
    response: str
    conversation_id: int


class ConversationResponse(BaseModel):
    id: int
    title: str


class MessageResponse(BaseModel):
    id: int
    role: str
    content: str

@router.get("/")
def root():
    return {
        "application": "Viumsa",
        "version": "0.1.0",
        "status": "running"
    }


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    message = request.message.strip()

    if not message:
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty"
        )

    # If there is no conversation yet, create one.
    if request.conversation_id is None:
        title = message[:60]

        conversation = ConversationService.create_conversation(
            db=db,
            title=title
        )

    else:
        conversation = ConversationService.get_conversation(
            db=db,
            conversation_id=request.conversation_id
        )

        if conversation is None:
            raise HTTPException(
                status_code=404,
                detail="Conversation not found"
            )

    # Save the user's message.
    ConversationService.add_message(
        db=db,
        conversation_id=conversation.id,
        role="user",
        content=message
    )

    # Ask Viumsa.
    # Load previous conversation history.
    saved_messages = ConversationService.get_messages(
    db=db,
    conversation_id=conversation.id
    )

    history = [
    {
        "role": saved_message.role,
        "content": saved_message.content
    }
    for saved_message in saved_messages[:-1]
    ]

    # Ask Viumsa with conversation context.
    response = await ai_service.chat(
    message=message,
    history=history
    )

    # Save Viumsa's response.
    ConversationService.add_message(
        db=db,
        conversation_id=conversation.id,
        role="assistant",
        content=response
    )

    return ChatResponse(
        response=response,
        conversation_id=conversation.id
    )
@router.get(
    "/conversations",
    response_model=list[ConversationResponse]
)
def get_conversations(
    db: Session = Depends(get_db)
):
    conversations = ConversationService.get_conversations(db)

    return [
        ConversationResponse(
            id=conversation.id,
            title=conversation.title
        )
        for conversation in conversations
    ]
@router.get(
    "/conversations/{conversation_id}/messages",
    response_model=list[MessageResponse]
)
def get_conversation_messages(
    conversation_id: int,
    db: Session = Depends(get_db)
):
    conversation = ConversationService.get_conversation(
        db=db,
        conversation_id=conversation_id
    )

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )

    messages = ConversationService.get_messages(
        db=db,
        conversation_id=conversation_id
    )

    return [
        MessageResponse(
            id=message.id,
            role=message.role,
            content=message.content
        )
        for message in messages
    ]