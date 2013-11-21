from peewee import CompositeKey

from arnold.exceptions import FieldNotFoundException, FieldsRequiredException


def create_table_sql(model_class, fields, safe=False):
    compiler = model_class._meta.database.compiler()
    parts = ['CREATE TABLE']
    if safe:
        parts.append('IF NOT EXISTS')
    meta = model_class._meta
    parts.append(compiler.quote(meta.db_table))
    columns = map(compiler.field_sql, fields)
    if isinstance(meta.primary_key, CompositeKey):
        pk_cols = map(compiler.quote, (
            meta.fields[f].db_column for f in meta.primary_key.fields))
        columns.append('PRIMARY KEY (%s)' % ', '.join(pk_cols))
    parts.append('(%s)' % ', '.join(columns))
    return parts


def create_table(model_class, field_names=[], safe=False):
    if len(field_names) <= 0:
        raise FieldsRequiredException
    fields = []
    for name in field_names:
        field = model_class._meta.fields.get(name)
        if field is None:
            raise FieldNotFoundException
        fields.append(field)

    model_class._meta.database.execute_sql(
        ' '.join(create_table_sql(model_class, fields, safe))
    )
