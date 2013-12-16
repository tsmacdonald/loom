(in-package #:loom)

(defparameter *default-corpus* '("~/src/loom/corpus/marshall/William_Marshall.abc"
"~/src/loom/corpus/marshall/William_Marshall_A_Collection_of_Strathspey_Reels__1781.abc"
"~/src/loom/corpus/marshall/William_Marshall_Kinrara_1800.abc"
"~/src/loom/corpus/marshall/William_Marshalls_Scottish_Airs_Melodies_Strathspeys_Reels_c_1822.abc"
"~/src/loom/corpus/marshall/William_Marshalls_Scottish_Melodies_Reels_Strathspeys_volume_2nd_1845.abc"))

(defparameter *reels* (remove-if-not (lambda (tune-cons) (string-equal (cl-abc::tune-rhythm (car tune-cons)) "Reel")) *tunes*))

(defun read-and-preprocess (files)
  (mapcar #'extract-features (apply #'append (mapcar #'cl-abc::parse-file files))))

(defun extract-features (tune)
  (cons tune (mapcar #'note-to-int-pair (apply #'append (cl-abc::tune-melody tune)))))

(defun note-to-int-pair (note)
  "Returns a cons cell containing the pitch (as an integer) and the length (as a rational)"
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
	 (notes (cdr tune))
	 (sum 0))
      (with-open-file (out (concatenate 'string "~/src/loom/output/" (cl-ppcre:regex-replace-all "[^a-zA-Z0-9]+" (cl-abc::tune-title raw-tune) "_") ".csv")
			   :direction :output
			   :if-exists :supersede)
	(format out "~a~T~a~T~a" "Time" "Pitch" "Length")
	(dolist (note notes)
	  (format out "~&~A~T~a~T~a" (coerce sum 'float) (car note) (coerce (cdr note) 'float))
	  (incf sum (cdr note)))))))
      

(defun to-csv-time-pitch (tunes)
  (dolist (tune tunes)
    (let
	((raw-tune (car tune))
	 (notes (cdr tune))
	 (sum 0))
      (with-open-file (out (concatenate 'string "~/src/loom/output/" (cl-ppcre:regex-replace-all "[^a-zA-Z0-9]+" (cl-abc::tune-title raw-tune) "_") ".csv")
			   :direction :output
			   :if-exists :supersede)
;	(format out "~a~T~a" "Time" "Pitch")
	(dolist (note notes)
	  (format out "~&~A~T~a" (coerce sum 'float) (car note))
	  (incf sum (cdr note)))))))




(defun to-csv-1d (tunes)
  (dolist (tune tunes)
    (when tune
      (let
	  ((raw-tune (car tune))
	   (notes (cdr tune)))
	(with-open-file (out (concatenate 'string "~/src/loom/output/" (cl-ppcre:regex-replace-all "[^a-zA-Z0-9]+" (cl-abc::tune-title raw-tune) "_") "__l16_1d_reel_nopickup.csv")
			     :direction :output
			     :if-exists :supersede)
					;	(format out "~a~T~a" "Time" "Pitch")
	  (dolist (note notes)
	    (let*
		((pitch (- (car note) 38))
		 (length (cdr note))
		 (too-short (or (and (boundp 'too-short) too-short) (< length 1/16)))
		 (to-go (if (and (boundp 'too-short) (> to-go 0)) to-go 1/16))
		 (reps (/ length 1/16)))
	      (if too-short
		  (progn
		    (format out "~&~A" pitch)
		    (decf to-go length)
		    (if (<= to-go 0)
			(setf too-short nil)))
		  (dotimes (i reps)
		    (format out "~&~A" pitch))))))))))

(defun smallest-positive (x y)
  (if (zerop x)
      (if (zerop y)
	  10000000
	  y)
      (if (zerop y)
	  x
	  (min x y))))

(defun measure-length (measure)
  (apply #'+ (mapcar #'cl-abc::note-length measure)))

(defun pickupp (tune)
  (let ((measures (cl-abc::tune-melody tune)))
    (/= (measure-length (first measures)) (measure-length (second measures)))))

(defun remove-pickup (tune)
  (when (pickupp tune)
    (setf (cl-abc::tune-melody tune) (rest (cl-abc::tune-melody tune))))
  tune)