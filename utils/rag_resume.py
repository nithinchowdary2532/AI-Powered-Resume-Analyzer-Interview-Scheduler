from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

# Load a pre-trained model (do this once)
model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_text(text):
    """Embed a single text string using the sentence transformer model."""
    return model.encode([text])[0]

def build_job_db(job_dict):
    """
    Build a FAISS vector index for job roles.
    Returns: (faiss_index, job_keys, job_embeddings)
    """
    job_texts = []
    job_keys = []
    for role, data in job_dict.items():
        desc = f"{role}: {' '.join(data['mandatory_skills'])} {' '.join(data['skills'])}"
        job_texts.append(desc)
        job_keys.append(role)
    job_embeddings = np.vstack([embed_text(t) for t in job_texts])
    index = faiss.IndexFlatL2(job_embeddings.shape[1])
    index.add(job_embeddings)
    return index, job_keys, job_embeddings

def match_resume_to_jobs(resume_text, index, job_keys, job_embeddings, top_k=1):
    """
    Given resume text, return the top_k most similar job roles and their similarity scores.
    """
    resume_emb = embed_text(resume_text)
    D, I = index.search(np.array([resume_emb]), top_k)
    matches = []
    for idx, dist in zip(I[0], D[0]):
        score = 1 / (1 + dist)  # Convert L2 distance to a similarity score (higher is better)
        matches.append((job_keys[idx], score))
    return matches