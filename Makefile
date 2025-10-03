.PHONY: help generate test

help:
	@echo "Available commands:"
	@echo "  make generate  - Generate consolidated qrcode file"
	@echo "  make test      - Run tests against golden masters"
	@echo "  make help      - Show this help message"

generate:
	python bundler.py python-qrcode/qrcode

test: generate
	python test_qrcode.py
