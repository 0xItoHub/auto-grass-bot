#!/usr/bin/env python3
"""
Auto Grass Bot - GitHub Actions用スクリプト
毎日23:50に実行され、今日のContributionが0なら自動コミットを実行
"""

import requests
import os
import datetime
import subprocess
import json
import sys


def get_today_contributions(token, username):
    """GitHub GraphQL APIで今日のContribution数を取得"""

    today = datetime.datetime.utcnow().date().isoformat()

    # GraphQLクエリ
    query = (
        """
    query {
      user(login: "%s") {
        contributionsCollection {
          contributionCalendar {
            weeks {
              contributionDays {
                date
                contributionCount
              }
            }
          }
        }
      }
    }
    """
        % username
    )

    headers = {"Authorization": f"bearer {token}", "Content-Type": "application/json"}

    try:
        response = requests.post(
            "https://api.github.com/graphql",
            json={"query": query},
            headers=headers,
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()

        # 今日のContribution数を検索
        for week in data["data"]["user"]["contributionsCollection"][
            "contributionCalendar"
        ]["weeks"]:
            for day in week["contributionDays"]:
                if day["date"] == today:
                    return day["contributionCount"]

        # 今日のデータが見つからない場合は0として扱う
        return 0

    except Exception as e:
        print(f"❌ API呼び出しエラー: {e}")
        return None


def make_auto_commit():
    """自動コミットを実行"""

    timestamp = datetime.datetime.utcnow().isoformat()

    # ログファイルに記録
    log_file = "grass_log.txt"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"🌱 Auto grass commit at {timestamp}\n")

    # Git設定
    subprocess.run(
        ["git", "config", "--global", "user.name", "github-actions[bot]"], check=True
    )
    subprocess.run(
        [
            "git",
            "config",
            "--global",
            "user.email",
            "41898282+github-actions[bot]@users.noreply.github.com",
        ],
        check=True,
    )

    # コミット
    subprocess.run(["git", "add", log_file], check=True)
    subprocess.run(
        ["git", "commit", "-m", f"🌱 Auto grass commit - {timestamp}"], check=True
    )

    print(f"✅ Auto commit created: {timestamp}")


def main():
    """メイン処理"""

    # 環境変数から設定を取得
    token = os.environ.get("GITHUB_TOKEN")
    username = os.environ.get("GH_USERNAME")

    if not token or not username:
        print("❌ 必要な環境変数が設定されていません")
        print(f"GITHUB_TOKEN: {'✅' if token else '❌'}")
        print(f"GH_USERNAME: {'✅' if username else '❌'}")
        sys.exit(1)

    print(f"🔍 Checking contributions for user: {username}")

    # 今日のContribution数を取得
    contributions = get_today_contributions(token, username)

    if contributions is None:
        print("❌ Contribution数の取得に失敗しました")
        sys.exit(1)

    print(f"📊 Today's contributions: {contributions}")

    if contributions > 0:
        print("✅ Contributions already exist for today. No action needed.")
        sys.exit(0)

    print("⚠️ No contributions found for today. Making an auto commit...")

    try:
        make_auto_commit()
        print("🎉 Auto commit completed successfully!")
    except Exception as e:
        print(f"❌ Auto commit failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
