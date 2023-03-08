#!/usr/bin/env doomscript

(setq
 org-confirm-babel-evaluate 'nil
 org-src-preserve-indentation 't)

(require 'doom-start)
(require 'ob)
(require 'ox-hugo)

(org-babel-do-load-languages
 'org-babel-load-languages
 '((octave . t) (python . t)(emacs-lisp . t)))

(find-file "README.org")
(org-blackfriday-export-to-markdown)
