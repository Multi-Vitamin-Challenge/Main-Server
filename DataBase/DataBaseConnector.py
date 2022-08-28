import mysql.connector
import DataBaseTools


config = DataBaseTools.read_config()




def run_without_ouput(sql):
    mydb = mysql.connector.connect(
    host=config["Database_host"],
    user=config["Database_Username"],
    password=config["Database_Password"],
    database=config["Database_name"]
    )
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    mydb.commit()
    return mycursor.rowcount


def run_with_output(sql):
    mydb = mysql.connector.connect(
    host=config["Database_host"],
    user=config["Database_Username"],
    password=config["Database_Password"],
    database=config["Database_name"]
    )    
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return myresult


if __name__ == "__main__":
    run_without_ouput("INSERT INTO `multivitamin`.`users` (`idusers`, `username`, `password`, `name`) VALUES ('1', '2', '3', '4');")
    run_without_ouput("INSERT INTO `multivitamin`.`users` (`idusers`, `username`, `password`, `name`) VALUES ('5', '6', '7', '8');")
    run_without_ouput("INSERT INTO `multivitamin`.`users` (`idusers`, `username`, `password`, `name`) VALUES ('10', '11', '12', '13');")
    run_without_ouput("""DELETE FROM `multivitamin`.`users` WHERE (`idusers` = '1');""")
    run_without_ouput("DELETE FROM `multivitamin`.`users` WHERE (`idusers` = '5');")
    run_without_ouput("""DELETE FROM `multivitamin`.`users` WHERE (`idusers` = '10');""")

    print(run_with_output("Select * from multivitamin.users"))