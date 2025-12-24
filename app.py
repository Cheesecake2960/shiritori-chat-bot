from flask import Flask, request, abort
import random

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)
game = 0

省く文字 = ["ァ","ィ","ゥ","ェ","ォ","ャ","ュ","ョ","ッ","ぁ","ぃ","ぅ","ぇ","ぉ","ゃ","ゅ","ょ","っ","ー"]
置き換え先 = ["ア","イ","ウ","エ","オ","ヤ","ユ","ヨ","","あ","い","う","え","お","や","ゆ","よ","",""]

使った言葉 = []

ひらがな = ["あ","い","う","え","お"
         ,"か","き","く","け","こ"
         ,"さ","し","す","せ","そ"
         ,"た","ち","つ","て","と"
         ,"な","に","ぬ","ね","の"
         ,"は","ひ","ふ","へ","ほ"
         ,"ま","み","む","め","も"
         ,"や","ゆ","よ"
         ,"ら","り","る","れ","ろ"
         ,"わ","を","ん"
         ,"が","ぎ","ぐ","げ","ご"
         ,"ざ","じ","ず","ぜ","ぞ"
         ,"だ","ぢ","づ","で","ど"
         ,"ば","び","ぶ","べ","ぼ"
         ,"ぱ","ぴ","ぷ","ぺ","ぽ"
         ,"ぁ","ぃ","ぅ","ぇ","ぉ"
         ,"ゃ","ゅ","ょ","っ"]

カタカナ = ["ア","イ","ウ","エ","オ"
         ,"カ","キ","ク","ケ","コ"
         ,"サ","シ","ス","セ","ソ"
         ,"タ","チ","ツ","テ","ト"
         ,"ナ","ニ","ヌ","ネ","ノ"
         ,"ハ","ヒ","フ","ヘ","ホ"
         ,"マ","ミ","ム","メ","モ"
         ,"ヤ","ユ","ヨ"
         ,"ラ","リ","ル","レ","ロ"
         ,"ワ","ヲ","ン"
         ,"ガ","ギ","グ","ゲ","ゴ"
         ,"ザ","ジ","ズ","ゼ","ゾ"
         ,"ダ","ヂ","ヅ","デ","ド"
         ,"バ","ビ","ブ","ベ","ボ"
         ,"パ","ピ","プ","ペ","ポ"
         ,"ァ","ィ","ゥ","ェ","ォ"
         ,"ャ","ュ","ョ","ッ"]

使える文字 = ["あ","い","う","え","お"
         ,"か","き","く","け","こ"
         ,"さ","し","す","せ","そ"
         ,"た","ち","つ","て","と"
         ,"な","に","ぬ","ね","の"
         ,"は","ひ","ふ","へ","ほ"
         ,"ま","み","む","め","も"
         ,"や","ゆ","よ"
         ,"ら","り","る","れ","ろ"
         ,"わ","を","ん"
         ,"が","ぎ","ぐ","げ","ご"
         ,"ざ","じ","ず","ぜ","ぞ"
         ,"だ","ぢ","づ","で","ど"
         ,"ば","び","ぶ","べ","ぼ"
         ,"ぱ","ぴ","ぷ","ぺ","ぽ"
         ,"ア","イ","ウ","エ","オ"
         ,"カ","キ","ク","ケ","コ"
         ,"サ","シ","ス","セ","ソ"
         ,"タ","チ","ツ","テ","ト"
         ,"ナ","ニ","ヌ","ネ","ノ"
         ,"ハ","ヒ","フ","ヘ","ホ"
         ,"マ","ミ","ム","メ","モ"
         ,"ヤ","ユ","ヨ"
         ,"ラ","リ","ル","レ","ロ"
         ,"ワ","ヲ","ン"
         ,"ガ","ギ","グ","ゲ","ゴ"
         ,"ザ","ジ","ズ","ゼ","ゾ"
         ,"ダ","ヂ","ヅ","デ","ド"
         ,"バ","ビ","ブ","ベ","ボ"
         ,"パ","ピ","プ","ペ","ポ"
         ,"ー"]
