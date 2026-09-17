import os
import base64

from openai import OpenAI
from django.core.management.base import BaseCommand
from movie.models import Movie
from dotenv import load_dotenv


class Command(BaseCommand):
    help = "Generate and update the first movie image using OpenAI API"

    def handle(self, *args, **kwargs):

        load_dotenv("../openAI.env")

        client = OpenAI(
            api_key=os.environ.get("openai_apikey")
        )

        images_folder = "media/movie/images/"
        os.makedirs(images_folder, exist_ok=True)

        movies = Movie.objects.all()

        self.stdout.write(f"Found {movies.count()} movies")

        for movie in movies:

            self.stdout.write(f"Processing: {movie.title}")

            try:
                prompt = (
                    f"Create a cinematic movie poster for a film titled "
                    f"'{movie.title}'. "
                    f"Use this description as context: {movie.description}. "
                    f"No text or letters in the image."
                )

                response = client.images.generate(
                    model="gpt-image-2",
                    prompt=prompt,
                    size="1024x1024",
                    n=1,
                )

                image_base64 = response.data[0].b64_json

                image_bytes = base64.b64decode(image_base64)

                safe_title = movie.title.replace("/", "_").replace("\\", "_")

                image_filename = f"m_{safe_title}.png"
                image_path_full = os.path.join(
                    images_folder,
                    image_filename
                )

                with open(image_path_full, "wb") as file:
                    file.write(image_bytes)

                movie.image = f"movie/images/{image_filename}"
                movie.save()

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Saved and updated image for: {movie.title}"
                    )
                )

            except Exception as e:
                self.stderr.write(
                    f"Failed for {movie.title}: {str(e)}"
                )

            break