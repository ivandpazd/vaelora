class_name TerrainDefinition
extends "res://content/content_definition.gd"

enum MovementDomain { LAND, NAVAL, IMPASSABLE }

@export var movement_domain: MovementDomain = MovementDomain.LAND
@export_range(1, 100, 1) var land_movement_cost: int = 1
@export_range(1, 100, 1) var naval_movement_cost: int = 1
@export var food_yield: int = 0
@export var production_yield: int = 0
@export var coin_yield: int = 0
@export_range(0.0, 1.0, 0.01) var defense_modifier: float = 0.0
@export var vision_bonus: int = 0
@export var blocks_line_of_sight: bool = false
@export var workable_city_territory: bool = false
@export var legal_improvement_ids: Array[String] = []
@export var allows_roads: bool = false


func validate() -> PackedStringArray:
	var errors := super.validate()
	if not id.begins_with("terrain."):
		errors.append("Terrain IDs must use the terrain namespace: %s" % id)
	if food_yield < 0 or production_yield < 0 or coin_yield < 0 or vision_bonus < 0:
		errors.append("Terrain yields and vision bonus cannot be negative: %s" % id)
	if movement_domain == MovementDomain.IMPASSABLE and (workable_city_territory or allows_roads or not legal_improvement_ids.is_empty()):
		errors.append("Impassable terrain cannot be workable or support roads/improvements: %s" % id)
	var seen := {}
	for improvement_id in legal_improvement_ids:
		if not ContentCatalogScript.is_valid_id(improvement_id) or seen.has(improvement_id):
			errors.append("Terrain improvement IDs must be valid and unique: %s" % id)
			break
		seen[improvement_id] = true
	return errors
