from fastapi import APIRouter

router = APIRouter(prefix="/api/v2/transaction")

@router.get("/")
def list(use_case):
    use_case.execute()
    

@router.get("/{user_id}")
def get_by_user_id(use_case):
    use_case.execute()


@router.post("/{transaction_id}")
def get_by_id(use_case):
    use_case.execute()


