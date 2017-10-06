from naoqi import ALProxy

ip_addr = "192.168.0.107"
port = 9559

from naoqi import ALProxy
motion = ALProxy("ALMotion", ip_addr, port)
tts    = ALProxy("ALTextToSpeech", ip_addr, port)
motion.moveInit()
motion.post.moveTo(0.5, 0, 0)
tts.say("I'm walking")