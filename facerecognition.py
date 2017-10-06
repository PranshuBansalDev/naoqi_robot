#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: A Simple class to get & read FaceDetected Events"""

import argparse
import sys
import time

import qi

IP_ADDR = "192.168.0.107"
PORT = 9559

class HumanGreeter(object):
    """
    A simple class to react to face detection events.
    """

    def __init__(self, app):
        """
        Initialisation of qi framework and event detection.
        """
        super(HumanGreeter, self).__init__()
        app.start()
        session = app.session
        
        # Get the service ALMemory.
        self.memory = session.service("ALMemory")
        self.speech_to_text = session.service("ALSpeechRecognition")
        self.tts = session.service("ALTextToSpeech")
        self.face_detection = session.service("ALFaceDetection")

        # init asr_service
        self.speech_to_text.pause(True)
        self.speech_to_text.setLanguage("English")
        self.vocab = ["yes", "no", "please"]
        self.speech_to_text.setVocabulary(self.vocab, False)

        # Add subscription for face detection
        self.face_subscriber = self.memory.subscriber("FaceDetected")
        self.face_subscriber.signal.connect(self.on_human_tracked)
        self.got_face = False
        self.last_face_detected = 0

        # Add subscription for speech detection
        self.speech_subscriber = self.memory.subscriber("WordRecognized")
        self.speech_subscriber.signal.connect(self.on_word_recognized)
        self.got_word = False
        self.last_word_detected = 0

        # Subscribe to the face_detection
        self.face_detection.subscribe("HumanGreeter")
        self.speech_to_text.pause(False)

    def on_word_recognized(self, value):
        print value
        if value[1] > 0.5:
            self.tts.say("You just said {}".format(value[0]))
        # if value == []:
        #    self.got_word = False
        #elif not self.got_word:
        #    self.got_word = True
        #    self.last_word_detected = time.time()
        #    print value

    def on_human_tracked(self, value):
        """
        Callback for event FaceDetected.
        """
        if value == []:  # empty value when the face disappears
            self.got_face = False
        elif not self.got_face and (time.time() - self.last_face_detected >= 10):  # only speak the first time a face appears
            self.got_face = True
            print "I saw a face!"
            self.tts.say("Hello, you!")
            self.last_face_detected = time.time()
            """
            # First Field = TimeStamp.
            timeStamp = value[0]
            print "TimeStamp is: " + str(timeStamp)

            # Second Field = array of face_Info's.
            face_info_array = value[1]
            for j in range(len(face_info_array) - 1):
                face_info = face_info_array[j]

                # First Field = Shape info.
                face_shape_info = face_info[0]

                # Second Field = Extra info (empty for now).
                face_extra_info = face_info[1]

                print "Face Infos :  alpha %.3f - beta %.3f" % (face_shape_info[1], face_shape_info[2])
                print "Face Infos :  width %.3f - height %.3f" % (face_shape_info[3], face_shape_info[4])
                print "Face Extra Infos :" + str(face_extra_info)
        """

    def run(self):
        """
        Loop on, wait for events until manual interruption.
        """
        print "Starting HumanGreeter"
        try:
            while True:
                time.sleep(1)
                
        except KeyboardInterrupt:
            print "Interrupted by user, stopping HumanGreeter"
            self.face_detection.unsubscribe("HumanGreeter")
            #stop
            sys.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default=IP_ADDR,
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=PORT,
                        help="Naoqi port number")

    args = parser.parse_args()
    try:
        # Initialize qi framework.
        connection_url = "tcp://" + args.ip + ":" + str(args.port)
        app = qi.Application(["HumanGreeter", "--qi-url=" + connection_url])
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    human_greeter = HumanGreeter(app)
    human_greeter.run()
