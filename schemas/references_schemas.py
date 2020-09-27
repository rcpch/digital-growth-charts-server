from marshmallow import Schema, fields


class ReferenceSchema(Schema):
    author = fields.String(
        description="The published authors of the Reference data (if available)")
    chart_name = fields.String(
        description="The common name of the reference data (if available)")
    date = fields.String(
        description="Date of publication of the reference data (if available)")
    description = fields.String(
        description="Description of the reference data: type of data, intended usage, limitations, applicable age ranges (if available)")
    file_name = fields.String(
        description="File name of the reference within our codebase (if available)")
    acknowledgement_text = fields.String(
        description="Acknowledgement text regarding the origin of the reference data (if available)")
    publication_reference = fields.String(
        description="Standard publication citation (if available)")
    publication_url = fields.String(
        description="URL for the publication (if available)")


class ReferencesResponseSchema(Schema):
    # Defines the schema of the API response. This is compiled into the openAPI spec.
    references = fields.List(fields.Nested(ReferenceSchema()))
