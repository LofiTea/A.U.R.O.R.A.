import nextcord
import mysql.connector
import json

from nextcord.ext import commands
from nextcord import Interaction
from mysql.connector import Error

class Storage(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Don't forget to turn on MAMP
    @nextcord.slash_command(name="store_info", description="Stores some data from a user to a database")
    async def store_info(self, interaction: Interaction, message: str):
        guild = interaction.guild.id

        try:
            connection = mysql.connector.connect(
                host='localhost', 
                port='8889',
                database='A.U.R.O.R.A.', 
                user='root', 
                password='root'
            )
            
            mySQL_Create_Table_Query = f"""CREATE TABLE IF NOT EXISTS DB_{guild} (
                                            Id int(11) NOT NULL AUTO_INCREMENT,
                                            User varchar(250) NOT NULL,
                                            Message varchar(5000) NOT NULL,
                                            PRIMARY KEY (Id))"""
            
            cursor = connection.cursor()
            cursor.execute(mySQL_Create_Table_Query)
            print(f"Guild ({guild}) Table created successfully or already exists")

        except mysql.connector.Error as error:
            print(f"Failed to create table in MySQL: {error}")

        finally:
            if connection.is_connected():
                try:
                    table = f"DB_{guild}"
                    mySQL_Insert_Row_Query = f"INSERT INTO {table} (User, Message) VALUES (%s, %s)"
                    mySQL_Insert_Row_Values = (str(interaction.user), message)

                    cursor.execute(mySQL_Insert_Row_Query, mySQL_Insert_Row_Values)
                    connection.commit()

                    await interaction.response.send_message("The message is stored!")

                except mysql.connector.Error as error:
                    print(f"Failed to insert record into MySQL table: {error}")
                finally:
                    cursor.close()
                    connection.close()

    @nextcord.slash_command(name="retrieve_info", description="Retrieve some information that a user stored in a database")
    async def retrieve_info(self, interaction: Interaction):
        guild = interaction.guild.id
        table = f"DB_{guild}"
        
        try:
            connection = mysql.connector.connect(
                host='localhost', 
                port='8889',
                database='A.U.R.O.R.A.', 
                user='root', 
                password='root'
            )
            
            cursor = connection.cursor()

            mySQL_Select_Query = f"SELECT * FROM {table} WHERE User = %s"
            cursor.execute(mySQL_Select_Query, (str(interaction.user),))

            records = cursor.fetchall()

            received_data = []

            for row in records:
                received_data.append({"Id": str(row[0]), "Message": str(row[2])})

            await interaction.response.send_message("All Stored Data: \n\n" + json.dumps(received_data, indent=1))
        
        except mysql.connector.Error as error:
            print(f"Failed to get record from MySQL table: {error}")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

def setup(client):
    client.add_cog(Storage(client))