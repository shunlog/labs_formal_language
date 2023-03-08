;;; config.el --- Description -*- lexical-binding: t; -*-
;;
;; Copyright (C) 2022 Artiom Balan
;;
;; Author: Artiom Balan <artiombalan331@gmail.com>
;; Maintainer: Artiom Balan <artiombalan331@gmail.com>
;; Created: March 12, 2022
;; Modified: March 12, 2022
;; Version: 0.0.1
;; Keywords: abbrev bib c calendar comm convenience data docs emulations extensions faces files frames games hardware help hypermedia i18n internal languages lisp local maint mail matching mouse multimedia news outlines processes terminals tex tools unix vc wp
;; Homepage: https://github.com/awh/config
;; Package-Requires: ((emacs "24.3"))
;;
;; This file is not part of GNU Emacs.
;;
;;; Commentary:
;;
;;  Description
;;
;;; Code:


(setq
 org-latex-listings 'minted
 org-latex-compiler "xelatex"
 org-confirm-babel-evaluate 'nil
 org-src-preserve-indentation 't)

(require 'ob)
(org-babel-do-load-languages
 'org-babel-load-languages
 '((octave . t) (python . t)(emacs-lisp . t)))

(provide 'config)
;;; config.el ends here
