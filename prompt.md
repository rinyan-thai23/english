# System Instructions & Architecture Blueprint: English Reading Acquisition System (Prototype)

## 1. Project Overview & Philosophy
本プロジェクトの主目的は、英会話やスピーキングの習得ではなく、**「海外向けマイクロSaaS・GASツール販売、一次データリサーチ、海外フォーラム読解のための超高速英文リーディング力（受動語彙・構文把握力）」**を最短で獲得するためのプロトタイプ開発である。

手元にある約2,800語（パブリックドメイン語彙DB）のCSVデータを起点とし、無駄な日常会話的文脈を排除して「データ処理・IT・自動化・海外ビジネス」の文脈へ特化させる。
余計なリッチUIや巨大な依存関係は不要。Unix哲学に則った軽量・堅牢・単機能かつ拡張しやすい骨格（Prototype）を構築すること。

---

## 2. Input Data Specifications
入力となるCSVファイル (`ngsl_words.csv` 等) の想定基本スキーマ:
- `id`: 一意のインデックス番号 (int)
- `word`: 対象の英単語 (string)
- `rank`: 頻度ランキング (int, 1-2803等)
- `part_of_speech`: 品詞 (string: n, v, adj, adv 等)

---

## 3. Implementation Roadmap (Step 1 - Step 4)

以下の **Step 1 〜 Step 4** を実行・完結できるコードベース、パイプラインスクリプト、および最小構成のビューアを設計・実装せよ。

```
+-------------------------------------------------------------+
| Step 1: Data Filtering & Categorization Pipeline            |
|   - CSV Ingestion -> Deduplication -> Known Word Filter    |
|   - Syntax/Logic Cluster Tagging (Logic, Action, State)     |
+------------------------------+------------------------------+
                               |
                               v
+-------------------------------------------------------------+
| Step 2: Contextual Data Augmentation via LLM API             |
|   - Batch Worker (15-word strict IT/Business micro-sentences)|
|   - Exponential Backoff & Rate Limit Handling               |
|   - JSONL / Enriched CSV Export                             |
+------------------------------+------------------------------+
                               |
                               v
+-------------------------------------------------------------+
| Step 3: High-Velocity Rapid Reading Viewer (CLI / Minimal UI)|
|   - Zero-Friction "3-Second Per Word" Flash Streamer        |
|   - Keybindings (Next, Known/Mastered, Star for Later)       |
|   - Local Progress Tracker (SQLite / JSON State)            |
+------------------------------+------------------------------+
                               |
                               v
+-------------------------------------------------------------+
| Step 4: Real-World Ingest & Vocabulary Intersect Engine     |
|   - Scrape/Input target English text (GitHub/Reddit/Docs)   |
|   - Tokenize & match against Mastered vs Unknown List        |
|   - Instant Vocabulary Gap & Density Report                 |
+-------------------------------------------------------------+
```

---

### Step 1: データ選別・構文機能クラスタリング (Data Filtering & Functional Tagging)
単なるアルファベット順・頻度順の処理ではなく、「英文の骨格を決める機能」に焦点を当ててデータを分類・選別する前処理パイプラインを実装せよ。

1. **不要語フィルタリング機構**:
   - 既に理解している語（中学レベル等）を即座に除外（`status: known`）できるリストまたはコンフィグを用意すること。
2. **構文機能タグ付け（Functional Role Tagging）**:
   単語を以下の4系統に分類するメタデータカラム `functional_type` を付与するロジックまたはプロンプト定義を構築すること。
   - `logic_direction`: 論理展開・条件・接続（e.g., `unless`, `furthermore`, `despite`, `whereas`）
   - `system_action`: システム操作・データ挙動・変化（e.g., `retrieve`, `extract`, `trigger`, `yield`, `mutate`）
   - `system_state`: 状態定義・制約・属性（e.g., `mandatory`, `latent`, `redundant`, `concurrent`）
   - `domain_entity`: 一般名詞・実体（優先度低）

---

### Step 2: LLM APIによるコンテキスト注入（Contextual Sentence Generation）
各単語に対して、日常会話のノイズを完全に排した「データ/開発/B2Bビジネス」特化の短文を非同期・バッチで一括生成するスクリプトを実装せよ。

1. **生成要件・制約**:
   - 1単語につき「15単語以内の極めて簡潔な英文」を1つ生成。
   - 文脈は必ず **「Webスクレイピング / API連携 / データベース運用 / 海外SaaS販売 / マーケティング自動化」** のいずれかとする。
   - 自然な日本語対訳（直訳調、構文構造がわかるもの）を1つ生成。
   - 構文上のキーとなる品詞や使い方のミニノート（20文字以内）を付与。
2. **堅牢性・実行制御**:
   - API制限（Rate Limit）や接続エラーに対応するリトライ処理（Exponential Backoff）。
   - 途中停止しても再開可能な「進捗保存（Checkpoint）機構」（処理済み行のスキップ）。
   - 出力形式: 後続処理が容易な `enriched_words.jsonl` または `enriched_words.csv`。

---

### Step 3: 高速パッシブインプット用プロトタイプ（Rapid Reading Streamer）
単語を「1語3秒」で脳に叩き込むための、装飾を排除した超高速プロトタイプ（軽量CLIまたは単一HTMLファイル）を構築せよ。

1. **画面・情報レイアウト**:
   - メイン表示: 英単語（大）＋ 発音記号/品詞
   - サブ表示: IT/ビジネス例文（中）＋ 日本語対訳（必要時トグルまたは同時表示）
   - 機能タグ（Logic / Action / State）の視覚的識別
2. **操作系（ゼロフリクション設計）**:
   - キーボード操作完結（スペースキーで次、`K`で習得済みにマークして除外、`S`で要復習フラグ）。
   - 無駄なアニメーションやトランジションは禁止（レイテンシゼロで次を表示）。
3. **学習ログ管理**:
   - 閲覧日時、表示回数、ステータス（`unseen`, `learning`, `mastered`）をローカルファイル（JSONまたはSQLite）に自動保存。

---

### Step 4: 実戦ドキュメント照合・語彙ギャップ解析エンジン (Doc Intersect Engine)
海外展開の実務（GitHub README、Stripe APIドキュメント、RedditのB2Bフォーラム投稿など）の生テキストを入力とし、学習効果を即座に検証するツールを実装せよ。

1. **解析機能**:
   - 入力された英文テキストをトークナイズ（単語分解・原形化）。
   - 自身のDBと突合し、以下の3カテゴリに分類・集計:
     1. **既知・習得済み語彙（Mastered）**: カバー率（%）を算出。
     2. **現在学習中の語彙（Learning / Step 2生成済み）**: 文章中での出現箇所をハイライト。
     3. **未登録の未知語（Unknown / Technical Terms）**: 出現頻度順にソートしてリストアップ。
2. **出力形式**:
   - ターミナル上のサマリー出力、または単一の軽量Markdown/HTMLレポート。

---

## 4. Technical Constraints & Code Quality Requirements
- **言語・環境**: Python 3.10+ または Node.js (TypeScript可)。最小限の外部依存ライブラリで構成すること。
- **アーキテクチャ**: 各Stepが疎結合であり、CLIから単体実行可能なモジュール構造とすること。
- **エラーハンドリング**: ファイル未存在、不正なCSVフォーマット、APIキー未設定、JSONデコードエラーに対する適切なフォールバックを実装すること。