# ツイートのトピック分類

TwitterのフォロワーのツイートをLDAを用いてトピック分類してみる一連のプログラム。

## 準備

TwitterAPIを使うのでデベロッパー登録して，環境変数にトークンなどを設定しておく。

### 環境変数

- TWITTER_DEV_ENV : Twitter Dev で登録した開発用 Environment 名
- API_KEY : Twitter Dev で取得した API_KEY
- API_SECRET_TOKEN : Twitter Dev で取得した API_SECRET_TOKEN
- ACCESS_TOKEN : Twitter Dev で取得した ACCESS_TOKEN
- ACCESS_TOKEN_SECRET : Twitter Dev で取得した ACCESS_TOKEN_SECRET
- MECAB_DIC : MeCab辞書のディレクトリ

## Twitter関連

### get_userinfo.py

指定されたユーザのユーザ情報を取得し，画面に表示する。
ユーザはユーザIDまたはスクリーン名で指定する。

#### 利用法

``` shell
python get_followrs.py -u 10010
```

#### オプション

- **-u / --user_id** : ユーザIDを指定する。
- **-s / --screen_name** : スクリーン名（ユーザ名）を指定する。

### get_followers.py

指定されたユーザをフォローしているユーザのIDを収集する。
ユーザはユーザIDまたはスクリーン名で指定する。

#### 利用法

``` shell
python get_followrs.py -u 10010 -f output.json -c 100
```

#### オプション

- **-u / --user_id** : ユーザIDを指定する。
- **-s / --screen_name** : スクリーン名（ユーザ名）を指定する。
- **-c / --count** : 取得するフォロワーの最大数。
- **-f / --filename** : 出力するファイル名。JSON形式で出力される。
指定がない場合は画面上に出力される。

### get_friends.py

指定されたユーザがフォローしているユーザ（友人）のIDを収集する。
ユーザはユーザIDまたはスクリーン名で指定する。

#### 利用法

``` shell
python get_friends.py -u 10010 -f output.json -c 100
```

#### オプション

- **-u / --user_id** : ユーザIDを指定する。
- **-s / --screen_name** : スクリーン名（ユーザ名）を指定する。
- **-c / --count** : 取得する友人の最大数。
- **-f / --filename** : 出力するファイル名。JSON形式で出力される。
指定がない場合は画面上に出力される。

### get_timeline.py

指定されたユーザのツイートを収集する。

#### 利用法

``` shell
python get_timeline.py -s hoge -f tweets20200801 -n 100
```

#### オプション

- **-u / --user_id** : ユーザIDを指定する。
- **-s / --screen_name** : スクリーン名（ユーザ名）を指定する。
- **-n / --num_tweets** : 取得するツイートの数。
- **-f / --base_filename** : 出力するファイル名。ツイートはJSON形式で出力される。
指定がない場合は画面上に出力される。

### get_friends_tweets.py

指定されたユーザがフォローしているユーザ（友人）のツイートを収集する。

#### 利用法

``` shell
python get_friends_tweets.py -s hoge -f tweets20200801 -c 50 -n 100
```

#### オプション

- **-u / --user_id** : ユーザIDを指定する。
- **-s / --screen_name** : スクリーン名（ユーザ名）を指定する。
- **-c / --count** : 取得する友人の最大数。
- **-n / --num_tweets** : 各友人について取得するツイートの数。
- **-f / --base_filename** : 出力するファイル名の接頭辞。
ツイートはJSON形式で出力され，実際のファイル名は「接頭辞_ユーザID.json」のようになる。
指定がない場合は画面上に出力される。

### トピック分類（LDA）

### create_corpus.py

コーパスと辞書を作成する。

#### 利用法

``` shell
python create_corpus.py -d dic/hoge.dict -c dic/hoge.mm -u 0.8 -l 3 a.json b.json c.json
```

#### オプション

- **-c / --corpus** : 出力するコーパスファイル名。
- **-d / --dictionary** : 出力する辞書ファイル名。
- **-u / --upper_limit** : 出現頻度が多すぎる単語を辞書に含めないようにするため，
辞書に含める単語の出現頻度の上限を実数値（0.0〜1.0）で指定する。
- **-l / --lower_limit** : 出現回数が少なすぎる単語を辞書に含めないようにするため，
辞書に含める単語の出現回数の下限を整数で指定する。
- JSONファイル : ツイートファイルを指定する。

### calc_topic_num.py

トピック数を決定するために，トピック数を変えながら，PerplexityとCoherenceを計算，プロットする。

#### 利用法

``` shell
python calc_topic_num.py \
    -d dic/hoge.dict -c dic/hoge.mm \
    --start 2 --limit 10 --step 3 \
    -s output.pdf \
    -m "c_v" \
    -r 10
    a.json b.json c.json
```

この例では，トピック数を2から10に3刻みで変化（2,5,8）させながら，
それぞれのトピック数では10回計算を繰り返し，その平均をPDF形式で出力する。

#### オプション

- **-c / --corpus** : コーパスファイル名（mmで終わるもの）を指定する。
- **-d / --dictionary** : 辞書ファイル名を指定する。
- **--start** : トピック数の初期値。
- **--limit** : トピック数の最大値。
- **--step** : トピック数の増分。
- **-m / --coherence_measure** : Coherenceの計算方法。デフォルトは "c_v"。
その他に "u_mass", "c_uci", "c_nmpi" が指定できる。
手法の違いは
[gensimのCoherenceモデル](https://radimrehurek.com/gensim/models/coherencemodel.html) を参照のこと。
- **-r / --repeat** : PerprexityやCoherenceは乱数によって，その値が毎回変わるため，
その影響を減らすために，平均値を計算する。
その平均値を計算するために複数回の計算が必要となるが，その回数を指定する。
- **-s / --save_fig** : 保存するプロットのファイル名。
画像形式は拡張子から自動的に決定される。
ファイル名が指定されない場合は画面に表示される。
- **-t / --use_tfidf** : TF-IDFコーパスを利用する。
- JSONファイル : ツイートファイルを指定する。

### create_model.py

### check_model.py

### infer_topic_from_text.py

### visualize_by_html.py

### visualize_by_wordcloud.py

