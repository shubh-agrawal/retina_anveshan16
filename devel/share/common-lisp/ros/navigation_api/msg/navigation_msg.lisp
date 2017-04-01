; Auto-generated. Do not edit!


(cl:in-package navigation_api-msg)


;//! \htmlinclude navigation_msg.msg.html

(cl:defclass <navigation_msg> (roslisp-msg-protocol:ros-message)
  ((start_point
    :reader start_point
    :initarg :start_point
    :type cl:string
    :initform "")
   (destination
    :reader destination
    :initarg :destination
    :type cl:string
    :initform "")
   (current_address
    :reader current_address
    :initarg :current_address
    :type cl:string
    :initform "")
   (target_heading
    :reader target_heading
    :initarg :target_heading
    :type cl:float
    :initform 0.0)
   (start_crdnts
    :reader start_crdnts
    :initarg :start_crdnts
    :type cl:string
    :initform "")
   (target_crdnts
    :reader target_crdnts
    :initarg :target_crdnts
    :type cl:string
    :initform ""))
)

(cl:defclass navigation_msg (<navigation_msg>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <navigation_msg>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'navigation_msg)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name navigation_api-msg:<navigation_msg> is deprecated: use navigation_api-msg:navigation_msg instead.")))

(cl:ensure-generic-function 'start_point-val :lambda-list '(m))
(cl:defmethod start_point-val ((m <navigation_msg>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader navigation_api-msg:start_point-val is deprecated.  Use navigation_api-msg:start_point instead.")
  (start_point m))

(cl:ensure-generic-function 'destination-val :lambda-list '(m))
(cl:defmethod destination-val ((m <navigation_msg>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader navigation_api-msg:destination-val is deprecated.  Use navigation_api-msg:destination instead.")
  (destination m))

(cl:ensure-generic-function 'current_address-val :lambda-list '(m))
(cl:defmethod current_address-val ((m <navigation_msg>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader navigation_api-msg:current_address-val is deprecated.  Use navigation_api-msg:current_address instead.")
  (current_address m))

(cl:ensure-generic-function 'target_heading-val :lambda-list '(m))
(cl:defmethod target_heading-val ((m <navigation_msg>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader navigation_api-msg:target_heading-val is deprecated.  Use navigation_api-msg:target_heading instead.")
  (target_heading m))

(cl:ensure-generic-function 'start_crdnts-val :lambda-list '(m))
(cl:defmethod start_crdnts-val ((m <navigation_msg>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader navigation_api-msg:start_crdnts-val is deprecated.  Use navigation_api-msg:start_crdnts instead.")
  (start_crdnts m))

(cl:ensure-generic-function 'target_crdnts-val :lambda-list '(m))
(cl:defmethod target_crdnts-val ((m <navigation_msg>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader navigation_api-msg:target_crdnts-val is deprecated.  Use navigation_api-msg:target_crdnts instead.")
  (target_crdnts m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <navigation_msg>) ostream)
  "Serializes a message object of type '<navigation_msg>"
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'start_point))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'start_point))
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'destination))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'destination))
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'current_address))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'current_address))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'target_heading))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'start_crdnts))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'start_crdnts))
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'target_crdnts))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'target_crdnts))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <navigation_msg>) istream)
  "Deserializes a message object of type '<navigation_msg>"
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'start_point) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'start_point) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'destination) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'destination) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'current_address) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'current_address) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'target_heading) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'start_crdnts) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'start_crdnts) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'target_crdnts) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'target_crdnts) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<navigation_msg>)))
  "Returns string type for a message object of type '<navigation_msg>"
  "navigation_api/navigation_msg")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'navigation_msg)))
  "Returns string type for a message object of type 'navigation_msg"
  "navigation_api/navigation_msg")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<navigation_msg>)))
  "Returns md5sum for a message object of type '<navigation_msg>"
  "9a1c613c009062e1b0137332da96d004")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'navigation_msg)))
  "Returns md5sum for a message object of type 'navigation_msg"
  "9a1c613c009062e1b0137332da96d004")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<navigation_msg>)))
  "Returns full string definition for message of type '<navigation_msg>"
  (cl:format cl:nil "string start_point~%string destination~%string current_address~%float64 target_heading~%string start_crdnts ~%string target_crdnts~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'navigation_msg)))
  "Returns full string definition for message of type 'navigation_msg"
  (cl:format cl:nil "string start_point~%string destination~%string current_address~%float64 target_heading~%string start_crdnts ~%string target_crdnts~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <navigation_msg>))
  (cl:+ 0
     4 (cl:length (cl:slot-value msg 'start_point))
     4 (cl:length (cl:slot-value msg 'destination))
     4 (cl:length (cl:slot-value msg 'current_address))
     8
     4 (cl:length (cl:slot-value msg 'start_crdnts))
     4 (cl:length (cl:slot-value msg 'target_crdnts))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <navigation_msg>))
  "Converts a ROS message object to a list"
  (cl:list 'navigation_msg
    (cl:cons ':start_point (start_point msg))
    (cl:cons ':destination (destination msg))
    (cl:cons ':current_address (current_address msg))
    (cl:cons ':target_heading (target_heading msg))
    (cl:cons ':start_crdnts (start_crdnts msg))
    (cl:cons ':target_crdnts (target_crdnts msg))
))
