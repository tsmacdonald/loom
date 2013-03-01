;;;; loom.asd

(asdf:defsystem #:loom
  :serial t
  :description "Lisp's Output of Original Music, which frankly speaking could be colossal. A project to generate traditional Scottish music."
  :author "Tim Macdonald <tsmacdonald@gmail.com>"
  :license "GPLv3"
  :depends-on (#:cl-abc
               #:cl-ppcre)
  :components ((:file "package")
               (:file "loom")))

