from argparse import ArgumentParser
import codecs
from VERSION import TTS_CLIENT_VERSION
from call_listvoices import call_listvoices
from call_listlexicons import call_listlexicons
from call_getlexicon import call_getlexicon
from call_deletelexicon import call_deletelexicon
from call_putlexicon import call_putlexicon

from call_synthesize import call_synthesize


def main():
    print("Techmo TTS gRPC client " + TTS_CLIENT_VERSION)

    parser = ArgumentParser()
    parser.add_argument("-s", "--service-address", dest="service", required=True,
        help="An IP address and port (address:port) of a service the client connects to.", type=str)
    parser.add_argument("--session-id", dest="session_id", default="",
        help="A session ID to be passed to the service. If not specified, the service generates a default session ID.", type=str)
    parser.add_argument("--grpc-timeout", dest="grpc_timeout", default=0,
        help="A timeout in milliseconds used to set gRPC deadline - how long the client is willing to wait for a reply from the server (optional).", type=int)
    parser.add_argument("--list-voices", dest="list_voices", action='store_true', default=False,
        help="Lists all available voices.")
    parser.add_argument("-r", "--response", dest="response", default="streaming",
        help="streaming or single, calls the streaming (default) or non-streaming version of Synthesize.", type=str)
    parser.add_argument("-t", "--text", dest="text", default="Polski tekst do syntezy",
        help="A text to be synthesized.", type=str)
    parser.add_argument("-i", "--input-text-file", dest="inputfile", default="",
        help="A file with text to be synthesized.", type=str)
    parser.add_argument("-o", "--out-path", dest="out_path", default="",
        help="A path to the output wave file with synthesized audio content.", type=str)
    parser.add_argument("-f", "--sample-rate", dest="sample_rate", default=0,
        help="A sample rate in Hz of synthesized audio. Set to 0 (default) to use voice's original sample rate.", type=int)
    parser.add_argument("--ae", "--audio-encoding", dest="audio_encoding", default="pcm16",
        help="An encoding of the output audio, pcm16 (default) or ogg-vorbis.", type=str)
    parser.add_argument("--sp", "--speech-pitch", dest="speech_pitch", default=1.0,
        help="Allows adjusting the default pitch of the synthesized speech (optional, can be overriden by SSML).", type=float)
    parser.add_argument("--sr", "--speech-range", dest="speech_range", default=1.0,
        help="Allows adjusting the default range of the synthesized speech (optional, can be overriden by SSML).", type=float)
    parser.add_argument("--ss", "--speech-rate", dest="speech_rate", default=1.0,
        help="Allows adjusting the default rate (speed) of the synthesized speech (optional, can be overriden by SSML).", type=float)
    parser.add_argument("--sv", "--speech-volume", dest="speech_volume", default=1.0,
        help="Allows adjusting the default volume of the synthesized speech (optional, can be overriden by SSML).", type=float)
    parser.add_argument("--vn", "--voice-name", dest="voice_name", default="",
        help="A name od the voice used to synthesize the phrase (optional, can be overriden by SSML).", type=str)
    parser.add_argument("--vg", "--voice-gender", dest="voice_gender", default="",
        help="A gender of the voice - female or male (optional, can be overriden by SSML).", type=str)
    parser.add_argument("--va", "--voice-age", dest="voice_age", default="",
        help="An age of the voice - adult, child, or senile (optional, can be overriden by SSML).", type=str)
    parser.add_argument("-l", "--language", dest="language", default="",
        help="ISO 639-1 language code of the phrase to synthesize (optional, can be overriden by SSML).", type=str)
    parser.add_argument("--play", dest="play", default=False, action="store_true",
        help="Play synthesized audio. Works only with pcm16 (default) encoding.")
    parser.add_argument("--tls-dir", dest="tls_directory", default="",
        help="If set to a path with SSL/TLS credential files (client.crt, client.key, ca.crt), use SSL/TLS authentication. Otherwise use insecure channel (default).", type=str)
    parser.add_argument("--list-lexicons", dest="list_lexicons", action='store_true', default=False,
        help="Lists all available lexicons.")
    parser.add_argument("--get-lexicon", dest="lexicon_to_get", default="",
        help="Sends back the content of the lexicon with the requested name.", type=str)
    parser.add_argument("--delete-lexicon", dest="lexicon_to_delete", default="",
        help="Removes the lexicon with the requested name.", type=str)
    parser.add_argument("--put-lexicon", nargs=2, metavar=("LEXICON_TO_PUT", "LEXICON_CONTENT"),
        help="Adds a new lexicon with the requested name or overwrites the existing one if there is already a lexicon with such name. Content of the lexicon, shall comply to https://www.w3.org/TR/pronunciation-lexicon/.", type=str)

    # Parse and validate options
    args = parser.parse_args()

    # Check if service address and port are provided
    if len(args.service) == 0:
        raise RuntimeError("No service address and port provided.")

    if args.list_voices:
        call_listvoices(args)
        return
    
    if args.list_lexicons:
        call_listlexicons(args)
        return
    
    if (args.lexicon_to_get != ""):
        call_getlexicon(args)
        return

    if (args.lexicon_to_delete != ""):
        call_deletelexicon(args)
        return
    
    if (args.put_lexicon[0] != ""):
        call_putlexicon(args)
        return

    # Input text determination
    input_text = ""
    if len(args.inputfile) > 0:
        with codecs.open(args.inputfile, encoding='utf-8', mode="r") as fread:
            input_text = fread.read()
    elif len(args.text) > 0:
        input_text = args.text
    else:
        raise RuntimeError("Empty input string for synthesis.")

    call_synthesize(args, input_text)


if __name__ == '__main__':
    main()
