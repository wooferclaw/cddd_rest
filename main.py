from fastapi import FastAPI
from pydantic import BaseModel
from utils import get_model, smiles_to_embedding, seq_to_emb, emb_to_seq


app = FastAPI(title="Predicting Continuous and Data-Driven" \
                    "Descriptors (CDDD) from SMILE IDs")


class SMILE(BaseModel):
    """Represent input as a list of batches containing smiles"""
    batches: list


class CDDD(BaseModel):
    cddd: list


@app.on_event("startup")
def load_model():
    """ Load model on server startup"""
    global model
    model = get_model()


@app.get("/")
def home():
    """Just provide a simple link to API docs"""
    return "Continuous and Data-Driven Descriptors (CDDD) API.  "\
        "For documenation head over to http://localhost:80/docs"


@app.post("/predict")
def predict(smile: SMILE):
    """Given a list containing """
    batches = smile.batches
    batches = [item for sublist in batches for item in sublist]

    preds = smiles_to_embedding(batches, model)
    preds = preds.to_json()  # serialize pandas DF to send over REST

    return {"Prediction": preds}


@app.post("/smiles_to_cddd")
def seq2emb(smiles: SMILE):
    print(smiles)
    preds = seq_to_emb(smiles, model)
    preds = preds.to_json()  # serialize pandas DF to send over REST

    return {"1": preds}


@app.post("/cddd_to_smiles")
def emb2seq(cddd: CDDD):
    """Given a list containing """
    print(cddd)
    smiles = emb_to_seq(cddd.cddd, model)
    print(smiles)

    return smiles
