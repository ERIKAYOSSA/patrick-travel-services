from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import SessionLocal
from app.models.partner import Partner
from app.schemas.partner import PartnerCreate
from app.services.auth import get_current_user
from app.models.user import User
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/admin/partners")
def create_partner(partner: PartnerCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        return {"error": "Accès réservé à l'administration"}

    new_partner = Partner(**partner.dict())
    db.add(new_partner)
    db.commit()
    db.refresh(new_partner)
    return {"message": "Partenaire ajouté", "id": new_partner.id}

@router.get("/admin/partners")
def list_partners(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        return {"error": "Accès réservé à l'administration"}

    partners = db.query(Partner).all()
    return partners

@router.patch("/admin/partners/{partner_id}")
def update_partner(partner_id: int, update_data: PartnerCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Accès réservé à l'administration")

    partner = db.query(Partner).filter(Partner.id == partner_id).first()
    if not partner:
        raise HTTPException(status_code=404, detail="Partenaire introuvable")

    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(partner, key, value)

    db.commit()
    db.refresh(partner)
    return {"message": "Partenaire mis à jour", "id": partner.id}

@router.delete("/admin/partners/{partner_id}")
def delete_partner(partner_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Accès réservé à l'administration")

    partner = db.query(Partner).filter(Partner.id == partner_id).first()
    if not partner:
        raise HTTPException(status_code=404, detail="Partenaire introuvable")

    db.delete(partner)
    db.commit()
    return {"message": "Partenaire supprimé"}