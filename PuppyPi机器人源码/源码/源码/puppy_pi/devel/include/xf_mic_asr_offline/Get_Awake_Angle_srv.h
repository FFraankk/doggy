// Generated by gencpp from file xf_mic_asr_offline/Get_Awake_Angle_srv.msg
// DO NOT EDIT!


#ifndef XF_MIC_ASR_OFFLINE_MESSAGE_GET_AWAKE_ANGLE_SRV_H
#define XF_MIC_ASR_OFFLINE_MESSAGE_GET_AWAKE_ANGLE_SRV_H

#include <ros/service_traits.h>


#include <xf_mic_asr_offline/Get_Awake_Angle_srvRequest.h>
#include <xf_mic_asr_offline/Get_Awake_Angle_srvResponse.h>


namespace xf_mic_asr_offline
{

struct Get_Awake_Angle_srv
{

typedef Get_Awake_Angle_srvRequest Request;
typedef Get_Awake_Angle_srvResponse Response;
Request request;
Response response;

typedef Request RequestType;
typedef Response ResponseType;

}; // struct Get_Awake_Angle_srv
} // namespace xf_mic_asr_offline


namespace ros
{
namespace service_traits
{


template<>
struct MD5Sum< ::xf_mic_asr_offline::Get_Awake_Angle_srv > {
  static const char* value()
  {
    return "e9e10e1054cdfc6d195484df5648e04e";
  }

  static const char* value(const ::xf_mic_asr_offline::Get_Awake_Angle_srv&) { return value(); }
};

template<>
struct DataType< ::xf_mic_asr_offline::Get_Awake_Angle_srv > {
  static const char* value()
  {
    return "xf_mic_asr_offline/Get_Awake_Angle_srv";
  }

  static const char* value(const ::xf_mic_asr_offline::Get_Awake_Angle_srv&) { return value(); }
};


// service_traits::MD5Sum< ::xf_mic_asr_offline::Get_Awake_Angle_srvRequest> should match
// service_traits::MD5Sum< ::xf_mic_asr_offline::Get_Awake_Angle_srv >
template<>
struct MD5Sum< ::xf_mic_asr_offline::Get_Awake_Angle_srvRequest>
{
  static const char* value()
  {
    return MD5Sum< ::xf_mic_asr_offline::Get_Awake_Angle_srv >::value();
  }
  static const char* value(const ::xf_mic_asr_offline::Get_Awake_Angle_srvRequest&)
  {
    return value();
  }
};

// service_traits::DataType< ::xf_mic_asr_offline::Get_Awake_Angle_srvRequest> should match
// service_traits::DataType< ::xf_mic_asr_offline::Get_Awake_Angle_srv >
template<>
struct DataType< ::xf_mic_asr_offline::Get_Awake_Angle_srvRequest>
{
  static const char* value()
  {
    return DataType< ::xf_mic_asr_offline::Get_Awake_Angle_srv >::value();
  }
  static const char* value(const ::xf_mic_asr_offline::Get_Awake_Angle_srvRequest&)
  {
    return value();
  }
};

// service_traits::MD5Sum< ::xf_mic_asr_offline::Get_Awake_Angle_srvResponse> should match
// service_traits::MD5Sum< ::xf_mic_asr_offline::Get_Awake_Angle_srv >
template<>
struct MD5Sum< ::xf_mic_asr_offline::Get_Awake_Angle_srvResponse>
{
  static const char* value()
  {
    return MD5Sum< ::xf_mic_asr_offline::Get_Awake_Angle_srv >::value();
  }
  static const char* value(const ::xf_mic_asr_offline::Get_Awake_Angle_srvResponse&)
  {
    return value();
  }
};

// service_traits::DataType< ::xf_mic_asr_offline::Get_Awake_Angle_srvResponse> should match
// service_traits::DataType< ::xf_mic_asr_offline::Get_Awake_Angle_srv >
template<>
struct DataType< ::xf_mic_asr_offline::Get_Awake_Angle_srvResponse>
{
  static const char* value()
  {
    return DataType< ::xf_mic_asr_offline::Get_Awake_Angle_srv >::value();
  }
  static const char* value(const ::xf_mic_asr_offline::Get_Awake_Angle_srvResponse&)
  {
    return value();
  }
};

} // namespace service_traits
} // namespace ros

#endif // XF_MIC_ASR_OFFLINE_MESSAGE_GET_AWAKE_ANGLE_SRV_H
