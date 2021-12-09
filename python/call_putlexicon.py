import techmo_tts_pb2
import techmo_tts_pb2_grpc
import grpc
import os
from create_channel import create_channel

def call_putlexicon(args):
    channel = create_channel(args.service, args.tls_directory)
    stub = techmo_tts_pb2_grpc.TTSStub(channel)

    timeout=None
    if args.grpc_timeout > 0:
        timeout = args.grpc_timeout / 1000
    metadata = []
    if args.session_id:
        metadata = [('session_id', args.session_id)]

    request = techmo_tts_pb2.PutLexiconRequest(name=args.put_lexicon[0],content=args.put_lexicon[1])

    try:       
        stub.PutLexicon(request, timeout=timeout, metadata=metadata)
        print("\nLexicon: ",args.put_lexicon[0]," has been added\n")
       
    except grpc.RpcError as e:
        print("[Server-side error] Received following RPC error from the TTS service:", str(e))
