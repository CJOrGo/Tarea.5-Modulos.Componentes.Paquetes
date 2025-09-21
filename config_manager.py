# config_manager.py
import json
import os
from typing import Any, Dict


class ConfigManager:
    """Gestor de configuración para aplicaciones."""

    def __init__(self, archivo_config: str = "config.json"):
        self.archivo_config = archivo_config
        self.config: Dict[str, Any] = {}

        # Si el archivo existe, cargarlo
        if os.path.exists(self.archivo_config):
            try:
                with open(self.archivo_config, "r", encoding="utf-8") as f:
                    self.config = json.load(f)
            except json.JSONDecodeError:
                self.config = {}

    def get(self, clave: str, default: Any = None) -> Any:
        """Obtiene valor de configuración (soporta claves anidadas: 'db.host')."""
        partes = clave.split(".")
        valor = self.config
        for parte in partes:
            if isinstance(valor, dict) and parte in valor:
                valor = valor[parte]
            else:
                return default
        return valor

    def set(self, clave: str, valor: Any) -> None:
        """Establece valor de configuración (soporta claves anidadas: 'db.host')."""
        partes = clave.split(".")
        d = self.config
        for parte in partes[:-1]:
            if parte not in d or not isinstance(d[parte], dict):
                d[parte] = {}
            d = d[parte]
        d[partes[-1]] = valor

    def save(self) -> None:
        """Guarda configuración en archivo JSON."""
        with open(self.archivo_config, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=4, ensure_ascii=False)

    def load_from_env(self, mapeo: Dict[str, str]) -> None:
        """
        Carga configuración desde variables de entorno.
        Ejemplo:
            mapeo = {
                "DATABASE_URL": "db.url",
                "DATABASE_HOST": "db.host"
            }
        """
        for var_env, clave_conf in mapeo.items():
            valor = os.getenv(var_env)
            if valor is not None:
                self.set(clave_conf, valor)

"""
config = ConfigManager()
config.set("db.host", "localhost")
config.set("db.port", 5432)
config.save()
config.load_from_env({"DATABASE_URL": "db.url"})
"""