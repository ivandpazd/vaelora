class_name CivilizationDefinition
extends "res://content/content_definition.gd"

@export_multiline var identity_statement: String = ""
@export var heraldic_mark_description: String = ""
@export var palette_hex: Dictionary = {}
@export_multiline var silhouette_description: String = ""
@export var naming_voice: String = ""
@export var shared_unit_ids: Array[String] = []
@export var shared_building_ids: Array[String] = []
@export var shared_improvement_ids: Array[String] = []
@export var shared_technology_ids: Array[String] = []
@export var unique_technology_ids: Array[String] = []
@export var city_name_pool: Array[String] = []


func validate() -> PackedStringArray:
	var errors := super.validate()
	if not id.begins_with("civilization."):
		errors.append("Civilization IDs must use the civilization namespace: %s" % id)
	if identity_statement.strip_edges().is_empty():
		errors.append("Civilization identity statement must not be empty: %s" % id)
	if heraldic_mark_description.strip_edges().is_empty() or palette_hex.is_empty() or silhouette_description.strip_edges().is_empty() or naming_voice.strip_edges().is_empty():
		errors.append("Civilization presentation identity must be defined: %s" % id)
	_validate_ids(shared_unit_ids, "shared unit", errors)
	_validate_ids(shared_building_ids, "shared building", errors)
	_validate_ids(shared_improvement_ids, "shared improvement", errors)
	_validate_ids(shared_technology_ids, "shared technology", errors)
	_validate_ids(unique_technology_ids, "unique technology", errors)
	if city_name_pool.is_empty():
		errors.append("Civilization city-name pool must not be empty: %s" % id)
	var seen_names := {}
	for city_name in city_name_pool:
		var normalized := city_name.strip_edges().to_lower()
		if normalized.is_empty() or seen_names.has(normalized):
			errors.append("City-name pool entries must be non-empty and unique: %s" % id)
			break
		seen_names[normalized] = true
	return errors


func _validate_ids(values: Array[String], category: String, errors: PackedStringArray) -> void:
	var seen := {}
	for value in values:
		if not ContentCatalogScript.is_valid_id(value) or seen.has(value):
			errors.append("Civilization %s IDs must be valid and unique: %s" % [category, id])
			return
		seen[value] = true
