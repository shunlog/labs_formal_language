README.md: README.org
	emacs --visit README.org --batch -l config.el -f org-md-export-to-markdown
