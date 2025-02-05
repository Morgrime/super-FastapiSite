from fastapi import APIRouter

router = APIRouter()

@router.get('/')
async def index():
    return 'Index page'

@router.get('/test')
async def test_page():
    return 'Test page' 