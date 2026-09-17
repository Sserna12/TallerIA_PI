import os
import numpy as np
from django.core.management.base import BaseCommand
from movie.models import Movie
from openai import OpenAI
from dotenv import load_dotenv


class Command(BaseCommand):
    help = "Compare two movies and a prompt using OpenAI embeddings"

    def handle(self, *args, **kwargs):

        # Load OpenAI API key
        load_dotenv("../openAI.env")

        client = OpenAI(
            api_key=os.environ.get("openai_apikey")
        )

        # Movies selected for comparison
        movie1 = Movie.objects.get(title="La captura")
        movie2 = Movie.objects.get(title="Castillo medieval")

        # Function to generate embeddings
        def get_embedding(text):
            response = client.embeddings.create(
                input=[text],
                model="text-embedding-3-small"
            )

            return np.array(
                response.data[0].embedding,
                dtype=np.float32
            )

        # Cosine similarity
        def cosine_similarity(a, b):
            return np.dot(a, b) / (
                np.linalg.norm(a) * np.linalg.norm(b)
            )

        # Generate embeddings for both movies
        emb1 = get_embedding(movie1.description)
        emb2 = get_embedding(movie2.description)

        # Similarity between movies
        similarity = cosine_similarity(emb1, emb2)

        self.stdout.write(
            f"Movie 1: {movie1.title}"
        )

        self.stdout.write(
            f"Movie 2: {movie2.title}"
        )

        self.stdout.write(
            f"Similarity between movies: {similarity:.4f}"
        )

        # Prompt comparison
        prompt = "película de aventura y fantasía"

        self.stdout.write(
            f"Prompt: {prompt}"
        )

        prompt_emb = get_embedding(prompt)

        sim_prompt_movie1 = cosine_similarity(
            prompt_emb,
            emb1
        )

        sim_prompt_movie2 = cosine_similarity(
            prompt_emb,
            emb2
        )

        self.stdout.write(
            f"Prompt similarity vs '{movie1.title}': "
            f"{sim_prompt_movie1:.4f}"
        )

        self.stdout.write(
            f"Prompt similarity vs '{movie2.title}': "
            f"{sim_prompt_movie2:.4f}"
        )