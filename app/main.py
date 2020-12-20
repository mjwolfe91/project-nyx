from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle

app = FastAPI(title="Customer Recommendations", version="1.0.0", root_path="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Let's load in the model we used before
with open("./recommendations.pkl", "rb") as f:
    clf = pickle.load(f)

class Recommendation(BaseModel):
    """
    todo: get this info from Stroud!!
    """

@app.route("/predict")
def predict(sample: Recommendation):
    """
    Unpack the responses, predict on the input variables, and return the prediction.
    """
    #responses = [
        #todo get info from Stroud
    #]

    return clf.predict(inputs)[0]

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
