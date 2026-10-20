extends GutTest

const ContentCatalog = preload("res://content/content_catalog.gd")
const CivilizationDefinitionScript = preload("res://content/resources/civilization_definition.gd")
const TerrainDefinitionScript = preload("res://content/resources/terrain_definition.gd")
const AUREN = preload("res://content/data/civilizations/auren_league.tres")
const BRASAL = preload("res://content/data/civilizations/brasal_clans.tres")
const MEADOW = preload("res://content/data/terrain/meadow.tres")


func test_content_resources_match_their_contracts() -> void:
	assert_eq(AUREN.get_script(), CivilizationDefinitionScript)
	assert_eq(BRASAL.get_script(), CivilizationDefinitionScript)
	assert_eq(MEADOW.get_script(), TerrainDefinitionScript)
	assert_true(AUREN.validate().is_empty())
	assert_true(BRASAL.validate().is_empty())
	assert_true(MEADOW.validate().is_empty())
	assert_eq(AUREN.shared_unit_ids, BRASAL.shared_unit_ids)
	assert_eq(AUREN.shared_building_ids, BRASAL.shared_building_ids)
	assert_eq(AUREN.shared_improvement_ids, BRASAL.shared_improvement_ids)
	assert_eq(AUREN.shared_technology_ids, BRASAL.shared_technology_ids)
	assert_eq(AUREN.shared_unit_ids.size(), 5)
	assert_eq(AUREN.shared_building_ids.size(), 4)
	assert_eq(AUREN.shared_improvement_ids.size(), 5)
	assert_eq(AUREN.shared_technology_ids.size(), 12)
	assert_eq(AUREN.unique_technology_ids.size(), 2)
	assert_eq(BRASAL.unique_technology_ids.size(), 2)
	assert_false(AUREN.palette_hex.is_empty())
	assert_false(BRASAL.palette_hex.is_empty())
	assert_ne(AUREN.heraldic_mark_description, BRASAL.heraldic_mark_description)
	assert_eq(AUREN.city_name_pool.size(), 15)
	assert_eq(BRASAL.city_name_pool.size(), 15)
	assert_eq(MEADOW.food_yield, 2)
	assert_eq(MEADOW.land_movement_cost, 1)
	assert_eq(MEADOW.legal_improvement_ids, ["improvement.farm"])
	assert_true(ContentCatalog.is_valid_id("terrain.meadow"))
	assert_false(ContentCatalog.is_valid_id("Meadow"))
	assert_false(ContentCatalog.is_valid_id("terrain.Meadow"))


func test_content_catalog_registers_and_resolves_unique_ids() -> void:
	var catalog = ContentCatalog.new()
	assert_true(catalog.register(AUREN).is_empty())
	assert_true(catalog.register(BRASAL).is_empty())
	assert_true(catalog.register(MEADOW).is_empty())
	assert_eq(catalog.get_definition(AUREN.id), AUREN)
	assert_null(catalog.get_definition("civilization.missing"))

	var duplicate = AUREN.duplicate(true) as Resource
	assert_false(catalog.register(duplicate).is_empty())
	assert_eq(catalog.get_definition(AUREN.id), AUREN)
