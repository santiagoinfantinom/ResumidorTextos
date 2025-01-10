from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from fastapi.middleware.cors import CORSMiddleware

# Download ALL required NLTK data
try:
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('maxent_ne_chunker')
    nltk.download('words')
except:
    pass

# Verificar que el tokenizador está disponible
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

app = FastAPI()

# Configurar CORS - Mover esto ANTES de definir las rutas
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica los dominios exactos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Para almacenar los resúmenes
summaries = []

class Summary(BaseModel):
    text: str
    summary: str

class TextInput(BaseModel):
    text: str

def generate_summary(text: str, num_sentences: int = 3):
    # Tokenize the text into sentences
    sentences = sent_tokenize(text)
    
    # Tokenize words, remove stopwords and punctuation
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text.lower())
    words = [word for word in words if word.isalnum() and word not in stop_words]
    
    # Calculate word frequency
    freq_dist = FreqDist(words)
    
    # Score sentences based on word frequency
    sentence_scores = {}
    for sentence in sentences:
        for word in word_tokenize(sentence.lower()):
            if word in freq_dist:
                if sentence not in sentence_scores:
                    sentence_scores[sentence] = freq_dist[word]
                else:
                    sentence_scores[sentence] += freq_dist[word]
    
    # Get top sentences
    summary_sentences = sorted(sentence_scores.items(), 
                             key=lambda x: x[1], 
                             reverse=True)[:num_sentences]
    
    # Reconstruct the summary in the original order
    summary = ' '.join(sent for sent, score in sorted(summary_sentences, 
                      key=lambda x: sentences.index(x[0])))
    
    return summary

@app.post("/summary")
async def create_summary(input_text: TextInput):  # Hay que hacer que la función sea async
    summary = generate_summary(input_text.text)
    return Summary(text=input_text.text, summary=summary)

@app.get("/summaries")
def get_summaries():
    return {"message": "Endpoint working"}
