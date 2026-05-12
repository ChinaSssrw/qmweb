from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import LoginResponse, TokenResponse, UserCreate, UserLogin, UserResponse
from app.utils.wechat import create_access_token, get_current_user, wx_login

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/wx-login", response_model=LoginResponse)
async def wx_login_endpoint(body: UserLogin, db: Session = Depends(get_db)):
    openid = await wx_login(body.code)

    user = db.query(User).filter(User.wx_openid == openid).first()
    if not user:
        user = User(
            wx_openid=openid,
            nickname=f"用户{openid[-6:]}",
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    token = create_access_token({"sub": user.id})
    return LoginResponse(
        access_token=token,
        user=UserResponse.model_validate(user),
    )


@router.post("/register", response_model=UserResponse)
async def register(
    body: UserCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.phone:
        raise HTTPException(status_code=400, detail="Phone already bound")

    if body.referrer_id:
        referrer = db.query(User).filter(User.id == body.referrer_id).first()
        if not referrer:
            raise HTTPException(status_code=404, detail="Referrer not found")

    current_user.phone = body.phone
    current_user.referrer_id = body.referrer_id
    db.commit()
    db.refresh(current_user)

    return current_user
