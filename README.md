# 🌱 Auto Grass Bot

毎日23:50（JST）に自動でGitHubの草を生やすGitHub Actionsボットです。

## 🎯 機能

- **自動実行**: 毎日23:50（JST）にGitHub Actionsが自動実行
- **スマート判定**: その日のContributionが0の場合のみコミット実行
- **手動実行**: 必要に応じて手動で実行可能
- **ログ記録**: 自動コミットの履歴を`grass_log.txt`に記録

## 🚀 セットアップ

### 1. リポジトリにプッシュ

このリポジトリをGitHubにプッシュしてください。

### 2. GitHub Actionsの有効化

1. GitHubリポジトリの「Actions」タブに移動
2. 「Auto Grass Bot」ワークフローが表示されることを確認
3. 初回実行は手動で「Run workflow」をクリック

### 3. 権限の確認

- `GITHUB_TOKEN`は自動で提供されます
- プライベートリポジトリの場合は、リポジトリの設定で「Actions」の権限を確認してください

## 📅 スケジュール

- **実行時間**: 毎日23:50（日本時間）
- **UTC時間**: 14:50（日本時間-9時間）
- **cron式**: `50 14 * * *`

## 🔧 動作の仕組み

1. **Contributionチェック**: GitHub GraphQL APIで今日のContribution数を取得
2. **条件判定**: Contribution数が0の場合のみ処理実行
3. **自動コミット**: `grass_log.txt`にタイムスタンプを追加してコミット
4. **プッシュ**: 変更をリポジトリにプッシュ

## 📁 ファイル構成

```
.github/
├── workflows/
│   └── auto-grass.yml      # GitHub Actionsワークフロー
└── scripts/
    └── check_and_commit.py # メイン処理スクリプト
├── grass_log.txt           # 自動コミットログ（自動生成）
└── README.md              # このファイル
```

## 🛠️ カスタマイズ

### 実行時間の変更

`.github/workflows/auto-grass.yml`の`cron`行を編集：

```yaml
- cron: '50 14 * * *'  # 現在: 23:50 JST
```

### コミットメッセージの変更

`.github/scripts/check_and_commit.py`の`make_auto_commit()`関数内を編集：

```python
subprocess.run(["git", "commit", "-m", f"🌱 Auto grass commit - {timestamp}"], check=True)
```

## 🔍 ログの確認

自動コミットの履歴は`grass_log.txt`で確認できます：

```
🌱 Auto grass commit at 2024-01-15T14:50:00.123456
🌱 Auto grass commit at 2024-01-16T14:50:00.234567
```

## ⚠️ 注意事項

- GitHub Actionsの無料枠は月2,000分（パブリックリポジトリは無制限）
- このボットは1日1回実行されるため、月約30分の使用量
- プライベートリポジトリの場合は使用量に注意

## 🎉 完了！

セットアップが完了すると、毎日23:50に自動で草が生えるようになります！

---

**免責事項**: このボットは学習目的で作成されています。GitHubの利用規約に従ってご利用ください。 