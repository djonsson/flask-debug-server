clean:
	rm -fr ci

install:
	pip install flask
	pip install pytest

make test:
	-make unit
	-make system

unit:
	py.test --junitxml ci/reports/unit.tests.xml flask-server/tests/unit.py

system:
	py.test --junitxml ci/reports/system.tests.xml flask-server/tests/system.py

ci:
	make install
	make test
	zip -r application.zip flask-server/src/application.py flask-server/src/requirements.txt