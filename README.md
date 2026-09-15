# RELEX: recipe learning through examples

The system behind RELEX: a writing tool that retrieves, from 180,000 recipes, a worked example matched to the learner's own draft, and the fine-tuned models, database and study materials around it. This is the original repository; the lab's copy at epfl-ml4ed/relex is a fork of it.

**Enhancing Procedural Writing Through Personalized Example Retrieval: A Case Study on Cooking Recipes**  
Paola Mejia-Domenzain, Jibril Frej, Seyed Parsa Neshaei, Luca Mouchel, Tanya Nazaretsky, Thiemo Wambsganss, Antoine Bosselut, Tanja Käser. *International Journal of Artificial Intelligence in Education*, 2024.  
[DOI](https://doi.org/10.1007/s40593-024-00408-z) · [Abstract and BibTeX](https://paola-md.github.io/papers/enhancing-procedural-writing-through-personalized-example-retrieval-a-ca.html)

Live system: https://go.epfl.ch/relex  
RELEXSet (the recipe dataset): https://drive.google.com/drive/folders/1ZUOvPxJaGpUjU5QsRlxqVq_pGipgTMlN  
Lab fork: https://github.com/epfl-ml4ed/relex  

## What is here

```
backend/recipe/     FastAPI service: retrieval, suggestions, login
frontend/           web client (started from the chat-app template)
model/              masked-language-model pretraining and regression fine-tuning (mlm.py, finetuning_regression.py, model_pipeline.py)
database/           Postgres set-up and formatting of the example recipes
transfer/           scripts that update rule colours and rules
docs/
  recipe-suggestions-rules.pdf   the suggestion rules
  questions_constructs.pdf  study-questions-complete.pdf  user-interviews.pdf
  effect-sizes.pdf  training-results-details.json  split-verification.ipynb   results added Feb 2024
readme.pdf          the original README as a PDF
```

## How to run

Python 3.8. Backend:

```bash
cd backend && pip install -r requirements.txt
uvicorn recipe.app:app --reload
```

The backend expects a Postgres database prepared with `database/start_database.py` and `database/format_examples.py`. Frontend:

```bash
cd frontend && npm install && npm start
```

The models in `model/` train with their own `requirements.txt` and `Dockerfile`. The login in `backend/recipe/login.py` is placeholder boilerplate from the FastAPI tutorial, not an authentication system: replace it before any deployment.

## Data

The recipe examples (RELEXSet) are shared separately on the Drive folder above; `database/data/` is empty here. Study data from the participants is not included.

## Cite

```bibtex
@article{mejiadomenzain2024enhancing,
  title      = {{Enhancing Procedural Writing Through Personalized Example Retrieval: A Case Study on Cooking Recipes}},
  author     = {Paola Mejia-Domenzain and Jibril Frej and Seyed Parsa Neshaei and Luca Mouchel and Tanya Nazaretsky and Thiemo Wambsganß and Antoine Bosselut and Tanja Käser},
  year       = {2024},
  journal    = {International Journal of Artificial Intelligence in Education},
  publisher  = {Springer Science+Business Media},
  doi        = {10.1007/s40593-024-00405-1},
  url        = {https://paola-md.github.io/papers/enhancing-procedural-writing-through-personalized-example-retrieval-a-ca.html}
}
```


## Licence and status

No licence file.

Not maintained: kept as the record of the paper.
