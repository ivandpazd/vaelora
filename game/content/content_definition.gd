class_name ContentDefinition
extends Resource

const ContentCatalogScript = preload("res://content/content_catalog.gd")

@export var id: String = ""
@export var display_name: String = ""


func validate() -> PackedStringArray:
	var errors := PackedStringArray()
	if not ContentCatalogScript.is_valid_id(id):
		errors.append("Content ID must use a lowercase namespaced identifier: %s" % id)
	if display_name.strip_edges().is_empty():
		errors.append("Content display name must not be empty: %s" % id)
	return errors
