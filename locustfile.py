# locustfile.py

from pathlib import Path

from locust import HttpUser, constant_throughput, task


CSV_FILE_PATH = Path("sample.csv")


class CsvUploadUser(HttpUser):
    """
    Fixed-rate CSV upload user.

    Sends requests at a controlled rate instead of random user pacing.
    """

    # Target: ~100 requests/sec across workers
    wait_time = constant_throughput(5)

    @task
    def upload_csv(self) -> None:
        """
        Upload one CSV file to /uploads/csv
        """
        with open(CSV_FILE_PATH, "rb") as f:
            files = {
                "file": (CSV_FILE_PATH.name, f, "text/csv"),
            }

            self.client.post(
                "/uploads/csv",
                files=files,
                name="/uploads/csv",
            )


# from pathlib import Path

# from locust import HttpUser, between, task


# CSV_FILE_PATH = Path("indian_data.csv")


# class CsvUploadUser(HttpUser):
#     """
#     Simulates users uploading CSV files to the FastAPI ingestion API.
#     """

#     wait_time = between(0.1, 0.3)

#     @task
#     def upload_csv(self) -> None:
#         """
#         Upload one CSV file to /uploads/csv
#         """
#         with open(CSV_FILE_PATH, "rb") as f:
#             files = {
#                 "file": (CSV_FILE_PATH.name, f, "text/csv"),
#             }

#             self.client.post(
#                 "/uploads/csv",
#                 files=files,
#                 name="/uploads/csv",
#             )
