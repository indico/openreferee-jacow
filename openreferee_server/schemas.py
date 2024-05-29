from marshmallow import EXCLUDE, Schema, validate
from webargs import fields

from .defaults import SERVICE_INFO


class ListEndpointSchema(Schema):
    create = fields.String(required=True)
    list = fields.String(required=True)


class EventEndpointsSchema(Schema):
    tags = fields.Nested(ListEndpointSchema)
    editable_types = fields.String(required=True)
    file_types = fields.Dict(
        keys=fields.String(),
        values=fields.Nested(ListEndpointSchema),
        required=True,
    )


class EditableEndpointsSchema(Schema):
    revisions = fields.Nested(
        {
            "details": fields.String(required=True),
            "replace": fields.String(required=True),
            "undo": fields.String(required=True),
        }
    )
    file_upload = fields.String(required=True)


class EventSchema(Schema):
    title = fields.String(required=True)
    url = fields.URL(schemes={"http", "https"}, required=True)
    token = fields.String(required=True)
    endpoints = fields.Nested(EventEndpointsSchema, required=True)


class EventInfoServiceSchema(Schema):
    version = fields.String()
    name = fields.String()


class EventInfoSchema(Schema):
    title = fields.String(required=True)
    url = fields.URL(schemes={"http", "https"}, required=True)
    can_disconnect = fields.Boolean(required=True, default=True)
    service = fields.Nested(
        EventInfoServiceSchema,
        required=True,
        default=SERVICE_INFO,
    )


class SignedFileSchema(Schema):
    uuid = fields.String(required=True)
    filename = fields.String(required=True)
    content_type = fields.String()
    file_type = fields.Integer(required=True)
    signed_download_url = fields.String(required=True)


class TagSchema(Schema):
    id = fields.Integer(required=True)
    code = fields.String(required=True)
    title = fields.String(required=True)
    color = fields.String()
    system = fields.Boolean()
    verbose_title = fields.String()
    is_used_in_revision = fields.Boolean()
    url = fields.String()


class RevisionTypeSchema(Schema):
    name = fields.String(required=True)
    title = fields.String(allow_none=True)
    css_class = fields.String(allow_none=True)


class EditingUserSchema(Schema):
    id = fields.Integer(required=True)
    full_name = fields.String(required=True)
    identifier = fields.String(required=True)
    avatar_url = fields.String()


class EditableSchema(Schema):
    id = fields.Integer(required=True)
    type = fields.String()
    state = fields.String(required=True)
    editor = fields.Nested(EditingUserSchema, allow_none=True)
    timeline_url = fields.String()
    revision_count = fields.Integer()


class _BaseRevisionSchema(Schema):
    comment = fields.String(required=True)
    user = fields.Nested(EditingUserSchema, required=True)
    type = fields.Nested(RevisionTypeSchema)
    tags = fields.List(fields.Nested(TagSchema))


class RevisionSchema(_BaseRevisionSchema):
    files = fields.List(fields.Nested(SignedFileSchema, unknown=EXCLUDE, required=True))


class TransientRevisionSchema(_BaseRevisionSchema):
    files = fields.List(fields.Nested(SignedFileSchema, unknown=EXCLUDE, required=True))


class RoleSchema(Schema):
    name = fields.String()
    code = fields.String()
    source = fields.String(validate=validate.OneOf(["event", "category"]))


class UserSchema(Schema):
    id = fields.Integer(required=True)
    full_name = fields.String(required=True)
    email = fields.String(required=True)
    manager = fields.Boolean(required=True)
    editor = fields.Boolean(required=True)
    submitter = fields.Boolean(required=True)
    roles = fields.List(fields.Nested(RoleSchema), required=True)


class CreateEditableSchema(Schema):
    editable = fields.Nested(EditableSchema, required=True)
    revision = fields.Nested(RevisionSchema, unknown=EXCLUDE, required=True)
    endpoints = fields.Nested(EditableEndpointsSchema, required=True)
    user = fields.Nested(UserSchema, required=True)


class CreateEditableResponseSchema(Schema):
    ready_for_review = fields.Boolean(load_default=False)


class ReviewEditableSchema(Schema):
    action = fields.String(required=True)
    revision = fields.Nested(TransientRevisionSchema, unknown=EXCLUDE, required=True)
    endpoints = fields.Nested(EditableEndpointsSchema, required=True)
    user = fields.Nested(UserSchema, required=True)


class CommentSchema(Schema):
    text = fields.String()
    internal = fields.Boolean()


class ReviewResponseSchema(Schema):
    publish = fields.Boolean()
    tags = fields.List(fields.Integer())
    comment = fields.String()
    comments = fields.List(fields.Nested(CommentSchema))


class SuccessSchema(Schema):
    success = fields.Boolean(required=True)


class ServiceInfoSchema(Schema):
    name = fields.String(required=True)
    version = fields.String(required=True)


class IdentifierParameter(Schema):
    identifier = fields.String(
        required=True, description="The unique ID which represents the event"
    )


class EditableParameters(Schema):
    class Meta:
        # avoid inconsistency when generating openapi locally and during CI
        ordered = True

    identifier = fields.String(
        required=True, description="The unique ID which represents the event"
    )
    contrib_id = fields.Integer(
        required=True, description="The unique ID which represents the contribution"
    )
    editable_type = fields.String(
        required=True, description="The name which represents the editable type"
    )


class ReviewParameters(EditableParameters):
    revision_id = fields.String(
        required=True, description="The unique ID which represents the revision"
    )


class ServiceActionsRequestSchema(Schema):
    revision = fields.Nested(RevisionSchema, unknown=EXCLUDE, required=True)
    user = fields.Nested(UserSchema, required=True)


class ServiceTriggerActionRequestSchema(ServiceActionsRequestSchema):
    action = fields.String(required=True)
    endpoints = fields.Nested(EditableEndpointsSchema, required=True)


class ServiceActionSchema(Schema):
    name = fields.String(required=True)
    title = fields.String(required=True)
    color = fields.String(missing=None)
    icon = fields.String(missing=None)
    confirm = fields.String(missing=None)


class ServiceActionResultSchema(Schema):
    publish = fields.Boolean(missing=None)
    comments = fields.List(fields.Nested(CommentSchema))
    tags = fields.List(fields.Int())
    redirect = fields.String(missing=None)
    reset = fields.Boolean(missing=False)
