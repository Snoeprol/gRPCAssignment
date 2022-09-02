# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: dronecommander.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x14\x64ronecommander.proto\x12\x0c\x64ronecommand\"\x1f\n\x0fRegisterRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\"\x1b\n\rRegisterReply\x12\n\n\x02id\x18\x01 \x01(\x05\"#\n\x15ListenWaypointRequest\x12\n\n\x02id\x18\x01 \x01(\x05\"?\n\x13ListenWaypointReply\x12(\n\x08waypoint\x18\x01 \x01(\x0b\x32\x16.dronecommand.Waypoint\"K\n\x13SendpositionRequest\x12(\n\x08position\x18\x01 \x01(\x0b\x32\x16.dronecommand.Position\x12\n\n\x02id\x18\x02 \x01(\x05\"\x13\n\x11SendpositionReply\"$\n\x08Waypoint\x12\x0b\n\x03lat\x18\x01 \x01(\x02\x12\x0b\n\x03lon\x18\x02 \x01(\x02\"1\n\x08Position\x12\x0b\n\x03lat\x18\x01 \x01(\x02\x12\x0b\n\x03lon\x18\x02 \x01(\x02\x12\x0b\n\x03\x61lt\x18\x03 \x01(\x02\x32\x90\x02\n\x0e\x44roneCommander\x12H\n\x08register\x12\x1d.dronecommand.RegisterRequest\x1a\x1b.dronecommand.RegisterReply\"\x00\x12]\n\x0flisten_waypoint\x12#.dronecommand.ListenWaypointRequest\x1a!.dronecommand.ListenWaypointReply\"\x00\x30\x01\x12U\n\rsend_position\x12!.dronecommand.SendpositionRequest\x1a\x1f.dronecommand.SendpositionReply\"\x00\x62\x06proto3')



_REGISTERREQUEST = DESCRIPTOR.message_types_by_name['RegisterRequest']
_REGISTERREPLY = DESCRIPTOR.message_types_by_name['RegisterReply']
_LISTENWAYPOINTREQUEST = DESCRIPTOR.message_types_by_name['ListenWaypointRequest']
_LISTENWAYPOINTREPLY = DESCRIPTOR.message_types_by_name['ListenWaypointReply']
_SENDPOSITIONREQUEST = DESCRIPTOR.message_types_by_name['SendpositionRequest']
_SENDPOSITIONREPLY = DESCRIPTOR.message_types_by_name['SendpositionReply']
_WAYPOINT = DESCRIPTOR.message_types_by_name['Waypoint']
_POSITION = DESCRIPTOR.message_types_by_name['Position']
RegisterRequest = _reflection.GeneratedProtocolMessageType('RegisterRequest', (_message.Message,), {
  'DESCRIPTOR' : _REGISTERREQUEST,
  '__module__' : 'dronecommander_pb2'
  # @@protoc_insertion_point(class_scope:dronecommand.RegisterRequest)
  })
_sym_db.RegisterMessage(RegisterRequest)

RegisterReply = _reflection.GeneratedProtocolMessageType('RegisterReply', (_message.Message,), {
  'DESCRIPTOR' : _REGISTERREPLY,
  '__module__' : 'dronecommander_pb2'
  # @@protoc_insertion_point(class_scope:dronecommand.RegisterReply)
  })
_sym_db.RegisterMessage(RegisterReply)

ListenWaypointRequest = _reflection.GeneratedProtocolMessageType('ListenWaypointRequest', (_message.Message,), {
  'DESCRIPTOR' : _LISTENWAYPOINTREQUEST,
  '__module__' : 'dronecommander_pb2'
  # @@protoc_insertion_point(class_scope:dronecommand.ListenWaypointRequest)
  })
_sym_db.RegisterMessage(ListenWaypointRequest)

ListenWaypointReply = _reflection.GeneratedProtocolMessageType('ListenWaypointReply', (_message.Message,), {
  'DESCRIPTOR' : _LISTENWAYPOINTREPLY,
  '__module__' : 'dronecommander_pb2'
  # @@protoc_insertion_point(class_scope:dronecommand.ListenWaypointReply)
  })
_sym_db.RegisterMessage(ListenWaypointReply)

SendpositionRequest = _reflection.GeneratedProtocolMessageType('SendpositionRequest', (_message.Message,), {
  'DESCRIPTOR' : _SENDPOSITIONREQUEST,
  '__module__' : 'dronecommander_pb2'
  # @@protoc_insertion_point(class_scope:dronecommand.SendpositionRequest)
  })
_sym_db.RegisterMessage(SendpositionRequest)

SendpositionReply = _reflection.GeneratedProtocolMessageType('SendpositionReply', (_message.Message,), {
  'DESCRIPTOR' : _SENDPOSITIONREPLY,
  '__module__' : 'dronecommander_pb2'
  # @@protoc_insertion_point(class_scope:dronecommand.SendpositionReply)
  })
_sym_db.RegisterMessage(SendpositionReply)

Waypoint = _reflection.GeneratedProtocolMessageType('Waypoint', (_message.Message,), {
  'DESCRIPTOR' : _WAYPOINT,
  '__module__' : 'dronecommander_pb2'
  # @@protoc_insertion_point(class_scope:dronecommand.Waypoint)
  })
_sym_db.RegisterMessage(Waypoint)

Position = _reflection.GeneratedProtocolMessageType('Position', (_message.Message,), {
  'DESCRIPTOR' : _POSITION,
  '__module__' : 'dronecommander_pb2'
  # @@protoc_insertion_point(class_scope:dronecommand.Position)
  })
_sym_db.RegisterMessage(Position)

_DRONECOMMANDER = DESCRIPTOR.services_by_name['DroneCommander']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _REGISTERREQUEST._serialized_start=38
  _REGISTERREQUEST._serialized_end=69
  _REGISTERREPLY._serialized_start=71
  _REGISTERREPLY._serialized_end=98
  _LISTENWAYPOINTREQUEST._serialized_start=100
  _LISTENWAYPOINTREQUEST._serialized_end=135
  _LISTENWAYPOINTREPLY._serialized_start=137
  _LISTENWAYPOINTREPLY._serialized_end=200
  _SENDPOSITIONREQUEST._serialized_start=202
  _SENDPOSITIONREQUEST._serialized_end=277
  _SENDPOSITIONREPLY._serialized_start=279
  _SENDPOSITIONREPLY._serialized_end=298
  _WAYPOINT._serialized_start=300
  _WAYPOINT._serialized_end=336
  _POSITION._serialized_start=338
  _POSITION._serialized_end=387
  _DRONECOMMANDER._serialized_start=390
  _DRONECOMMANDER._serialized_end=662
# @@protoc_insertion_point(module_scope)
