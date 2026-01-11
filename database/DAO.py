from database.DB_connect import DBConnect
from model.state import State
from model.sighting import Sighting


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def get_all_states():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from state s"""
            cursor.execute(query)

            for row in cursor:
                result.append(
                    State(row["id"],
                          row["Name"],
                          row["Capital"],
                          row["Lat"],
                          row["Lng"],
                          row["Area"],
                          row["Population"],
                          row["Neighbors"]))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_sightings():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from sighting s 
                    order by `datetime` asc """
            cursor.execute(query)

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result


    @staticmethod
    def getAllAnni():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT DISTINCT YEAR(s.datetime)
                        FROM sighting s 
                        ORDER BY YEAR(s.datetime) DESC"""
            cursor.execute(query)

            for row in cursor:
                result.append(row['YEAR(s.datetime)'])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllForme():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT DISTINCT s.shape 
                        FROM sighting s 
                        WHERE s.shape != "unknown" and s.shape != ""
                        ORDER BY s.shape """
            cursor.execute(query)

            for row in cursor:
                result.append(row['shape'])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllNodi(forma, anno):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT *
                    FROM sighting s 
                    WHERE s.shape = %s AND YEAR(s.`datetime`) = %s"""
            cursor.execute(query,(forma,anno))

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllArchi(forma, anno, idMapAvvisamenti):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT DISTINCT s1.id as id1, s2.id as id2
                        FROM sighting s1, sighting s2
                        WHERE s1.shape = %s AND YEAR(s1.`datetime`) = %s AND s2.shape = %s AND YEAR(s2.`datetime`) = %s
                        AND s1.datetime < s2.datetime AND s1.state = s2.state """
            cursor.execute(query, (forma, anno, forma, anno))

            for row in cursor:
                result.append(
                    (idMapAvvisamenti[row["id1"]], idMapAvvisamenti[row["id2"]]  )
                )
            cursor.close()
            cnx.close()
        return result