count = 1
単語 = ["あり","アーモンド","いぬ","イルカ"
      ,"うし","ウインナー","えいが","エイ"
      ,"おちゃ","オアシス","かきごおり","カカオ"
      ,"ききゅう","キツツキ","くじ","クーラー"
      ,"けしごむ","けいさん","ケース","ケーキ"
      ,"こま","コップ","さくら","サービス"
      ,"しいたけ","シーソー","すうじ","スイカ"
      ,"せいかい","セーブ","そと","ソーダ"
      ,"たいこ","タイトル","ちゅうい","チェック"
      ,"つまようじ","ツリー","てんき","テーブル"
      ,"とうきょう","トマト","なまえ","ナイフ"
      ,"にじ","ニス","ぬいぐるみ","ヌードル"
      ,"ねじ","ネコ","のり","ノート"
      ,"はしご","ハチ","ひじ","ヒーロー"
      ,"ふぐ","ファミリー","へいわ","ヘリコプター"
      ,"ほうじちゃ","ホーム","まいにち","マネージャー"
      ,"みぎ","ミーティング","むら","ムービー"
      ,"めぐすり","メール","もり","モデル"
      ,"やま","ヤギ","ゆか","ユーザー"
      ,"よこ","ヨーロッパ","らっか","ラッキー"
      ,"りんご","リス","るす","ルール"
      ,"れきし","レア","ろうか","ロープ"
      ,"わに","ワープ","がいこく","ガーゼ"
      ,"ぎじゅつ","ギア","ぐうすう","グループ"
      ,"げんき","ゲーム","ごさ","ゴール"
      ,"ざひょう","ザリガニ","じょうほう","ジェットコースター"
      ,"ずけい","ズッキーニ","ぜったい","ゼリー"
      ,"ぞう","ゾンビ","だいきち","ダーツ"
      ,"づけ","ヅラ","でぐち","ディナー"
      ,"どう","ドア","ばくはつ","バーガー"
      ,"びじゅつ","ビスケット","ぶちょう","ブロック"
      ,"べんきょう","ベスト","ぼう","ボックス"
      ,"ぱくり","パイロット","ぴりから","ピラフ"
      ,"ぷーる","プードル","ぺあ","ペイント"
      ,"ぽんず","ポイント"]

app = Flask(__name__)

configuration = Configuration(access_token='QrjAObw271IelY7cs072QDOabPfpCa4uTEl+7k85OT3pv2YVBWiJPD/JRW44rSVh4sa3fGBaCxelHvjO/PaAduehDmaoC9FnB8x20oUdt20iOSvtIiBbTm4CfB59Rp1hqtankpQMlQyYUg2MZfDsTgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('9f3a0ac7ffd651704e92b9345dfb1f57')

@app.route("/")
def test():
    return "OK"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    global tango
    global game
    global henkan
    global 最後の文字
    global count
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        
        if event.message.text == "しりとり開始" and game == 0:
            count = 1
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text="しりとり")]
                    
                )
            )
            tango = "しりとり"
            game = 1
            使った言葉.clear()
        else:
            if event.message.text[len(event.message.text) - 1] == "ん" or event.message.text[len(event.message.text) - 1] == "ン":
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[TextMessage(text="You lose! あなたの負け!")]
                    )
                )
                使った言葉.clear()
                game = 0
            else:
                can_use=0
                for i in range(len(event.message.text)):
                    if event.message.text[i] in 使える文字:
                        can_use=1          
                if can_use==1:
                    if event.message.text[len(event.message.text) - 1] in 省く文字:
                                最後の文字 = event.message.text[len(event.message.text) - 2]
                    
                    if not tango[len(tango)-1] == "ー":
                        if tango[len(tango)-1] in ひらがな:
                            henkan2 = カタカナ[ひらがな.index(tango[len(tango)-1])]
                        else:
                            henkan2 = ひらがな[カタカナ.index(tango[len(tango)-1])]
        
                    if tango[len(tango)-count] == event.message.text[0] or henkan2 == event.message.text[0]:
                        if not event.message.text in 使った言葉:
                            使った言葉.append(event.message.text)
                            if not event.message.text[len(event.message.text) - count] == "ー":
                                if event.message.text[len(event.message.text) - count] in ひらがな:
                                    henkan = カタカナ[ひらがな.index(event.message.text[len(event.message.text) - count])]
                                else:
                                    henkan = ひらがな[カタカナ.index(event.message.text[len(event.message.text) - count])]
                            if not event.message.text[len(event.message.text) - count] == "ぢ" or not event.message.text[len(event.message.text) - count] == "ヂ":
                                
                                while True: #返答
                                        tango = 単語[random.randint(0,len(単語))-count]#単語決め
                                        save = event.message.text
                                        for i in 省く文字:
                                            save = save.replace(i,'')
                                        if tango[0] == save[len(save) - count] or tango[0] == save:
                                            break

                            
                            
                            line_bot_api.reply_message_with_http_info(
                                    ReplyMessageRequest(
                                        reply_token=event.reply_token,
                                        messages=[TextMessage(text=tango)]
                                    )
                            )
                        else:
                            line_bot_api.reply_message_with_http_info(
                            ReplyMessageRequest(
                            reply_token=event.reply_token,
                            messages=[TextMessage(text="すでに使っている言葉です You lose! あなたの負け！")])
                        )
                            game = 0
                            使った言葉.clear()
                    else:
                        if game == 1:
                            line_bot_api.reply_message_with_http_info(
                                ReplyMessageRequest(
                                reply_token=event.reply_token,
                                messages=[TextMessage(text="最後の文字と最初の文字が違います！ You lose! あなたの負け!")])
                            )
                            game = 0
                            使った言葉.clear()
                else:
                    line_bot_api.reply_message_with_http_info(
                        ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[TextMessage(text="使えない文字が入ってます You lose! あなたの負け!")])
                    )
                    game = 0
                    使った言葉.clear()
                            
                            
if __name__ == "__main__":
    app.run()
