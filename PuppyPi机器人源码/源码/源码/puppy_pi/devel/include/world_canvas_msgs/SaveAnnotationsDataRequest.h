// Generated by gencpp from file world_canvas_msgs/SaveAnnotationsDataRequest.msg
// DO NOT EDIT!


#ifndef WORLD_CANVAS_MSGS_MESSAGE_SAVEANNOTATIONSDATAREQUEST_H
#define WORLD_CANVAS_MSGS_MESSAGE_SAVEANNOTATIONSDATAREQUEST_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>

#include <world_canvas_msgs/Annotation.h>
#include <world_canvas_msgs/AnnotationData.h>

namespace world_canvas_msgs
{
template <class ContainerAllocator>
struct SaveAnnotationsDataRequest_
{
  typedef SaveAnnotationsDataRequest_<ContainerAllocator> Type;

  SaveAnnotationsDataRequest_()
    : annotations()
    , data()  {
    }
  SaveAnnotationsDataRequest_(const ContainerAllocator& _alloc)
    : annotations(_alloc)
    , data(_alloc)  {
  (void)_alloc;
    }



   typedef std::vector< ::world_canvas_msgs::Annotation_<ContainerAllocator> , typename ContainerAllocator::template rebind< ::world_canvas_msgs::Annotation_<ContainerAllocator> >::other >  _annotations_type;
  _annotations_type annotations;

   typedef std::vector< ::world_canvas_msgs::AnnotationData_<ContainerAllocator> , typename ContainerAllocator::template rebind< ::world_canvas_msgs::AnnotationData_<ContainerAllocator> >::other >  _data_type;
  _data_type data;





