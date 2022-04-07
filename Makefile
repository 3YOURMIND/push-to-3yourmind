

documentation:
	rm -R docs
	mkdir docs
	pdoc -o docs --html --config sort_identifiers=False --force push_to_3yourmind
	mv docs/push_to_3yourmind/* docs/
	rmdir docs/push_to_3yourmind
