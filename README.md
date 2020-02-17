# In development

Quiz app with using Wikidata for data factories

## Installation:
### using docker
* cp .env_DEFAULT .env
* cp alembic.ini_DEFAULT alembic.ini
* docker-compose up -d
* docker exec -it <docker id of app container from 'docker ps'> python run_factory.py

## Run factories
python run_factory.py - fill the database with countries
### Other factories
You can add new class to factories/factories.py

Example for presidents of USA
```python
class PresidentOfUSAFactory(ObjectFactory):
    category_name = 'Presidents of USA'
    filters = [{'property': 'P39', 'entity': 'Q11696'}]
    aliases = ['P734']
```
* `property` - property in Wikidata (`P39` - position held)
* `entity` - value of property (`Q11696` - President of the United States)
* `aliases` - additional aliases for correct answer (`P734` - family name)

See on Wikidata:
* https://www.wikidata.org/wiki/Q22686 

## Add question
* Add `category_id`, `text` and  `image_question_wikidata_prop` (text, sound and coordinates questions not supported yet)

## API
* /api/ask - get image url 
* /api/check - check answers (e.g. {"answer": "Colombia"})

# TODO
* Add support for text and coords question
* Multiple game
* Telegram bot
* example react app

## ISSUES
* Very slow /ask/ endpoint. A lot of time spent SVG to PNG converting (needs for Telegram bot)
