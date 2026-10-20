class_name ContentCatalog
extends RefCounted

const CONTENT_ID_PATTERN := "^[a-z][a-z0-9_]*(\\.[a-z][a-z0-9_]*)+$"

var _definitions: Dictionary = {}


static func is_valid_id(content_id: String) -> bool:
	var pattern := RegEx.new()
	if pattern.compile(CONTENT_ID_PATTERN) != OK:
		return false
	return pattern.search(content_id) != null


func register(definition: Resource) -> PackedStringArray:
	if definition == null:
		return PackedStringArray(["Cannot register a null content definition."])
	if not definition.has_method("validate") or not "id" in definition:
		return PackedStringArray(["Resource does not implement the content definition contract."])
	var errors: PackedStringArray = definition.validate()
	if not errors.is_empty():
		return errors
	if _definitions.has(definition.id):
		return PackedStringArray(["Duplicate content ID: %s" % definition.id])
	_definitions[definition.id] = definition
	return PackedStringArray()


func get_definition(content_id: String) -> Resource:
	return _definitions.get(content_id) as Resource


func get_definition_count() -> int:
	return _definitions.size()
