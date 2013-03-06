(in-package #:loom)

(defun read-and-preprocess (files)
  (mapcar #'extract-features (apply #'append (mapcar #'cl-abc::parse-file files))))

(defun extract-features (tune)
  (cons tune (mapcar #'note-to-int-pair (apply #'append (cl-abc::tune-melody tune)))))

(defun note-to-int-pair (note)
  (let
      ((pitch (cl-abc::note-pitch note)))
    (cons
     (+
      (* 12 (cl-abc::pitch-octave (cl-abc::note-pitch note)))
      (case (character (symbol-name (cl-abc::pitch-value pitch)))
	(#\C 0)
	(#\D 2)
	(#\E 4)
	(#\F 5)
	(#\G 7)
	(#\A 9)
	(#\B 11)
	(otherwise 0))
      (case (character (symbol-name (cl-abc::pitch-accidental pitch)))
	(#\F -1)
	(#\N 0)
	(#\S 1)
	(otherwise 0)))
     (cl-abc::note-length note))))

(defun to-csv (tunes)
  (dolist (tune tunes)
    (let
	((raw-tune (car tune))
	 (notes (cdr tune)))
      (with-open-file (out (concatenate 'string "~/src/loom/output/" (cl-ppcre:regex-replace-all "\\s+" (cl-abc::tune-title raw-tune) "_") ".csv")
			   :direction :output
			   :if-exists :supersede)
	(dolist (note notes)
	  (format out "~&~a~T~a" (car note) (cdr note)))))))
      