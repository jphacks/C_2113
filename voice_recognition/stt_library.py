# This code is baosically copied from https://cloud.google.com/speech-to-text/docs/streaming-recognize?hl=ja#speech-streaming-mic-recognize-python

from __future__ import division

import re

from google.cloud import speech

from googles_code import MicrophoneStream
import queue

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

def listen_print_loop(responses, output_queue: queue.Queue):
    """Iterates through server responses and prints them.

    The responses passed is a generator that will block until a response
    is provided by the server.

    Each response may contain multiple results, and each result may contain
    multiple alternatives; for details, see https://goo.gl/tjCPAU.  Here we
    print only the transcription for the top alternative of the top result.

    In this case, responses are provided for interim results as well. If the
    response is an interim one, print a line feed at the end of it, to allow
    the next result to overwrite it, until the response is a final one. For the
    final one, print a newline to preserve the finalized transcription.
    """
    num_chars_printed = 0
    for response in responses:
        if not response.results:
            continue

        # The `results` list is consecutive. For streaming, we only care about
        # the first result being considered, since once it's `is_final`, it
        # moves on to considering the next utterance.
        result = response.results[0]
        if not result.alternatives:
            continue

        # Display the transcription of the top alternative.

        transcript = result.alternatives[0].transcript

        # Display interim results, but with a carriage return at the end of the
        # line, so subsequent lines will overwrite them.
        #
        # If the previous result was longer than this one, we need to print
        # some extra spaces to overwrite the previous result
        # overwrite_chars = " " * (num_chars_printed - len(transcript))

        if (output_queue is not None):
            output_queue.put(result)
        if not result.is_final:
            #  stdout には出力しない
            # sys.stdout.write(transcript + overwrite_chars + "\r")
            # sys.stdout.flush()

            num_chars_printed = len(transcript)

        else:
            # print(transcript + overwrite_chars)

            # Exit recognition if any of the transcribed phrases could be
            # one of our keywords.
            if re.search(r"\b(認識終了)\b", transcript, re.I):
                print("Exiting..")
                break

            num_chars_printed = 0

def stt_main(output_queue: queue.Queue = None):
    # See http://g.co/cloud/speech/docs/languages
    # for a list of supported languages.
    language_code = "ja-JP"  # a BCP-47 language tag

    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code,
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )

    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (
            speech.StreamingRecognizeRequest(audio_content=content)
            for content in audio_generator
        )

        responses = client.streaming_recognize(streaming_config, requests)

        # Now, put the transcription responses to use.
        listen_print_loop(responses, output_queue)

if __name__ == "__main__":
    stt_main()
