from prettytable import PrettyTable
from colorama import Fore
from os import system
import click
from utils import read_json, write_json

table = PrettyTable()
table.field_names = ["ID", "First Name", "Last Name"]


db_path = r"src/data/users.json"

# system("clear")

@click.group()
def cli():
    pass

@cli.command()
def users():
    users = read_json(db_path)
    users_list = [*map(lambda user: [user["id"], user["fname"], user["lname"]], users)]
    if len(users) > 0:
        table.add_rows(users_list)
        print(table)
    else:
        print(Fore.GREEN + "Database empy!")
    
    
@cli.command()
@click.option("--fname", required=True, help="First name of the user", type=str)
@click.option("--lname", required=True, help="Last name of the user", type=str)
@click.pass_context
def new(ctx, fname, lname):
    if not fname or not lname:
        ctx.fail("The name and the last name are required!")
    else:
        users = read_json(db_path)
        
        if len(users) > 0:
            id_users = [*map(lambda usr: usr["id"], users)]
            id = max(id_users) + 1
        else:
            id = 1
        
        if "-" in fname or "-" in lname:
            fname = fname.replace("-", " ")
            lname = lname.replace("-", " ")
        
        # Add user to users list
        users.append({"id": id ,"fname":fname, "lname":lname})
        write_json(db_path, users)
    
        print(Fore.CYAN + f"Created successfully with id {id}!")

@cli.command()
@click.argument("id", type=int, required=True)
def user(id):
    users = read_json(db_path)
    user = [*filter(lambda user: user["id"] == id, users)]
    
    if len(user) < 1:
        print(Fore.RED + "User not found!")
        return
    
    users_list = [*map(lambda user: [user["id"], user["fname"], user["lname"]], user)]
    table.add_rows(users_list)
    print(table)
    
@cli.command()
@click.argument("id", type=int, required=True)
def delete(id):
    users = read_json(db_path)
    user = [*filter(lambda user: user["id"] == id, users)]
    
    if len(user) < 1:
        print(Fore.RED + "User not found!")
        return
    
    users.remove(*user)
    write_json(db_path, users)
    print(Fore.CYAN + f"User with id {id} was successfully delete!")


@cli.command()
@click.argument("id", type=int, required=True)
@click.option("--fname", help="First name of the user", type=str)
@click.option("--lname", help="Last name of the user", type=str)
def update(id, fname, lname):
    users = read_json(db_path)
    user = [*filter(lambda user: user["id"] == id, users)]       
    
    if len(user) < 1:
        print(Fore.RED + "User not found!")
        return
    
    if fname is not None:
        if "-" in fname:
            fname = fname.replace("-", " ")
        user[0]["fname"] = fname
     
    if lname is not None:   
        if "-" in lname:
            lname = lname.replace("-", " ")
        user[0]["lname"] = lname
            
    write_json(db_path, users)
    print(Fore.CYAN + f"User with id {id} was successfully updated!")
    
    
if __name__ == "__main__":
    cli()

