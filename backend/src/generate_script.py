
import os
from openai import OpenAI

def generate_script(text: str) -> list[str]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    prompt = f"""以下の文章を30秒のショート動画用ナレーション原稿に要約してください。5-7文で、1文ずつ改行してください。\n\n{text}"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "あなたはショート動画のナレーション原稿を作成するAIアシスタントです。"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,
        temperature=0.7,
    )
    # レスポンスが空の場合のハンドリングを追加
    if not response.choices or not response.choices[0].message.content:
        print("Warning: OpenAI API returned empty content.")
        return []
    script_text = response.choices[0].message.content.strip()
    # 各文をリストとして返すために、改行で分割する
    return [line.strip() for line in script_text.split('\n') if line.strip()]

if __name__ == '__main__':
    sample_text = """最近、AI技術の進化が目覚ましく、私たちの生活に大きな変化をもたらしています。特に、画像生成AIや自然言語処理AIは、クリエイティブな分野やビジネスの現場で活用が進んでいます。これにより、これまで人間が行っていた作業の一部が自動化され、より効率的なコンテンツ制作が可能になりました。しかし、AIの活用には倫理的な問題や著作権の問題など、まだ多くの課題が残されています。私たちはこれらの課題と向き合いながら、AI技術を社会に役立てていく必要があります。"""
    print("台本生成を開始します...")
    try:
        script = generate_script(sample_text)
        print("台本生成が完了しました:")
        for i, line in enumerate(script):
            print(f"{i+1}. {line}")
    except Exception as e:
        print(f"エラーが発生しました: {e}")


