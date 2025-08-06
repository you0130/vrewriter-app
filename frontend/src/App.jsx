import { useState } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Textarea } from '@/components/ui/textarea.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Loader2, Video, Sparkles, Download, Play } from 'lucide-react'
import './App.css'

function App() {
  const [inputText, setInputText] = useState('')
  const [isGenerating, setIsGenerating] = useState(false)
  const [generatedVideo, setGeneratedVideo] = useState(null)
  const [error, setError] = useState(null)

  const handleGenerate = async () => {
    if (!inputText.trim()) {
      setError('テキストを入力してください')
      return
    }

    setIsGenerating(true)
    setError(null)
    setGeneratedVideo(null)

    try {
      const response = await fetch('http://localhost:5001/api/video-simple/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: inputText }),
      })

      if (!response.ok) {
        throw new Error('動画生成に失敗しました')
      }

      const result = await response.json()
      setGeneratedVideo(`http://localhost:5001${result.video_url}`)
    } catch (err) {
      setError(err.message)
    } finally {
      setIsGenerating(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-indigo-100 dark:from-gray-900 dark:via-purple-900 dark:to-indigo-900">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="flex items-center justify-center gap-2 mb-4">
            <Video className="h-8 w-8 text-purple-600" />
            <h1 className="text-4xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
              Vrewriter
            </h1>
          </div>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            AIが文章からショート動画を自動生成。あなたのアイデアを魅力的な動画コンテンツに変換します。
          </p>
          <div className="flex items-center justify-center gap-2 mt-4">
            <Badge variant="secondary" className="flex items-center gap-1">
              <Sparkles className="h-3 w-3" />
              AI生成
            </Badge>
            <Badge variant="secondary">ショート動画</Badge>
            <Badge variant="secondary">自動テロップ</Badge>
          </div>
        </div>

        {/* Main Content */}
        <div className="max-w-4xl mx-auto">
          <Card className="mb-8">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Sparkles className="h-5 w-5 text-purple-600" />
                テキストから動画を生成
              </CardTitle>
              <CardDescription>
                記事やブログの内容を入力すると、AIが自動で画像を選定し、音声ナレーション付きのショート動画を生成します。
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <label htmlFor="input-text" className="block text-sm font-medium mb-2">
                  動画にしたいテキスト
                </label>
                <Textarea
                  id="input-text"
                  placeholder="ここに動画にしたいテキストを入力してください。例：AI技術の進化について、最新のトレンドや応用例を紹介します..."
                  value={inputText}
                  onChange={(e) => setInputText(e.target.value)}
                  className="min-h-[120px] resize-none"
                  disabled={isGenerating}
                />
              </div>
              
              {error && (
                <div className="p-3 bg-red-50 border border-red-200 rounded-md text-red-700 text-sm">
                  {error}
                </div>
              )}

              <Button 
                onClick={handleGenerate}
                disabled={isGenerating || !inputText.trim()}
                className="w-full bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700"
                size="lg"
              >
                {isGenerating ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    動画を生成中...
                  </>
                ) : (
                  <>
                    <Video className="mr-2 h-4 w-4" />
                    動画を生成
                  </>
                )}
              </Button>
            </CardContent>
          </Card>

          {/* Generated Video */}
          {generatedVideo && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Play className="h-5 w-5 text-green-600" />
                  生成された動画
                </CardTitle>
                <CardDescription>
                  動画が正常に生成されました。プレビューして、必要に応じてダウンロードしてください。
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="aspect-[9/16] max-w-sm mx-auto bg-black rounded-lg overflow-hidden">
                    <video 
                      controls 
                      className="w-full h-full object-cover"
                      src={generatedVideo}
                    >
                      お使いのブラウザは動画再生をサポートしていません。
                    </video>
                  </div>
                  
                  <div className="flex justify-center">
                    <Button asChild variant="outline">
                      <a href={generatedVideo} download>
                        <Download className="mr-2 h-4 w-4" />
                        動画をダウンロード
                      </a>
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}

          {/* Features */}
          <div className="grid md:grid-cols-3 gap-6 mt-12">
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">AI画像選定</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">
                  テキストの内容に最適な画像をAIが自動で検索・選定します。
                </p>
              </CardContent>
            </Card>
            
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">音声ナレーション</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">
                  自然な日本語音声でテキストを読み上げ、動画に追加します。
                </p>
              </CardContent>
            </Card>
            
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">自動テロップ</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">
                  読みやすいテロップを自動で生成し、動画に重ねて表示します。
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App

