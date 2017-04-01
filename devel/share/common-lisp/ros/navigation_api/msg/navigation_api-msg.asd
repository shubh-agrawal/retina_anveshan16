
(cl:in-package :asdf)

(defsystem "navigation_api-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "navigation_msg" :depends-on ("_package_navigation_msg"))
    (:file "_package_navigation_msg" :depends-on ("_package"))
  ))