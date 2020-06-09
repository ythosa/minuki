.PHONY: build
build:
	python server.py

.PHONY: sql
sql:
	C:/sqlite/sqlite3 ./db/finance.db < createdb.sql # Version of linux to run it on ubuntu :)

.PHONY: tokens
tokens:
	git update-index --assume-unchanged tokens.py

.DEFAULT_GOAL := build
