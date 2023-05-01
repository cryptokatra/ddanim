import streamlit as st
from PIL import Image
import moviepy.editor as mp
import cv2

def convert_to_2d_style(video_path):
    # 用 moviepy 獲取影片並轉為幀影像
    clip = mp.VideoFileClip(video_path)
    frames = clip.iter_frames()
    
    # 定義 2D 風格轉換函數
    def cartoonize(image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 5)
        edges = cv2.Laplacian(gray, cv2.CV_8U, ksize=5)
        ret, mask = cv2.threshold(edges, 100, 255, cv2.THRESH_BINARY_INV)
        return cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    # 逐幀進行轉換
    frames_out = []
    for frame in frames:
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        frame_out = cartoonize(frame)
        frames_out.append(frame_out)

    # 將幀影像轉為影片並儲存
    out_clip = mp.ImageSequenceClip(frames_out, fps=clip.fps)
    out_clip.write_videofile("output_2d_style.mp4")

def convert_to_3d_style(video_path):
    # 用 moviepy 獲取影片並轉為幀影像
    clip = mp.VideoFileClip(video_path)
    frames = clip.iter_frames()
    
    # 定義 3D 風格轉換函數
    def stylize(image):
        return cv2.stylization(image, sigma_s=60, sigma_r=0.6)

    # 逐幀進行轉換
    frames_out = []
    for frame in frames:
        frame_out = stylize(frame)
        frames_out.append(frame_out)

    # 將幀影像轉為影片並儲存
    out_clip = mp.ImageSequenceClip(frames_out, fps=clip.fps)
    out_clip.write_videofile("output_3d_style.mp4")

def convert_to_cartoon_style(video_path):
    # 用 moviepy 獲取影片並轉為幀影像
    clip = mp.VideoFileClip(video_path)
    frames = clip.iter_frames()
    
    # 定義漫畫風格轉換函數
    def cartoonize(image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 3)
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 2)
        color = cv2.bilateralFilter(image, 7, 250, 250)
        return cv2.bitwise_and(color, color, mask=edges)

    # 逐幀進行轉換
    frames_out = []
    for frame in frames:
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        frame_out = cartoonize(frame)
        frames_out.append(frame_out)

    # 將幀影像轉為影片並儲存
    out_clip = mp.ImageSequenceClip(frames_out, fps=clip.fps)
    out_clip.write_videofile("output_cartoon_style.mp4")

# 界面設置
st.title("影片風格轉換")
video_path = st.file_uploader("請選擇影片檔案：")

# 風格選擇
style = st.radio("請選擇風格：", ("2D動畫風格", "3D動畫風格", "漫畫風格"))

# 轉換按鈕
if st.button("生成新影片"):
    if video_path is not None:
        # 根據風格選擇進行轉換
        if style == "2D動畫風格":
            convert_to_2d_style(video_path.name)
        elif style == "3D動畫風格":
            convert_to_3d_style(video_path.name)
        elif style == "漫畫風格":
            convert_to_cartoon_style(video_path.name)
        st.success("已生成新影片！")
    else:
        st.warning("請選擇影片檔案！")