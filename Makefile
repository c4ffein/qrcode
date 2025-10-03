.PHONY: help generate test

help:
	@echo "Available commands:"
	@echo "  make get-submodule  - Get the missing submodule"
	@echo "  make generate       - Generate consolidated qrcode file"
	@echo "  make test           - Run tests against golden masters"
	@echo "  make help           - Show this help message"

get-submodule:
	git submodule update --init --recursive

generate:
	python bundler.py python-qrcode/qrcode

test: generate
	python test_qrcode.py
