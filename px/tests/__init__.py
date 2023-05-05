import os

if os.environ.get("CI") == "true" and os.environ.get("CODECOV_TOKEN"):
    import subprocess

    subprocess.run(["codecov"], check=True)
