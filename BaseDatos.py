from sqlalchemy import create_engine, schema, types
from sqlalchemy import MetaData, Column, Table, ForeignKey, UniqueConstraint

metadata = schema.MetaData()

tabla_letras = schema.Table('letras', metadata,
                            schema.Column('id', types.Integer,
                                          primary_key=True),
                            schema.Column('caracterTexto', types.String(1),
                                          unique=True),
                            schema.Column('codigoMorse', types.String(10)),
                            )

engine = create_engine('sqlite:///ConversorMorse.db', echo=False)
metadata.bind = engine

metadata.create_all(checkfirst=True)
