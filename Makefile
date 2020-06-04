.PHONY: build
build:
	python server.py

.PHONY: sql
sql:
	c:/sqlite/sqlite3 finance.db < createdb.sql

.PHONY: tokens
tokens:
	git update-index --assume-unchanged tokens.py

.DEFAULT_GOAL := build