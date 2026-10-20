extends SceneTree

const ContentCatalog = preload("res://content/content_catalog.gd")
const CivilizationDefinitionScript = preload("res://content/resources/civilization_definition.gd")
const TerrainDefinitionScript = preload("res://content/resources/terrain_definition.gd")
const AUREN = preload("res://content/data/civilizations/auren_league.tres")
const BRASAL = preload("res://content/data/civilizations/brasal_clans.tres")
const MEADOW = preload("res://content/data/terrain/meadow.tres")


func _initialize() -> void:
	var failures: Array[String] = []
	_expect(AUREN.get_script() == CivilizationDefinitionScript, "Auren data uses the civilization resource type.", failures)
	_expect(BRASAL.get_script() == CivilizationDefinitionScript, "Brasal data uses the civilization resource type.", failures)
	_expect(MEADOW.get_script() == TerrainDefinitionScript, "Meadow data uses the terrain resource type.", failures)
	_expect(AUREN.validate().is_empty(), "Auren content passes schema validation.", failures)
	_expect(BRASAL.validate().is_empty(), "Brasal content passes schema validation.", failures)
	_expect(MEADOW.validate().is_empty(), "Meadow content passes schema validation.", failures)
	_expect(AUREN.shared_unit_ids == BRASAL.shared_unit_ids, "Both civilizations reference the same shared unit IDs.", failures)
	_expect(AUREN.shared_building_ids == BRASAL.shared_building_ids, "Both civilizations reference the same shared building IDs.", failures)
	_expect(AUREN.shared_improvement_ids == BRASAL.shared_improvement_ids, "Both civilizations reference the same shared improvement IDs.", failures)
	_expect(AUREN.shared_technology_ids == BRASAL.shared_technology_ids, "Both civilizations reference the same shared technology IDs.", failures)
	_expect(AUREN.shared_unit_ids.size() == 5, "The prototype references all five shared unit definitions.", failures)
	_expect(AUREN.shared_building_ids.size() == 4, "The prototype references all four shared building definitions.", failures)
	_expect(AUREN.shared_improvement_ids.size() == 5, "The prototype references all five shared improvement and road definitions.", failures)
	_expect(AUREN.shared_technology_ids.size() == 12, "The prototype references all twelve shared technologies.", failures)
	_expect(AUREN.unique_technology_ids.size() == 2, "Auren references its two approved unique technologies.", failures)
	_expect(BRASAL.unique_technology_ids.size() == 2, "Brasal references its two approved unique technologies.", failures)
	_expect(not AUREN.palette_hex.is_empty() and not BRASAL.palette_hex.is_empty(), "Both civilizations provide authored palettes.", failures)
	_expect(AUREN.heraldic_mark_description != BRASAL.heraldic_mark_description, "Civilizations retain their distinct approved heraldry.", failures)
	_expect(AUREN.city_name_pool.size() == 15, "Auren contains its approved city-name pool.", failures)
	_expect(BRASAL.city_name_pool.size() == 15, "Brasal contains its approved city-name pool.", failures)
	_expect(MEADOW.food_yield == 2 and MEADOW.land_movement_cost == 1, "Meadow matches its canonical base yield and movement cost.", failures)
	_expect(MEADOW.legal_improvement_ids == ["improvement.farm"], "Meadow references its approved legal improvement by ID.", failures)
	_expect(ContentCatalog.is_valid_id("terrain.meadow"), "Namespaced lowercase content IDs are accepted.", failures)
	_expect(not ContentCatalog.is_valid_id("Meadow") and not ContentCatalog.is_valid_id("terrain.Meadow"), "Unnamespaced or case-variant content IDs are rejected.", failures)

	var catalog = ContentCatalog.new()
	_expect(catalog.register(AUREN).is_empty(), "A valid content definition registers.", failures)
	_expect(catalog.register(BRASAL).is_empty(), "A second unique content definition registers.", failures)
	_expect(catalog.register(MEADOW).is_empty(), "A terrain definition registers in the same catalog.", failures)
	_expect(catalog.get_definition(AUREN.id) == AUREN, "Definitions resolve by stable ID.", failures)
	_expect(catalog.get_definition("civilization.missing") == null, "Unknown IDs resolve to null rather than a different definition.", failures)

	var duplicate = AUREN.duplicate(true) as Resource
	_expect(not catalog.register(duplicate).is_empty(), "Duplicate IDs are rejected.", failures)
	_expect(catalog.get_definition(AUREN.id) == AUREN, "A duplicate cannot overwrite the registered definition.", failures)

	if failures.is_empty():
		print("Content contract checks passed.")
		quit(0)
		return

	for failure in failures:
		push_error(failure)
	quit(1)


func _expect(condition: bool, message: String, failures: Array[String]) -> void:
	if not condition:
		failures.append(message)
