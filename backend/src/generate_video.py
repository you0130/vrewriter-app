
import os
import requests
import ffmpeg
from generate_script import generate_script
from generate_audio import generate_audio
from search_images import search_images

def download_image(url: str, filename: str):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(filename, 'wb') as out_file:
        for chunk in response.iter_content(chunk_size=8192):
            out_file.write(chunk)
    print(f"Downloaded image: {filename}")

def generate_video_from_text(input_text: str, output_path: str = "output_video.mp4"):
    # 1. 台本生成
    print("Generating script...")
    script_lines = generate_script(input_text)
    if not script_lines:
        print("No script lines generated. Aborting video generation.")
        return

    # 2. 各行の音声と画像を生成・ダウンロード
    video_inputs = []
    audio_files = []
    image_files = []
    temp_dir = "./temp_assets"
    os.makedirs(temp_dir, exist_ok=True)

    for i, line in enumerate(script_lines):
        # 音声生成
        audio_filename = os.path.join(temp_dir, f"audio_{i}.mp3")
        generate_audio(line, audio_filename)
        audio_files.append(audio_filename)

        # 音声ファイルの長さを取得
        probe = ffmpeg.probe(audio_filename)
        duration = float(probe["format"]["duration"])

        # 画像検索・ダウンロード
        image_filename = os.path.join(temp_dir, f"image_{i}.jpg")
        try:
            image_urls = search_images(line, per_page=1)
            if image_urls:
                download_image(image_urls[0], image_filename)
                image_files.append(image_filename)
            else:
                print(f"No image found for line: {line}. Using placeholder.")
                # TODO: Placeholder image
                image_files.append("placeholder.jpg") # 仮のプレースホルダー
        except Exception as e:
            print(f"Error searching/downloading image for '{line}': {e}. Using placeholder.")
            # TODO: Placeholder image
            image_files.append("placeholder.jpg") # 仮のプレースホルダー

        video_inputs.append({"image": image_files[-1], "audio": audio_files[-1], "duration": duration, "text": line})

    # 3. FFmpegで動画を結合
    print("Combining video and audio with FFmpeg...")
    input_streams = []
    filter_complex = []
    audio_streams = []
    video_streams = []

    for i, item in enumerate(video_inputs):
        img_input = ffmpeg.input(item["image"], loop=1, t=item["duration"])
        aud_input = ffmpeg.input(item["audio"])

        # テロップの追加 (ニュース風スタイル)
        # 字幕の長さに応じてフォントサイズを調整し、複数行表示に対応
        text = item["text"]
        
        # 文字数に応じてフォントサイズを調整
        text_length = len(text)
        if text_length <= 20:
            fontsize = 48
        elif text_length <= 30:
            fontsize = 40
        elif text_length <= 40:
            fontsize = 36
        else:
            fontsize = 32
        
        # 長いテキストは自動的に改行
        if text_length > 25:
            # 25文字ごとに改行を挿入
            words = text
            lines = []
            while len(words) > 25:
                # 適切な区切り位置を探す
                break_pos = 25
                for i in range(24, 19, -1):  # 20-25文字の範囲で区切り位置を探す
                    if i < len(words) and words[i] in '、。！？':
                        break_pos = i + 1
                        break
                lines.append(words[:break_pos])
                words = words[break_pos:]
            if words:
                lines.append(words)
            text = '\n'.join(lines)
        
        text_overlay = ffmpeg.drawtext(img_input, text,
                            x="(w-text_w)/2", y="h-th-40",
                            fontsize=fontsize, fontcolor="white", box=1, boxcolor="black@0.5", boxborderw=10, 
                            fontfile="/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf")
        scaled_video = ffmpeg.filter(text_overlay, 'scale', w='1080', h='1920', force_original_aspect_ratio='decrease')
        padded_video = ffmpeg.filter(scaled_video, 'pad', w='1080', h='1920', x='(ow-iw)/2', y='(oh-ih)/2')
        video_streams.append(padded_video)
        audio_streams.append(aud_input)





    # 結合
    joined_video = ffmpeg.concat(*video_streams, v=1, a=0) # 動画ストリームのみ結合
    joined_audio = ffmpeg.concat(*audio_streams, v=0, a=1) # 音声ストリームのみ結合

    # 最終的な出力
    ffmpeg.output(joined_video, joined_audio, output_path,
                  vcodec="libx264", acodec="aac", strict="experimental",
                  pix_fmt="yuv420p", r=30, aspect="9:16"
    ).run(overwrite_output=True)

    print(f"Video generated successfully: {output_path}")

    # クリーンアップ
    for f in audio_files + image_files:
        if os.path.exists(f):
            os.remove(f)
    if os.path.exists(temp_dir) and not os.listdir(temp_dir):
        os.rmdir(temp_dir)

if __name__ == '__main__':
    # For testing purposes
    # 環境変数UNSPLASH_ACCESS_KEYとGOOGLE_APPLICATION_CREDENTIALSを設定してください
    # export UNSPLASH_ACCESS_KEY="YOUR_UNSPLASH_ACCESS_KEY"
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/google_credentials.json"
    sample_text = "AI技術の進化が目覚ましいです。私たちの生活に大きな変化をもたらしています。特に、画像生成AIや自然言語処理AIは、クリエイティブな分野やビジネスの現場で活用が進んでいます。これにより、これまで人間が行っていた作業の一部が自動化され、より効率的なコンテンツ制作が可能になりました。しかし、AIの活用には倫理的な問題や著作権の問題など、まだ多くの課題が残されています。私たちはこれらの課題と向き合いながら、AI技術を社会に役立てていく必要があります。"
    generate_video_from_text(sample_text, "final_video.mp4")


