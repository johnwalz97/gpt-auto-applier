format:
# format code using black and isort
	black gpt_auto_applier
	isort gpt_auto_applier

lint:
# lint code using ruff
	ruff check gpt_auto_applier
