import os
import tempfile
import time
from flask import Blueprint, request, jsonify, send_file
from flask_cors import cross_origin

video_simple_bp = Blueprint('video_simple', __name__)

@video_simple_bp.route('/generate', methods=['POST'])
@cross_origin()
def generate_video_simple():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'Text is required'}), 400
        
        input_text = data['text']
        
        # 簡単なテスト用レスポンス（実際の動画生成をシミュレート）
        time.sleep(2)  # 処理時間をシミュレート
        
        # テスト用の動画URLを返す（実際には先ほど生成した動画を使用）
        test_video_path = '/home/ubuntu/final_video.mp4'
        
        if os.path.exists(test_video_path):
            # 生成された動画をstaticディレクトリにコピー
            static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'videos')
            os.makedirs(static_dir, exist_ok=True)
            
            video_filename = f'test_video_{hash(input_text) % 10000}.mp4'
            final_path = os.path.join(static_dir, video_filename)
            
            # ファイルをコピー
            import shutil
            shutil.copy2(test_video_path, final_path)
            
            return jsonify({
                'success': True,
                'video_url': f'/static/videos/{video_filename}',
                'message': 'Video generated successfully (test mode)'
            })
        else:
            return jsonify({'error': 'Test video not found'}), 500
                
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@video_simple_bp.route('/status', methods=['GET'])
@cross_origin()
def status():
    return jsonify({'status': 'Simple video generation service is running'})

