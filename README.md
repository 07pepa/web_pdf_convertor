# PDF CONVERSION DEMO PROJECT

WARNING this project creates ./data folder for ease of debugging  (what was saved and what was converted)
please keep it tidy and never ever push it to server !

## getting started

for ease of developing you should install python 3.11 and install all requirements from ./requirements
otherwise pycharm may not know what you are using...usage of virtual environment is highly recommender

## building in docker

just simple  `docker-compose build` from project root will work if you want to run it locally then
look for python version in dockerfiles located and install libmagic1
and install all requirements from ./requirements `source .env` file, but it's not recommend.
because you need to manage version and starting of postgres and rabbit as vel

## running tests

from project root just run pytest

## example conversion

run  `docker-compose up`  and wait for following text

```
api-1     | Django version 4.2, using settings 'pdf_convertor.settings'
api-1     | Starting development server at http://0.0.0.0:8000/
api-1     | Quit the server with CONTROL-C
```

### upload

```bash
cd ./tests/resources
```

```bash
curl localhost:8000/documents/ --data-binary @tests.pdf -H "Content-Disposition: attachment;filename=test.pdf"
```

### query state of conversion

```bash
curl localhost:8000/documents/<id from upload>
```

### get png

```bash
curl localhost:8000/documents/<id from upload>/<page>
```

## Known limitation

only one uuid can be uploaded at time
unhandled exception during conversion (should be rare and only in case of corrupted pdf)
probably just modify api to allow more states (failed)

missing rights (aka no ownership of pdf conversion/state everyone can read everything)
