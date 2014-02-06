from peewee import (
    CompositeKey, Clause, SQL, EnclosedClause, ForeignKeyField,
)

from arnold.exceptions import FieldNotFoundException, FieldsRequiredException


def create_table_sql(model_class, fields, safe=False):
    compiler = model_class._meta.database.compiler()
    statement = 'CREATE TABLE IF NOT EXISTS' if safe else 'CREATE TABLE'
    meta = model_class._meta

    columns, constraints = [], []
    if isinstance(meta.primary_key, CompositeKey):
        pk_cols = [meta.fields[f]._as_entity()
                   for f in meta.primary_key.field_names]
        constraints.append(Clause(
            SQL('PRIMARY KEY'), EnclosedClause(*pk_cols)))

    for field in meta.get_fields():
        columns.append(compiler.field_definition(field))
        if isinstance(field, ForeignKeyField) and not field.deferred:
            constraints.append(compiler.foreign_key_constraint(field))

    return compiler.parse_node(
        Clause(
            SQL(statement),
            model_class._as_entity(),
            EnclosedClause(*(columns + constraints)))
    )


def create_table(model_class, field_names=[], safe=False):
    db = model_class._meta.database
    pk = model_class._meta.primary_key
    if db.sequences and pk.sequence:
        if not db.sequence_exists(pk.sequence):
            db.create_sequence(pk.sequence)

    if len(field_names) <= 0:
        raise FieldsRequiredException
    fields = []
    for name in field_names:
        field = model_class._meta.fields.get(name)
        if field is None:
            raise FieldNotFoundException
        fields.append(field)

    model_class._meta.database.execute_sql(
        *create_table_sql(model_class, fields, safe)
    )

    model_class._create_indexes()
