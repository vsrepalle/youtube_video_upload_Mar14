"""
Video composition module - SPEED OPTIMIZED
"""
from moviepy import CompositeVideoClip, ColorClip, ImageClip
import numpy as np
import traceback

try:
    import config
    CONFIG_AVAILABLE = True
except:
    CONFIG_AVAILABLE = False

from .text import text_generator

class VideoCompositor:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        # Optimized defaults for TrendWave Now
        self.header_height = 120
        self.header_opacity = 0.7
        self.header_font_size = 65
        self.subtitle_font_size = 70
        self.subtitle_y = 1650
        self.end_screen_cta = "🔔 SUBSCRIBE FOR MORE!"

    def create_header(self, headline, duration):
        if not headline: return None
        try:
            # Background
            header_bg = ColorClip(
                size=(self.width, self.header_height),
                color=(0, 0, 0)
            ).set_opacity(self.header_opacity).set_duration(duration)
            
            # Headline - forced lowercase for your brand style
            headline_img = text_generator.create_text_image(
                headline.lower(), 
                font_size=self.header_font_size,
                color='white',
                max_width=self.width - 100
            )
            
            headline_clip = ImageClip(headline_img).with_position(('center', 30)).set_duration(duration)
            return CompositeVideoClip([header_bg, headline_clip], size=(self.width, self.height)).with_position("top")
        except:
            return None

    def create_subtitles(self, text, duration):
        """SPEED OPTIMIZED: Chunk-based subtitles (1 clip per 5 words)"""
        if not text: return []
        
        words = text.split()
        words_per_chunk = 5 
        chunks = [words[i:i + words_per_chunk] for i in range(0, len(words), words_per_chunk)]
        
        subtitle_clips = []
        chunk_duration = duration / max(1, len(chunks))

        for i, chunk in enumerate(chunks):
            chunk_text = " ".join(chunk).lower() # Forced lowercase
            
            sub_img = text_generator.create_text_image(
                chunk_text,
                font_size=self.subtitle_font_size,
                color='yellow',
                stroke_width=4,
                stroke_color='black',
                max_width=self.width - 100
            )
            
            sub_clip = ImageClip(sub_img).with_position(('center', self.subtitle_y))
            sub_clip = sub_clip.set_duration(chunk_duration).set_start(i * chunk_duration)
            subtitle_clips.append(sub_clip)
            
        return subtitle_clips

    def create_end_screen(self, total_duration):
        """Subscribe hook - strictly at the end"""
        try:
            end_duration = min(4.0, total_duration * 0.1)
            end_start = total_duration - end_duration
            
            overlay = ColorClip(size=(self.width, self.height), color=(0,0,0)).set_opacity(0.8).set_duration(end_duration).set_start(end_start)
            
            sub_img = text_generator.create_text_image(
                self.end_screen_cta.lower(),
                font_size=95,
                color='white',
                stroke_color='red'
            )
            
            text_clip = ImageClip(sub_img).with_position('center').set_duration(end_duration).set_start(end_start)
            return overlay, text_clip
        except:
            return None, None