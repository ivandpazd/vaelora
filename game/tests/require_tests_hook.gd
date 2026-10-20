extends GutHookScript


func run() -> void:
	if gut.get_test_collector().get_ran_test_count() == 0:
		gut.logger.error("No GUT tests ran; check the selected test directory and filters.")
		set_exit_code(1)
