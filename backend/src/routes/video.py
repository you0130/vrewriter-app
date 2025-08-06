import os
import tempfile
import shutil
from flask import Blueprint, request, jsonify, send_file
from flask_cors import cross_origin
import sys

# 動画生成エンジンのインポート
sys.path.append('/home/ubuntu/vrewriter_app')
from generate_video import generate_video_from_text

video_bp = Blueprint('video', __name__)

@video_bp.route('/generate', methods=['POST'])
@cross_origin()
def generate_video():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'Text is required'}), 400
        
        input_text = data['text']
        
        # 一時ディレクトリで動画を生成
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = os.path.join(temp_dir, 'generated_video.mp4')
            
            # 環境変数を設定
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/ubuntu/gcp_credentials.json'
            os.environ['UNSPLASH_ACCESS_KEY'] = 'I0N8VBWuyH3yVq374QHS9ovaFkHbzRPXQ20QA5ULo-Y'
            
            # 動画生成
            generate_video_from_text(input_text, output_path)
            
            if os.path.exists(output_path):
                # 生成された動画をstaticディレクトリにコピー
                static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'videos')
                os.makedirs(static_dir, exist_ok=True)
                
                video_filename = f'video_{hash(input_text) % 10000}.mp4'
                final_path = os.path.join(static_dir, video_filename)
                shutil.copy2(output_path, final_path)
                
                return jsonify({
                    'success': True,
                    'video_url': f'/static/videos/{video_filename}',
                    'message': 'Video generated successfully'
                })
            else:
                return jsonify({'error': 'Video generation failed'}), 500
                
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@video_bp.route('/status', methods=['GET'])
@cross_origin()
def status():
    return jsonify({'status': 'Video generation service is running'})

