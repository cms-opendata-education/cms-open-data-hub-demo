# Adding a resource

Copy any file in `_resources/` and edit it. The fields below are the whole
schema; `python bin/validate.py` will tell you what is missing or misspelled.

Required: `title`, `status`, `last_verified`, `summary`, `audience`,
`languages`, `duration`, `setup_burden`, `links`, `license`.

Every value in `status`, `setup_burden`, `audience`, `physics_topics`,
`computing_topics`, `tags`, `prerequisites.*`, `data.formats`, and `links[].type`
must appear in `_data/vocab.yml`. If the term you need is not there, add it in
the same pull request with a one-line label.

## Fields that people get wrong

**`setup_burden`** is what a *teacher* has to arrange before class, not what the
activity is built with. A notebook you hand out as a Colab link is `colab` even
if it uses ROOT internally.

**`status`** describes maintenance, not quality. `unmaintained` material stays
listed and stays searchable. Use `archived` only for things that no longer work
at all.

**`last_verified`** means someone opened the links and they resolved. Bump it
when you check, not when you edit.

**`summary`** is what students do, in plain language, in two or three sentences.
Not what it teaches, not why it matters. Write it for someone deciding in ten
seconds whether to click.

## Description

Below the front matter, write a couple of paragraphs. Useful things to say:
where it has actually been used and with whom, what to do first, what students
find hard, what to cut if you are short of time. Avoid restating the metadata.

## Testimonials

Add to `_data/testimonials.yml` under the resource id. Honest is better than
enthusiastic. Anonymous is fine — use "Workshop participant".
