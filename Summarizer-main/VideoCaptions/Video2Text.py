import speech_recognition as sr 
import moviepy.editor as mp

from moviepy.editor import VideoFileClip

class VideoCaptions:

  output_video_path = 'converted.mp4'
  result = ''

  def getVideosDuration(self,input_video_path):
    video = VideoFileClip(input_video_path)
    video_duration = int(video.duration)
    print(video_duration)
    return video_duration

  def getChunkCaption(self, input_video_path):
    input_video_path = input_video_path[0]
    i = 0
    while i < self.getVideosDuration(input_video_path):
        
        try:
          with VideoFileClip(input_video_path) as video:
            #First 10 seconds
            new = video.subclip(i, i+9)
            new.write_videofile(self.output_video_path, audio_codec='aac')
            i+=10
        except:
          break

        clip = mp.VideoFileClip(r"converted.mp4".format(i+1)) 
        clip.audio.write_audiofile(r"converted.wav".format(i+1))
        r = sr.Recognizer()
        audio = sr.AudioFile("converted.wav".format(i+1))
        with audio as source:
          r.adjust_for_ambient_noise(source)  
          audio_file = r.record(source)
        self.result += r.recognize_google(audio_file)+' '

        
  def WriteCaptionInFile(self):
    with open('recognized.txt', mode ='w') as file:
          file.write(self.result) 
          file.write("\n") 
          print("Finally ready!")
    return self.result