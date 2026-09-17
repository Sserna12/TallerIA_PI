import os
from django.core.management.base import BaseCommand
from movie.models import Movie


class Command(BaseCommand):
    help = "Update movie images from local folder"

    def handle(self, *args, **kwargs):
        images_folder = "media/movie/images/"
        movies = Movie.objects.all()

        self.stdout.write(f"Found {movies.count()} movies")

        updated_count = 0

        for movie in movies:
            safe_title = movie.title.replace("/", "_").replace("\\", "_")
            image_filename = f"m_{safe_title}.png"
            image_path = os.path.join(images_folder, image_filename)

            if os.path.exists(image_path):
                movie.image = f"movie/images/{image_filename}"
                movie.save()

                updated_count += 1

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Updated image: {movie.title}"
                    )
                )
            else:
                self.stderr.write(
                    f"Image not found: {movie.title}"
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Finished updating {updated_count} movie images."
            )
        )
        