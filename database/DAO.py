from database.DB_connect import DBConnect
from model.driver import Driver


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getYears():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary = True)

        query = """select distinct s.year
                    from seasons s """

        cursor.execute(query)
        res = []
        for row in cursor:
            res.append(row["year"])

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getDrivers(year):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        query = """select distinct d.*
                    from races r, results r2, drivers d
                    where r.raceId = r2.raceId
                    and d.driverId = r2.driverId
                    and r2.`position` is not null
                    and year(r.date) = %s """

        cursor.execute(query,(year,))
        res = []
        for row in cursor:
            res.append(Driver(**row))

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getEdges(year):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        query = """ select r1.driverId as id1, r2.driverId as id2, count(*) as cnt
                        from results r1, results r2, races r
                        where r1.position < r2.position
                        and r1.raceId = r2.raceId
                        and r.raceId = r1.raceId
                        and r1.position is not null
                        and r2.position is not null
                        and year(r.date) = %s
                        group by id1, id2"""

        cursor.execute(query, (year,))
        res = []
        for row in cursor:
            res.append((row["id1"], row["id2"], row["cnt"]))

        cursor.close()
        cnx.close()
        return res