from flask import Flask, request, jsonify
from flask_cors import CORS
import time
import json

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({
        'message': 'Vrewriter Backend API is running',
        'status': 'success'
    })

@app.route('/api/video-simple/status')
def status():
    return jsonify({
        'status': 'Simple video generation service is running',
        'version': '1.0.0'
    })

@app.route('/api/video-simple/generate', methods=['POST'])
def generate_video():
    try:
        # リクエストデータを取得
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'Text is required'}), 400
        
        input_text = data['text']
        
        # 処理時間をシミュレート
        time.sleep(2)
        
        # テスト用のレスポンス
        response = {
            'success': True,
            'message': 'Video generated successfully (test mode)',
            'video_url': '/static/test_video.mp4',
            'input_text': input_text,
            'processing_time': '2 seconds'
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500

@app.route('/api/test')
def test():
    return jsonify({
        'message': 'API test endpoint',
        'status': 'working'
    })

if __name__ == '__main__':
    app.run(debug=True)

