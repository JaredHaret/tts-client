import techmo_tts_pb2
import techmo_tts_pb2_grpc
import grpc
import os
from create_channel import create_channel
import lxml.etree as etree


def call_getlexicon(args):
    channel = create_channel(args.service, args.tls_directory)
    stub = techmo_tts_pb2_grpc.TTSStub(channel)

    timeout=None
    if args.grpc_timeout > 0:
        timeout = args.grpc_timeout / 1000
    metadata = []
    if args.session_id:
        metadata = [('session_id', args.session_id)]

    request = techmo_tts_pb2.GetLexiconRequest(name=args.lexicon_to_get)

    try:
        response = stub.GetLexicon(request, timeout=timeout, metadata=metadata)
        xml_parser = etree.XMLParser(remove_blank_text=True, recover=True)
        x = etree.fromstring(response.content, parser=xml_parser)
        print("\n---",args.lexicon_to_get,"---\n")
        print(etree.tostring(x, pretty_print=True).decode())
    except grpc.RpcError as e:
        print("[Server-side error] Received following RPC error from the TTS service:", str(e))
