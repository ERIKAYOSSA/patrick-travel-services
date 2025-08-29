from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import SessionLocal
from app.models.offer import Offer
from app.schemas.offer import OfferCreate
from app.services.auth import get_current_user
from app.models.user import User

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/admin/offers")
def create_offer(offer: OfferCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Accès réservé à l'administration")

    new_offer = Offer(**offer.dict())
    db.add(new_offer)
    db.commit()
    db.refresh(new_offer)
    return {"message": "Offre ajoutée", "id": new_offer.id}

@router.get("/admin/offers")
def list_offers(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Accès réservé à l'administration")

    return db.query(Offer).all()

@router.patch("/admin/offers/{offer_id}")
def update_offer(offer_id: int, update_data: OfferCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Accès réservé à l'administration")

    offer = db.query(Offer).filter(Offer.id == offer_id).first()
    if not offer:
        raise HTTPException(status_code=404, detail="Offre introuvable")

    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(offer, key, value)

    db.commit()
    db.refresh(offer)
    return {"message": "Offre mise à jour", "id": offer.id}

@router.delete("/admin/offers/{offer_id}")
def delete_offer(offer_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Accès réservé à l'administration")

    offer = db.query(Offer).filter(Offer.id == offer_id).first()
    if not offer:
        raise HTTPException(status_code=404, detail="Offre introuvable")

    db.delete(offer)
    db.commit()
    return {"message": "Offre supprimée"}

@router.get("/admin/offers/filter")
def filter_offers_by_type(type: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Accès réservé à l'administration")

    offers = db.query(Offer).filter(Offer.type == type).all()
    return offers