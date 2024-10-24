[tool.poetry]
name = "parser_kufar"
version = "0.1.0"
description = ""
authors = ["shuckiy73 <121363089+shuckiy73@users.noreply.github.com>"]
readme = "README.md"

[tool.poetry.dependencies]
python = "^3.12"
aiogram = "^2.21"
requests = "^2.25.1"
beautifulsoup4 = "^4.9.3"
aiohttp = "^3.8.6"
cleo = "^2.0.0"  # Убедитесь, что версия cleo совместима

[tool.poetry.dev-dependencies]
pytest = "^6.2.2"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"