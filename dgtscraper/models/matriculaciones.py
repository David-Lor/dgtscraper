import datetime
import enum
from typing import Optional

import pydantic
import class_doc

from .common import CampoMetadata


class ClaseMatriculaEnum(str, enum.Enum):
    # TODO cuando se exporta el modelo a json, se usan los valores (numeros). Mejorar que pydantic parsee los numeros al enum, pero exporte los nombres u otros strings.
    Ordinaria = "0"
    Turistica = "1"
    Remolque = "2"
    Diplomatica = "3"
    Reservada = "4"
    VehiculoEspecial = "5"
    Ciclomotor = "6"
    TransporteTemporal = "7"
    Historica = "8"


class Matriculacion(pydantic.BaseModel):

    fechaMatriculacion: datetime.date
    """Fecha de matriculación del vehículo.
    clave=FEC_MATRICULA
    posicion=1
    longitud=8
    """

    claseMatricula: ClaseMatriculaEnum
    """Código de clase de la matrícula.
    clave=COD_CLASE_MAT
    posicion=2
    longitud=1
    """

    fechaTransferencia: Optional[datetime.date]
    """Fecha de tramitación, que se corresponde con la fecha de transferencia del vehículo
    contenida en los datos de transferencias.
    clave=FEC_TRAMITACION
    posicion=3
    longitud=8
    """

    vehiculoMarca: str
    """Marca del vehículo.
    clave=MARCA_ITV
    posicion=4
    longitud=30
    """

    vehiculoModelo: str
    """Modelo del vehículo
    clave=MODELO_ITV
    posicion=5
    longitud=22
    """

    codigoProcedencia: str
    """Código de la procedencia del vehículo.
    clave=COD_PROCEDENCIA_ITV
    posicion=6
    longitud=1
    """

    bastidor: str
    """Número de bastidor.
    clave=BASTIDOR_ITV
    posicion=7
    longitud=21
    """

    codigoTipo: str
    """Código del tipo de vehículo.
    clave=COD_TIPO
    posicion=8
    longitud=2
    """

    codPropulsion: str
    """Código del tipo de propulsión.
    clave=COD_PROPULSION_ITV
    posicion=9
    longitud=1
    """

    cilindrada: float
    """Cilindrada del vehículo.
    clave=CILINDRADA_ITV
    posicion=10
    longitud=5
    """

    potencia: float
    """Potencia fiscal del vehículo, en CVF. Redondeado a la segunda cifra decimal.
    clave=POTENCIA_ITV
    posicion=11
    longitud=6
    """

    tara: float
    """Tara (peso) del vehículo.
    clave=TARA
    posicion=12
    longitud=6
    """

    pesoMaximo: float
    """Peso máximo del vehículo.
    clave=PESO_MAX
    posicion=13
    longitud=6
    """

    plazas: int
    """Número de plazas del vehículo. Para vehículos de carga, número de plazas máximo permitido cuando está descargado.
    clave=NUM_PLAZAS
    posicion=14
    longitud=3
    """

    precintado: bool
    """Indicador de vehículo precintado.
    clave=IND_PRECINTO
    posicion=15
    longitud=2
    """

    embargado: bool
    """Indicador de vehículo embargado.
    clave=IND_EMBARGO
    posicion=16
    longitud=2
    """

    transmisiones: int
    """Número de transmisiones que ha tenido el vehículo.
    clave=NUM_TRANSMISIONES
    posicion=17
    longitud=2
    """

    titulares: int
    """Número de titulares del vehículo.
    clave=NUM_TITULARES
    posicion=18
    longitud=2
    """

    localidad: str
    """Localidad del domicilio del vehículo.
    clave=LOCALIDAD_VEHICULO
    posicion=19
    longitud=24
    """

    provincia: str
    """Provincia donde está domiciliado el vehículo.
    clave=COD_PROVINCIA_VEH
    posicion=20
    longitud=2
    """

    provinciaMatriculacion: str
    """Provincia donde fue matriculado el vehículo.
    clave=COD_PROVINCIA_MAT
    posicion=21
    longitud=2
    """

    tramite: str
    """Código del trámite.
    clave=CLAVE_TRAMITE
    posicion=22
    longitud=1
    """

    fechaTramite: datetime.date
    """Fecha en la que se realizó el trámite.
    clave=FEC_TRAMITE
    posicion=23
    longitud=8
    """

    codigoPostal: str
    """Código postal donde está domiciliado el vehículo.
    clave=CODIGO_POSTAL
    posicion=24
    longitud=5
    """

    fechaPrimeraMatriculacion: Optional[datetime.date]
    """Fecha de la primera matriculación del vehículo
    clave=FEC_PRIM_MATRICULACION
    posicion=25
    longitud=8
    """

    nuevo: bool
    """Indica si el vehículo es nuevo (True) o usado (False) al momento de la fechaMatriculacion.
    clave=IND_NUEVO_USADO
    posicion=26
    longitud=1
    """

    personaJuridica: bool
    """Indica si el titular del vehículo es una persona física (False) o jurídica (True).
    clave=PERSONA_FISICA_JURIDICA
    posicion=27
    longitud=1
    """

    codigoITV: str
    """Código ITV.
    clave=CODIGO_ITV
    posicion=28
    longitud=9
    """

    servicio: str
    """Código de servicio del vehículo.
    clave=SERVICIO
    posicion=29
    longitud=3
    """

    codigoMunicipioINE: int
    """Código INE del municipio del domicilio del vehículo.
    clave=COD_MUNICIPIO_INE_VEH
    posicion=30
    longitud=5
    """

    municipio: str
    """Nombre del municipio donde está domiciliado el vehículo.
    clave=MUNICIPIO
    posicion=31
    longitud=30
    """

    potenciaKW: Optional[float]
    """Potencia neta máxima en kW.
    clave=KW_ITV
    posicion=32
    longitud=7
    """

    plazasMaximo: int
    """Número máximo de plazas del vehículo. Para vehículos de carga, número de plazas máximo permitido cuando está cargado.
    clave=NUM_PLAZAS_MAX
    posicion=33
    longitud=3
    """

    co2: Optional[int]
    """Emisiones de CO2 del vehículo.
    clave=CO2_ITV
    posicion=34
    longitud=5
    """

    renting: bool
    """Indica si es un vehículo de renting (True).
    clave=RENTING
    posicion=35
    longitud=1
    """

    titularTutelado: bool
    """Indica si el vehículo está a nombre de un titular menor de edad o con tutela judicial.
    clave=COD_TUTELA
    posicion=36
    longitud=1
    """

    class Config:
        anystr_strip_whitespace = True

    @property
    def cargaUtil(self) -> float:
        return self.pesoMaximo - self.tara

    @pydantic.validator("fechaMatriculacion", "fechaTransferencia", "fechaTramite", "fechaPrimeraMatriculacion", pre=True)
    def convert_date(cls, v):
        """Convierte fechas del formato 'YYMMDD' a 'YYYY-MM-DD'."""
        if isinstance(v, str) and len(v) == 8:
            day = v[0:2]
            month = v[2:4]
            year = v[4:8]
            v = f"{year}-{month}-{day}"
        if not v:
            v = None

        return v

    @pydantic.validator("precintado", "embargado", "renting", "titularTutelado", pre=True)
    def convert_boolean(cls, v):
        if isinstance(v, str):
            if v == "SI" or v == "S":
                return True
            if not v or v == "NO" or v == "N":
                return False
        return v

    @pydantic.validator("co2", pre=True)
    def convert_empty_nullables(cls, v):
        if v == "":
            return None
        return v

    @pydantic.validator("nuevo", pre=True)
    def convert_estado_nuevo(cls, v):
        if isinstance(v, str):
            if v == "N":
                return True
            if v == "U":
                return False
        return v

    @pydantic.validator("personaJuridica", pre=True)
    def convert_persona_juridica(cls, v):
        if isinstance(v, str):
            if v == "X":
                return True
            if v == "D":
                return False
        return v

    @pydantic.validator("potenciaKW", pre=True)
    def convert_potenciakw(cls, v):
        if v == "*******":
            return None
        return v

    @classmethod
    def get_fields_metadata(cls):
        singleton_attr_name = "__claves_fields_singleton"
        try:
            return getattr(cls, singleton_attr_name)
        except AttributeError:
            fields_docs = class_doc.extract_docs_from_cls_obj(cls)
            result = [
                CampoMetadata.from_docstring(
                    field_name=field_name,
                    docstring_lines=field_docs_lines,
                )
                for field_name, field_docs_lines in fields_docs.items()
            ]
            result.sort(key=lambda metadata: metadata.posicion)

            setattr(cls, singleton_attr_name, result)
            return result
