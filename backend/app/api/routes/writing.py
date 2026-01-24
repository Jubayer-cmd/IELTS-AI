"""
IELTS Writing evaluation routes.

Following FastAPI full-stack template pattern.
"""
from fastapi import APIRouter, HTTPException, status

from app.api.deps import SessionDep, CurrentUser
from app.models import (
    Essay,
    EssayCreate,
    EssayPublic,
    EssaysPublic,
    EvaluationRequest,
    EvaluationResponse,
    BandScore,
    Message,
)

router = APIRouter()


@router.get("/", response_model=Message)
def writing_service_info() -> Message:
    """Writing service health check."""
    return Message(message="IELTS Writing Evaluation Service")


@router.post("/evaluate", response_model=EvaluationResponse)
def evaluate_essay(
    session: SessionDep,
    current_user: CurrentUser,
    essay_in: EvaluationRequest
) -> EvaluationResponse:
    """
    Evaluate an IELTS essay and return scores.

    Requires authentication. Consumes 1 credit.
    """
    # Check user credits
    if current_user.credits <= 0:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="Insufficient credits. Please purchase more."
        )

    # Validate word count
    word_count = len(essay_in.text.split())
    if word_count < 50:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Essay too short. Minimum 50 words required."
        )
    if word_count > 500:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Essay exceeds 500 word limit."
        )

    # TODO: Integrate LLM evaluation (LangGraph workflow)
    # For now, return mock scores
    band_scores = BandScore(
        task_achievement=7.0,
        coherence=7.5,
        lexical=7.0,
        grammar=7.0
    )

    overall_score = (
        band_scores.task_achievement +
        band_scores.coherence +
        band_scores.lexical +
        band_scores.grammar
    ) / 4

    # Save essay to database
    essay = Essay(
        text=essay_in.text,
        task_type=essay_in.task_type,
        word_limit=essay_in.word_limit,
        user_id=current_user.id,
        word_count=word_count,
        overall_score=overall_score,
        task_achievement=band_scores.task_achievement,
        coherence=band_scores.coherence,
        lexical=band_scores.lexical,
        grammar=band_scores.grammar,
        feedback="Great essay! Keep practicing.",  # TODO: LLM feedback
    )
    session.add(essay)

    # Deduct credit
    current_user.credits -= 1
    session.add(current_user)

    session.commit()
    session.refresh(essay)

    return EvaluationResponse(
        word_count=word_count,
        overall_score=round(overall_score, 1),
        band_scores=band_scores,
        feedback=essay.feedback,
    )


@router.get("/essays", response_model=EssaysPublic)
def get_my_essays(
    session: SessionDep,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 20
) -> EssaysPublic:
    """
    Get current user's essays with pagination.
    """
    from sqlmodel import select

    statement = (
        select(Essay)
        .where(Essay.user_id == current_user.id)
        .order_by(Essay.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    essays = session.exec(statement).all()

    count_statement = select(Essay).where(Essay.user_id == current_user.id)
    count = len(session.exec(count_statement).all())

    return EssaysPublic(data=essays, count=count)


@router.get("/essays/{essay_id}", response_model=EssayPublic)
def get_essay(
    session: SessionDep,
    current_user: CurrentUser,
    essay_id: int
) -> Essay:
    """
    Get a specific essay by ID.
    """
    essay = session.get(Essay, essay_id)

    if not essay:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Essay not found"
        )

    if essay.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    return essay


@router.delete("/essays/{essay_id}", response_model=Message)
def delete_essay(
    session: SessionDep,
    current_user: CurrentUser,
    essay_id: int
) -> Message:
    """
    Delete an essay.
    """
    essay = session.get(Essay, essay_id)

    if not essay:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Essay not found"
        )

    if essay.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    session.delete(essay)
    session.commit()
    return Message(message="Essay deleted successfully")
