.PHONY: build
build:
	python server.py

.PHONY: sql
sql:
	c:/sqlite/sqlite3 finance.db < createdb.sql

.DEFAULT_GOAL := build