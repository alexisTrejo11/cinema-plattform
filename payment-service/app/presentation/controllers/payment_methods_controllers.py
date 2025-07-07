from fastapi import APIRouter

router = APIRouter(prefix="/api/v2/payment-methods")

@router.get("/")
def lsit(use_case):
    use_case.execute()
    

@router.post("/{payment_id}")
def create(use_case):
    use_case.execute()


@router.delete("/{payment_id}")
def delete(use_case):
    use_case.execute()

