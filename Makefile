.PHONY: preview check serve all

# Edit records, then `make preview` and open preview.html. No Ruby required.
preview: check
	python3 bin/build_preview.py

# Schema and vocabulary checks. Run before opening a pull request.
check:
	python3 bin/validate.py

# The real site. Needs Ruby and `bundle install` once.
serve:
	bundle exec jekyll serve --livereload

all: check preview
