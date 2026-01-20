from database.DB_connect import DBConnect
from model.artist import Artist

class DAO:

    @staticmethod
    def get_all_artists():

        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT *
                FROM artist a
                """
        cursor.execute(query)
        for row in cursor:
            artist = Artist(id=row['id'], name=row['name'])
            result.append(artist)
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_artisti_album(num_album):
        try:
            conn = DBConnect.get_connection()
            result = []
            cursor = conn.cursor(dictionary=True)
            query = """
                    SELECT a.id as id_artista
                    FROM artist a, album ab
                    WHERE a.id = ab.artist_id
                    GROUP BY a.id
                    HAVING COUNT(*) >= %s
                    
                    """
            cursor.execute(query, [num_album],)
            for row in cursor:
                result.append(row["id_artista"])

            cursor.close()
            conn.close()
            return result
        except Exception as e:
            print("Errore di esecuzione query")

    @staticmethod
    def get_edges():

        try:
            conn = DBConnect.get_connection()
            result = []
            cursor = conn.cursor(dictionary=True)
            query = """
                    SELECT a1.artist_id as id_a1, a2.artist_id as id_a2, COUNT(DISTINCT (t1.genre_id)) as w
                    FROM album a1, album a2, track t1, track t2
                    WHERE a1.artist_id < a2.artist_id
                        AND t1.id != t2.id
                        AND a1.id = t1.album_id
                        AND a2.id = t2.album_id
                        AND t1.genre_id = t2.genre_id
                    GROUP BY a1.artist_id, a2.artist_id
    
                    """
            cursor.execute(query)
            for row in cursor:
                result.append([row["id_a1"], row["id_a2"], row["w"]])

            cursor.close()
            conn.close()
            return result
        except Exception as e:
            print("Errore di esecuzione query")