  typedef boost::shared_ptr< ::world_canvas_msgs::SaveAnnotationsDataRequest_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::world_canvas_msgs::SaveAnnotationsDataRequest_<ContainerAllocator> const> ConstPtr;

}; // struct SaveAnnotationsDataRequest_

typedef ::world_canvas_msgs::SaveAnnotationsDataRequest_<std::allocator<void> > SaveAnnotationsDataRequest;

typedef boost::shared_ptr< ::world_canvas_msgs::SaveAnnotationsDataRequest > SaveAnnotationsDataRequestPtr;
typedef boost::shared_ptr< ::world_canvas_msgs::SaveAnnotationsDataRequest const> SaveAnnotationsDataRequestConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::world_canvas_msgs::SaveAnnotationsDataRequest_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::world_canvas_msgs::SaveAnnotationsDataRequest_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::world_canvas_msgs::SaveAnnotationsDataRequest_<ContainerAllocator1> & lhs, const ::world_canvas_msgs::SaveAnnotationsDataRequest_<ContainerAllocator2> & rhs)
{
  return lhs.annotations == rhs.annotations &&
    lhs.data == rhs.data;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::world_canvas_msgs::SaveAnnotationsDataRequest_<ContainerAllocator1> & lhs, const ::world_canvas_msgs::SaveAnnotationsDataRequest_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace world_canvas_msgs

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsMessage< ::world_canvas_msgs::SaveAnnotationsDataRequest_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::world_canvas_msgs::SaveAnnotationsDataRequest_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::world_canvas_msgs::SaveAnnotationsDataRequest_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::world_canvas_msgs::SaveAnnotationsDataRequest_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::world_canvas_msgs::SaveAnnotationsDataRequest_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::world_canvas_msgs::SaveAnnotationsDataRequest_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::world_canvas_msgs::SaveAnnotationsDataRequest_<ContainerAllocator> >
{
  static const char* value()
  {
    return "d204dc5afba8bb6886ec4a83711f9c6e";
  }

  static const char* value(const ::world_canvas_msgs::SaveAnnotationsDataRequest_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0xd204dc5afba8bb68ULL;
  static const uint64_t static_value2 = 0x86ec4a83711f9c6eULL;
};

template<class ContainerAllocator>
struct DataType< ::world_canvas_msgs::SaveAnnotationsDataRequest_<ContainerAllocator> >
{
  static const char* value()
  {
    return "world_canvas_msgs/SaveAnnotationsDataRequest";
  }

  static const char* value(const ::world_canvas_msgs::SaveAnnotationsDataRequest_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::world_canvas_msgs::SaveAnnotationsDataRequest_<ContainerAllocator> >
{
  static const char* value()
  {
    return "# Utility service kept to make debug and testing easier:\n"
"#   saves together annotations and its data assuming a 1-1 relationship.\n"
"\n"
"Annotation[] annotations\n"
"AnnotationData[] data \n"
"\n"
"================================================================================\n"
"MSG: world_canvas_msgs/Annotation\n"
"# Annotation: a generic descriptor for an element (object) in a semantic map\n"
"# An annotation can be used to introspect, visualize or key into database filters/searches without\n"
"# having to touch the described object directly\n"
"#  - timestamp : Creation/last update time\n"
"#  - world     : World the object belongs to\n"
"#  - id        : Annotation unique id\n"
"#  - data_id   : Referenced object unique id (an object can be reference by 1 or more annotations)\n"
"#  - name      : Referenced object name\n"
"#  - type      : Referenced object type (a message type, as world canvas objects are ROS messages)\n"
"#  - shape     : One of 1 (CUBE), 2 (SPHERE), 3 (CYLINDER), 9 (TEXT)\n"
"#  - color     : R, G, B, A (optional)\n"
"#  - size      : X, Y, Z (optional)\n"
"#  - keywords  : Generic properties of this object: allows basic filtering without introspecting\n"
"#                the object itself\n"
"#  - relationships : List of associated annotations, used for retrieving operational sets of objects\n"
"\n"
"# General properties\n"
"time timestamp\n"
"uuid_msgs/UniqueID id\n"
"uuid_msgs/UniqueID data_id\n"
"string world\n"
"string name\n"
"string type\n"
"\n"
"# Physical properties\n"
"int32  shape\n"
"std_msgs/ColorRGBA color\n"
"geometry_msgs/Vector3 size\n"
"geometry_msgs/PoseWithCovarianceStamped pose\n"
"\n"
"# Querying properties\n"
"string[] keywords\n"
"uuid_msgs/UniqueID[] relationships\n"
"\n"
"================================================================================\n"
"MSG: uuid_msgs/UniqueID\n"
"# A universally unique identifier (UUID).\n"
"#\n"
"#  http://en.wikipedia.org/wiki/Universally_unique_identifier\n"
"#  http://tools.ietf.org/html/rfc4122.html\n"
"\n"
"uint8[16] uuid\n"
"\n"
"================================================================================\n"
"MSG: std_msgs/ColorRGBA\n"
"float32 r\n"
"float32 g\n"
"float32 b\n"
"float32 a\n"
"\n"
"================================================================================\n"
"MSG: geometry_msgs/Vector3\n"
"# This represents a vector in free space. \n"
"# It is only meant to represent a direction. Therefore, it does not\n"
"# make sense to apply a translation to it (e.g., when applying a \n"
"# generic rigid transformation to a Vector3, tf2 will only apply the\n"
"# rotation). If you want your data to be translatable too, use the\n"
"# geometry_msgs/Point message instead.\n"
"\n"
"float64 x\n"
"float64 y\n"
"float64 z\n"
"================================================================================\n"
"MSG: geometry_msgs/PoseWithCovarianceStamped\n"
"# This expresses an estimated pose with a reference coordinate frame and timestamp\n"
"\n"
"Header header\n"
"PoseWithCovariance pose\n"
"\n"
"================================================================================\n"
"MSG: std_msgs/Header\n"
"# Standard metadata for higher-level stamped data types.\n"
"# This is generally used to communicate timestamped data \n"
"# in a particular coordinate frame.\n"
"# \n"
"# sequence ID: consecutively increasing ID \n"
"uint32 seq\n"
"#Two-integer timestamp that is expressed as:\n"
"# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')\n"
"# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')\n"
"# time-handling sugar is provided by the client library\n"
"time stamp\n"
"#Frame this data is associated with\n"
"string frame_id\n"
"\n"
"================================================================================\n"
"MSG: geometry_msgs/PoseWithCovariance\n"
"# This represents a pose in free space with uncertainty.\n"
"\n"
"Pose pose\n"
"\n"
"# Row-major representation of the 6x6 covariance matrix\n"
"# The orientation parameters use a fixed-axis representation.\n"
"# In order, the parameters are:\n"
"# (x, y, z, rotation about X axis, rotation about Y axis, rotation about Z axis)\n"
"float64[36] covariance\n"
"\n"
"================================================================================\n"
"MSG: geometry_msgs/Pose\n"
"# A representation of pose in free space, composed of position and orientation. \n"
"Point position\n"
"Quaternion orientation\n"
"\n"
"================================================================================\n"
"MSG: geometry_msgs/Point\n"
"# This contains the position of a point in free space\n"
"float64 x\n"
"float64 y\n"
"float64 z\n"
"\n"
"================================================================================\n"
"MSG: geometry_msgs/Quaternion\n"
"# This represents an orientation in free space in quaternion form.\n"
"\n"
"float64 x\n"
"float64 y\n"
"float64 z\n"
"float64 w\n"
"\n"
"================================================================================\n"
"MSG: world_canvas_msgs/AnnotationData\n"
"# Data for an element in a semantic map stored as a byte array generated by ros::serialization\n"
"# These objects are unique, although they can be referenced by one or more annotations\n"
"#  - id   : Object unique id; data_id field on Annotation messages point to this uuid\n"
"#  - type : Object type; duplicated from annotation for convenience on deserialization\n"
"#  - data : Serialized data\n"
"uuid_msgs/UniqueID id\n"
"string type\n"
"uint8[] data\n"
;
  }

  static const char* value(const ::world_canvas_msgs::SaveAnnotationsDataRequest_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::world_canvas_msgs::SaveAnnotationsDataRequest_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.annotations);
      stream.next(m.data);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct SaveAnnotationsDataRequest_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::world_canvas_msgs::SaveAnnotationsDataRequest_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::world_canvas_msgs::SaveAnnotationsDataRequest_<ContainerAllocator>& v)
  {
    s << indent << "annotations[]" << std::endl;
    for (size_t i = 0; i < v.annotations.size(); ++i)
    {
      s << indent << "  annotations[" << i << "]: ";
      s << std::endl;
      s << indent;
      Printer< ::world_canvas_msgs::Annotation_<ContainerAllocator> >::stream(s, indent + "    ", v.annotations[i]);
    }
    s << indent << "data[]" << std::endl;
    for (size_t i = 0; i < v.data.size(); ++i)
    {
      s << indent << "  data[" << i << "]: ";
      s << std::endl;
      s << indent;
      Printer< ::world_canvas_msgs::AnnotationData_<ContainerAllocator> >::stream(s, indent + "    ", v.data[i]);
    }
  }
};

} // namespace message_operations
} // namespace ros

#endif // WORLD_CANVAS_MSGS_MESSAGE_SAVEANNOTATIONSDATAREQUEST_H
