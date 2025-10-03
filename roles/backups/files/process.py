
import ast
import csv
import json
import os
import sys
from datetime import datetime

from scripts.query import PostgresQuery
from scripts.structure import PostgresStructure
from scripts.utils import (
    inventory_insert,
    system_insert,
    version_insert,
    model_insert,
    type_insert,
    hostname_insert,
    backups_insert,
)

url = os.path.realpath(os.path.dirname(__file__))
parent_dir = os.path.abspath(os.path.join(url, "backups"))


class ProccessDnfUpdate:
    def __init__(self):
        pass

    def main(self):
        PostgresStructure().create_tables()
        archivos_txt = [
            archivo
            for archivo in os.listdir(f"{parent_dir}")
            if archivo.endswith(".json")
        ]
        current_date = datetime.now().date()
        sincronice_update = set()
        for item in archivos_txt:

            file_path = f"{parent_dir}/{item.replace('.json', '.txt')}"

            try:
                with open(file_path, "r", encoding="utf-8") as record:
                    data_file = record.read()
            except FileNotFoundError:
                data_file = None

            with open(f"{parent_dir}/{item}", "r", encoding="utf-8") as record:
                data = json.load(record)  # Carga y parsea JSON a dict de Python
                sincronice_hardening = set()
                # Inventory******************************************************************
                inventory_id = PostgresQuery().absent_insertar_or_update(
                    query=inventory_insert,
                    params=(data.get("ip", "N/A"), True),
                    quer_name="inventory_insert",
                )
                # system******************************************************************
                system_id = PostgresQuery().absent_insertar_or_update(
                    query=system_insert,
                    params=(data.get("ansible_net_system", "N/A"), True),
                    quer_name="system_insert",
                )
                # version******************************************************************
                version_id = PostgresQuery().absent_insertar_or_update(
                    query=version_insert,
                    params=(data.get("ansible_net_version", "N/A"), True),
                    quer_name="version_insert",
                )
                # model******************************************************************
                stacked_models = data.get("ansible_net_stacked_models")
                if stacked_models and len(stacked_models) > 0:
                    model_name = stacked_models[0]
                else:
                    model_name = "N/A"

                model_id = PostgresQuery().absent_insertar_or_update(
                    query=model_insert,
                    params=(model_name, True),
                    quer_name="model_insert",
                )
                # type******************************************************************
                type_id = PostgresQuery().absent_insertar_or_update(
                    query=type_insert,
                    params=(data.get("ansible_net_iostype", "N/A"), True),
                    quer_name="type_insert",
                )
                # hostname******************************************************************
                hostname_id = PostgresQuery().absent_insertar_or_update(
                    query=hostname_insert,
                    params=(data.get("ansible_net_hostname", "N/A"), True),
                    quer_name="hostname_insert",
                )
                sincronice_update.add(
                    (
                        system_id.get("id",None) if system_id else None,
                        inventory_id.get("id",None) if inventory_id else None,
                        version_id.get("id",None) if version_id else None,
                        model_id.get("id",None) if model_id else None,
                        type_id.get("id",None) if type_id else None,
                        hostname_id.get("id",None) if hostname_id else None,
                        current_date,
                        True,
                        data_file
                    )
                )
        # FIN FOR #################################################################################
        if sincronice_update:
            PostgresQuery().absent_insertar_or_update_masive(
                query=backups_insert,
                params=sincronice_update,
                quer_name="backups_insert",
            )


if __name__ == "__main__":
    proceso = ProccessDnfUpdate()  # Crear instancia
    try:
        proceso.main()  # Llamar a main
    except Exception as e:
        print(f"Error durante la ejecución: {e}", file=sys.stderr)
        sys.exit(1)  # Sale con código 1 en caso de error

    sys.exit(0)  # Sale con código 0 si todo fue OK
