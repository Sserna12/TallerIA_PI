import os
import random
import numpy as np

from django.core.management.base import BaseCommand
from movie.models import Movie
from openai import OpenAI
from dotenv import load_dotenv


class Command(BaseCommand):
    help = "Generate and store embeddings for all movies"

    def handle(self, *args, **kwargs):

        load_dotenv("../openAI.env")

        client = OpenAI(
            api_key=os.environ.get("openai_apikey")
        )

        movies = Movie.objects.all()

        self.stdout.write(
            f"Found {movies.count()} movies in the database"
        )

        def get_embedding(text):
            response = client.embeddings.create(
                input=[text],
                model="text-embedding-3-small"
            )

            return np.array(
                response.data[0].embedding,
                dtype=np.float32
            )

        for movie in movies:
            try:
                emb = get_embedding(movie.description)

                movie.emb = emb.tobytes()
                movie.save()

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Embedding stored for: {movie.title}"
                    )
                )

            except Exception as e:
                self.stderr.write(
                    f"Failed to generate embedding for {movie.title}: {e}"
                )

        self.stdout.write(
            self.style.SUCCESS(
                "Finished generating embeddings for all movies"
            )
        )

        # Select a random movie to display its embedding
        random_movie = random.choice(list(movies))

        embedding = np.frombuffer(
            random_movie.emb,
            dtype=np.float32
        )

        self.stdout.write("")
        self.stdout.write(
            f"Random movie: {random_movie.title}"
        )

        self.stdout.write(
            f"Embedding dimensions: {len(embedding)}"
        )

        self.stdout.write(
            f"Embedding: {embedding[:20]}"
        )
        