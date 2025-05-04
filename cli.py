import typer
from backup import mysql, postgres, mongodb, sqlite

app = typer.Typer(help="Database Backup CLI Utility")

@app.command()
def backup(db_type: str = typer.Option(..., help="Database type: mysql, postgres, mongodb, sqlite")):
    if db_type == "mysql":
        mysql.backup()
    elif db_type == "postgres":
        postgres.backup()
    elif db_type == "mongodb":
        mongodb.backup()
    elif db_type == "sqlite":
        sqlite.backup()
    else:
        typer.echo("Unsupported database type.")

@app.command()
def restore(file: str = typer.Argument(...), db_type: str = typer.Option(...)):
    typer.echo(f"Restoring {db_type} database from {file}...")
    # Add call to restore module here

if __name__ == "__main__":
    app()
