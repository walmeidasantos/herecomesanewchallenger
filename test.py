import uvicorn
from app2.api.server import app
from app2.models.pessoa import pessoaCreate, pessoaResponse

uvicorn.run(app, host="0.0.0.0", port=9999)
