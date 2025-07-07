from fastapi import APIRouter

router = APIRouter(prefix="/api/v2/payments")

@router.get("/")
def search(use_case):
    use_case.execute()
    

@router.get("/{payment_id}")
def get_by_id(use_case):
    use_case.execute()


@router.post("/{payment_id}/verify")
def verificate(use_case):
    use_case.execute()


@router.post("/{payment_id}/status")
def update_status(use_case):
    use_case.execute()



