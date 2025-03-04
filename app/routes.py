from flask import Flask, request, jsonify
from .utils import main
import mysql.connector
from decouple import config
BASE_DATOS_ACTUALIZADA = {}

def register_routes(app):

    app.config["MYSQL_HOST"] = config("MYSQL_HOST")
    app.config["MYSQL_USER"] = config("MYSQL_USER")
    app.config["MYSQL_PASSWORD"] = config("MYSQL_PASSWORD")
    app.config["MYSQL_DB"] = config("MYSQL_DB")
    app.config["MYSQL_PORT"] = config("MYSQL_PORT", cast=int)

    def actualizar_base_datos():
        global BASE_DATOS_ACTUALIZADA
        try:
            app.mysql = mysql.connector.connect(
                host=app.config["MYSQL_HOST"],
                user=app.config["MYSQL_USER"],
                password=app.config["MYSQL_PASSWORD"],
                database=app.config["MYSQL_DB"],
                port=app.config["MYSQL_PORT"]
            )
            base_datos = {}

            with app.mysql.cursor(dictionary=True) as cur:
                cur.execute("SHOW TABLES")
                tablas = [list(tabla.values())[0] for tabla in cur.fetchall()]

                for nombre_tabla in tablas:
                    cur.execute(f"DESCRIBE {nombre_tabla}")
                    columnas_info = cur.fetchall()

                    cur.execute(
                        f"""
                        SELECT COLUMN_NAME 
                        FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE 
                        WHERE TABLE_NAME = '{nombre_tabla}' AND CONSTRAINT_NAME = 'PRIMARY'
                    """
                    )
                    primary_keys = [pk["COLUMN_NAME"] for pk in cur.fetchall()]

                    cur.execute(
                        f"""
                        SELECT COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME 
                        FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE 
                        WHERE TABLE_NAME = '{nombre_tabla}' AND REFERENCED_TABLE_NAME IS NOT NULL
                    """
                    )
                    foreign_keys = {
                        fk["COLUMN_NAME"]: f"{fk['REFERENCED_TABLE_NAME']}.{fk['REFERENCED_COLUMN_NAME']}"
                        for fk in cur.fetchall()
                    }

                    estructura_tabla = {
                        "columnas": {},
                        "llave_primaria": primary_keys[0] if primary_keys else None,
                        "llaves_foraneas": foreign_keys if foreign_keys else None,
                    }

                    for columna in columnas_info:
                        nombre_columna = columna["Field"]
                        tipo_dato = columna["Type"]
                        restricciones = []

                        if "auto_increment" in columna["Extra"]:
                            restricciones.append("AUTOINCREMENTAL")
                        if columna["Null"] == "NO":
                            restricciones.append("NO NULO")
                        if nombre_columna in primary_keys:
                            restricciones.append("CLAVE PRIMARIA")
                        if nombre_columna in foreign_keys:
                            restricciones.append("CLAVE FORANEA")

                        estructura_tabla["columnas"][nombre_columna] = {
                            "tipo": tipo_dato,
                            "restricciones": restricciones,
                        }

                    base_datos[nombre_tabla] = estructura_tabla

            BASE_DATOS_ACTUALIZADA = base_datos
            print("Base de datos actualizada")
        except Exception as e:
            print(f"Error al actualizar la base de datos: {str(e)}")
        finally:
            if app.mysql.is_connected():
                app.mysql.close()

    actualizar_base_datos()

    @app.route("/", methods=["POST"])
    def consultar():
        try:
            data = request.get_json()
            consulta = data.get("consulta", "").strip()

            if not consulta:
                return jsonify({"error": "No se recibió ninguna consulta"}), 400

            resultado = procesar_consulta(consulta)

            if resultado.startswith("Error"):
                return jsonify({"resultado": resultado, "datos_tabla": "error"}), 400

            datos_tabla = obtener_datos_tabla(resultado)

            actualizar_base_datos()  # Actualizamos la base de datos después de la consulta

            return jsonify({"resultado": resultado, "datos_tabla": datos_tabla})

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def procesar_consulta(consulta):
        try:
            analizar_query = main.analizar_query(consulta)

            return f"{analizar_query}"
        except Exception as e:
            return str(e)

    def obtener_datos_tabla(resultado):
        datos_tabla = {}
        try:
            # Conectar a la base de datos usando mysql.connector
            conn = mysql.connector.connect(
                host=app.config["MYSQL_HOST"],
                user=app.config["MYSQL_USER"],
                password=app.config["MYSQL_PASSWORD"],
                database=app.config["MYSQL_DB"],
                port=app.config["MYSQL_PORT"],
            )

            # Usar el cursor con dictionary=True para obtener resultados en formato de diccionario
            with conn.cursor(dictionary=True) as cur:
                if not resultado.strip().upper().startswith("SELECT"):
                    try:
                        cur.execute(resultado)
                        conn.commit()                                         
                        cur.execute("SHOW TABLES")
                        tablas = [list(tabla.values())[0] for tabla in cur.fetchall()]

                        for nombre_tabla in tablas:
                            cur.execute(f"SELECT * FROM {nombre_tabla}")
                            filas = cur.fetchall()

                            if filas:
                                columnas = [{"name": col} for col in filas[0].keys()]
                                datos_tabla[nombre_tabla] = {
                                    "columns": columnas,
                                    "data": filas,
                                }

                    except Exception as e:
                        print(f"Error ejecutando la consulta: {str(e)}")
                        conn.rollback() 
                        return str(e)

                else:
                    # Manejo de consultas SELECT
                    palabras = resultado.split()
                    if "FROM" in palabras:
                        indice_from = palabras.index("FROM")
                        nombre_tabla = palabras[indice_from + 1]

                        cur.execute(resultado)
                        filas = cur.fetchall()

                        if filas:
                            columnas = [{"name": col} for col in filas[0].keys()]
                            datos_tabla[nombre_tabla] = {
                                "columns": columnas,
                                "data": filas,
                            }

        except Exception as e:
            print(f"Error general: {str(e)}")
            return str(e)
        finally:
            if conn.is_connected():
                conn.close()

        return datos_tabla if datos_tabla else "error"