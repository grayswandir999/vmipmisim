all:
	python3 setup.py sdist

clean:
	rm -fr dist ipmisim.egg-info ipmisim/*pyc
