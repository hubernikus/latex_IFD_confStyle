;; --------------------------------------------------------------
;;
;;       EMACS - Configuration file
;;        Source: /.emacs/init.el file for

;; INSTALL PACKAGES
;; --------------------------------------------------------------

;; To evaluate file:  Alt-C 'eval-buffer'



(require 'package)

(add-to-list 'package-archives
       '("melpa" . "http://melpa.org/packages/") t)

(package-initialize)
(when (not package-archive-contents)
  (package-refresh-contents))

(defvar myPackages
  '(better-defaults
    ein
    elpy
    flycheck
    material-theme
    py-autopep8
    writegood-mode
    ))

(mapc #'(lambda (package)
    (unless (package-installed-p package)
      (package-install package)))
      myPackages)

;; BASIC CUSTOMIZATION
;; --------------------------------------

(setq inhibit-startup-message t) ;; hide the startup message
;; Define color theme
(load-theme 'manoj-dark t) ;;  manoj-darkasdf
(global-linum-mode t) ;; enable line numbers globally


(global-unset-key (kbd "C-z"));; disable accidental freeze

(tool-bar-mode -1) ;; Hide toolbar

;;(setq prelude-whitespace 1) ;; show whitepsace
;;(add-hook 'prog-mode-hook 'prelude-turn-off-whitespace t)

;; (when (fboundp 'electric-indent-mode) (electric-indent-mode -1)) ;; no indent

(auto-fill-mode -1) ;; no line break

;; (add-hook 'text-mode-hook 'turn-off-auto-fill)

;;(remove-hook 'text-mode-hook 'turn-off-auto-fill)

;; Programming CUSTOMIZATION
;; --------------------------------------

;;; Shut up compile saves
(setq compilation-ask-about-save nil)
;;; Don't save *anything*
(setq compilation-save-buffers-predicate '(lambda () nil))


;; PYTHON CONFIGURATION
;; --------------------------------------

(elpy-enable)
(elpy-use-ipython)

;; use flycheck not flymake with elpy
(when (require 'flycheck nil t)
  (setq elpy-modules (delq 'elpy-module-flymake elpy-modules))
  (add-hook 'elpy-mode-hook 'flycheck-mode))

;; enable autopep8 formatting on save
(require 'py-autopep8)
(add-hook 'elpy-mode-hook 'py-autopep8-enable-on-save)
(require 'python)
(defun python--add-debug-highlight ()
  "Adds a highlighter for use by `python--pdb-breakpoint-string'"
  (highlight-lines-matching-regexp "## DEBUG ##\\s-*$" 'hi-red-b))

(add-hook 'python-mode-hook 'python--add-debug-highlight)

(defvar python--pdb-breakpoint-string "import pdb; pdb.set_trace() ## DEBUG ##"
  "Python breakpoint string used by `python-insert-breakpoint'")

(defun python-insert-breakpoint ()
  "Inserts a python breakpoint using `pdb'"
  (interactive)
  (back-to-indentation)
  ;; this preserves the correct indentation in case the line above
  ;; point is a nested block
  (split-line)
  (insert python--pdb-breakpoint-string))
(define-key python-mode-map (kbd "<f5>") 'python-insert-breakpoint)

(defadvice compile (before ad-compile-smart activate)
  "Advises `compile' so it sets the argument COMINT to t
if breakpoints are present in `python-mode' files"
  (when (derived-mode-p major-mode 'python-mode)
    (save-excursion
      (save-match-data
        (goto-char (point-min))
        (if (re-search-forward (concat "^\\s-*" python--pdb-breakpoint-string "$")
                               (point-max) t)
            ;; set COMINT argument to `t'.
            (ad-set-arg 1 t))))))

(setq python-shell-interpreter "ipython"
      python-shell-interpreter-args "-i")

;;; Python usage


;; LATEX CONFIGURATION
;; -------------------------------------------
(setq TeX-auto-save t)
(setq TeX-parse-self t)
(setq-default TeX-master nil)

(add-hook 'LaTeX-mode-hook 'visual-line-mode)
(add-hook 'LaTeX-mode-hook 'flyspell-mode)
(add-hook 'LaTeX-mode-hook 'LaTeX-math-mode)
(add-hook 'LaTeX-mode-hook 'TeX-source-correlate-mode)

(add-hook 'LaTeX-mode-hook 'turn-on-reftex)
(setq reftex-plug-into-AUCTeX t)
(setq TeX-PDF-mode t)

(setq TeX-output-view-style
    (quote
     (("^pdf$" "." "evince -f %o")
      ("^html?$" "." "iceweasel %o"))))

;; Setting up writegood-mode
(require 'writegood-mode)
(global-set-key "\C-cg" 'writegood-mode)


;; MATLAB CONFIGURATION
;; ------------------------------------------------------

;; (add-to-list 'load-path "~/.emacs.d/personal/matlab-emacs")
;; (load-library "matlab-load")
;; (custom-set-variables
;;  '(matlab-shell-command-switches '("-nodesktop -nosplash")))
;; (add-hook 'matlab-mode-hook 'auto-complete-mode)
;; (setq auto-mode-alist
;;     (cons
;;      '("\\.m$" . matlab-mode)
;;      auto-mode-alist))

;; init.el ends here
