from invoke import task


@task
def start(c):
    """
    Start the Uvicorn server.
    """
    c.run("uvicorn store.main:app --reload")


@task
def precommit_install(c):
    """
    Install pre-commit.
    """
    c.run("poetry run pre-commit install")
